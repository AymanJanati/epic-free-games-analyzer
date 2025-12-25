import kagglehub
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import ssl
import certifi

# Fix SSL certificate issue
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()


# Page config
st.set_page_config(
    page_title="Epic Games Free Giveaway Analysis", layout="wide", page_icon="🎮")

# Title and description
st.title("🎮 Epic Games Free Giveaway History (2018-2025)")
st.markdown("Analysis and visualization of Epic Games Store free game giveaways")

# Load data with caching


@st.cache_data
def load_data_from_kaggle():
    try:
        # Set SSL certificate environment variables
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

        # Download dataset
        path = kagglehub.dataset_download(
            "prajwaldongre/epic-games-free-giveaway-history-20182025")

        # Find CSV file in the downloaded path
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

        if not csv_files:
            return None, "No CSV file found in the dataset"

        # Load the first CSV file
        df = pd.read_csv(os.path.join(path, csv_files[0]))

        # Try to parse date columns
        date_columns = [col for col in df.columns if 'date' in col.lower(
        ) or 'start' in col.lower() or 'end' in col.lower()]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                pass

        return df, None
    except Exception as e:
        return None, str(e)


def load_data_from_upload(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)

        # Try to parse date columns - be more aggressive in detection
        date_keywords = ['date', 'start', 'end', 'time', 'year',
                         'month', 'day', 'giveaway', 'free', 'available']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in date_keywords):
                try:
                    # Try different date parsing strategies
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    if df[col].notna().sum() == 0:
                        # If all dates failed, try other formats
                        try:
                            df[col] = pd.to_datetime(
                                df[col], format='mixed', errors='coerce')
                        except:
                            pass
                except:
                    pass

        return df, None
    except Exception as e:
        return None, str(e)


# Data loading options
st.sidebar.header("📁 Data Source")
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Download from Kaggle", "Upload CSV file"],
    help="If Kaggle download fails, you can manually download the CSV and upload it here"
)

df = None
error_msg = None

if data_source == "Download from Kaggle":
    with st.spinner("Loading dataset from Kaggle..."):
        df, error_msg = load_data_from_kaggle()

    if error_msg:
        st.error(f"Error loading from Kaggle: {error_msg}")
        st.info("💡 Try using 'Upload CSV file' option instead. Download the dataset manually from: https://www.kaggle.com/datasets/prajwaldongre/epic-games-free-giveaway-history-20182025")
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        with st.spinner("Loading uploaded file..."):
            df, error_msg = load_data_from_upload(uploaded_file)

        if error_msg:
            st.error(f"Error loading file: {error_msg}")
    else:
        st.info("👆 Please upload the Epic Games dataset CSV file using the sidebar")
        st.markdown(
            "Download it from: [Kaggle Dataset](https://www.kaggle.com/datasets/prajwaldongre/epic-games-free-giveaway-history-20182025)")

if df is not None:
    # Sidebar filters
    st.sidebar.header("📊 Filters")

    # Display dataset info
    st.sidebar.subheader("Dataset Info")
    st.sidebar.write(f"Total Games: {len(df)}")
    st.sidebar.write(f"Columns: {len(df.columns)}")

    # Show column names and types
    with st.sidebar.expander("View Columns & Types", expanded=True):
        for col in df.columns:
            col_type = str(df[col].dtype)
            st.write(f"**{col}**: {col_type}")

    # Show sample data
    with st.sidebar.expander("View Sample Data"):
        st.dataframe(df.head(3))

    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Overview", "📅 Timeline", "🎯 Game Details", "📊 Raw Data"])

    with tab1:
        st.header("Overview Statistics")

        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Games Given Away", len(df))

        with col2:
            # Try to find date column for year analysis
            date_col = next(
                (col for col in df.columns if 'date' in col.lower()), None)
            if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
                years = df[date_col].dt.year.nunique()
                st.metric("Years Covered", years)
            else:
                st.metric("Columns Available", len(df.columns))

        with col3:
            # Try to find price column
            price_col = next((col for col in df.columns if 'price' in col.lower(
            ) or 'value' in col.lower()), None)
            if price_col:
                try:
                    total_value = df[price_col].sum()
                    st.metric("Total Value", f"${total_value:,.2f}")
                except:
                    st.metric("Data Points", len(df) * len(df.columns))
            else:
                st.metric("Data Points", len(df) * len(df.columns))

        with col4:
            # Try to find genre/category column
            genre_col = next((col for col in df.columns if 'genre' in col.lower(
            ) or 'category' in col.lower() or 'tag' in col.lower()), None)
            if genre_col:
                unique_genres = df[genre_col].nunique()
                st.metric("Unique Categories", unique_genres)
            else:
                st.metric("Rows", len(df))

        st.divider()

        # Visualizations based on available columns
        col_left, col_right = st.columns(2)

        with col_left:
            # Try to find any useful column for visualization
            date_col = next(
                (col for col in df.columns if 'date' in col.lower()), None)

            if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
                st.subheader("Games Given Away Over Time")
                df_clean = df.dropna(subset=[date_col])
                df_clean['Year'] = df_clean[date_col].dt.year
                df_clean['Month'] = df_clean[date_col].dt.to_period(
                    'M').astype(str)

                games_per_month = df_clean.groupby(
                    'Month').size().reset_index(name='Count')

                fig = px.bar(games_per_month, x='Month', y='Count',
                             title='Games Per Month',
                             labels={'Count': 'Number of Games',
                                     'Month': 'Month'},
                             color='Count',
                             color_continuous_scale='Blues')
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Show top items from first text column
                text_cols = df.select_dtypes(include=['object']).columns
                if len(text_cols) > 0:
                    first_text_col = text_cols[0]
                    st.subheader(f"Top 15 by {first_text_col}")
                    top_items = df[first_text_col].value_counts().head(15)

                    fig = px.bar(x=top_items.values, y=top_items.index,
                                 orientation='h',
                                 title=f'Most Common {first_text_col}',
                                 labels={'x': 'Count', 'y': first_text_col},
                                 color=top_items.values,
                                 color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No suitable column found for visualization")

        with col_right:
            # Genre/Category distribution
            genre_col = next((col for col in df.columns if 'genre' in col.lower(
            ) or 'category' in col.lower() or 'tag' in col.lower()), None)
            if genre_col:
                st.subheader("Distribution by Category")
                genre_counts = df[genre_col].value_counts().head(10)

                fig = px.pie(values=genre_counts.values, names=genre_counts.index,
                             title=f'Top 10 {genre_col}',
                             hole=0.3)
                fig.update_traces(textposition='inside',
                                  textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Try to find any categorical column with reasonable unique values
                for col in df.select_dtypes(include=['object']).columns:
                    unique_count = df[col].nunique()
                    if 2 < unique_count < 50:  # Sweet spot for pie chart
                        st.subheader(f"Distribution: {col}")
                        value_counts = df[col].value_counts().head(10)

                        fig = px.pie(values=value_counts.values, names=value_counts.index,
                                     title=f'Top 10 {col}',
                                     hole=0.3)
                        fig.update_traces(
                            textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                        break
                else:
                    # Fallback: Show distribution of row indices or IDs
                    st.subheader("Dataset Distribution")
                    st.info(
                        f"Dataset contains {len(df)} total entries across {len(df.columns)} columns")

                    # Show a simple bar chart of data completeness
                    completeness = (df.notna().sum() / len(df)
                                    * 100).sort_values(ascending=False)
                    fig = px.bar(x=completeness.values, y=completeness.index,
                                 orientation='h',
                                 title='Data Completeness by Column',
                                 labels={
                                     'x': 'Completeness (%)', 'y': 'Column'},
                                 color=completeness.values,
                                 color_continuous_scale='Greens')
                    st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Timeline Analysis")

        # More flexible date column detection
        date_keywords = ['date', 'start', 'end', 'time',
                         'year', 'giveaway', 'free', 'available']
        potential_date_cols = [col for col in df.columns if any(
            keyword in col.lower() for keyword in date_keywords)]
        date_col = None

        # Find first valid datetime column
        for col in potential_date_cols:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                date_col = col
                break

        # If no datetime column found, try to find year column or parse manually
        if not date_col:
            st.warning(
                "⚠️ No datetime column detected. Looking for alternative date information...")

            # Check for Year column or similar
            year_cols = [col for col in df.columns if 'year' in col.lower()]
            if year_cols:
                st.info(f"Found year column: {year_cols[0]}")
                year_col = year_cols[0]

                # Create visualizations based on year
                st.subheader("Games per Year")
                try:
                    games_per_year = df[year_col].value_counts(
                    ).sort_index().reset_index()
                    games_per_year.columns = ['Year', 'Games']

                    fig = px.bar(games_per_year, x='Year', y='Games',
                                 title='Free Games Given Away Each Year',
                                 color='Games',
                                 color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)

                    # Cumulative
                    games_per_year['Cumulative'] = games_per_year['Games'].cumsum()
                    fig = px.line(games_per_year, x='Year', y='Cumulative',
                                  title='Cumulative Free Games',
                                  labels={'Cumulative': 'Total Games', 'Year': 'Year'})
                    fig.update_traces(line_color='#0078F2')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating year-based visualization: {e}")
            else:
                st.error("❌ No date or year column found in the dataset.")
                st.info("Available columns: " + ", ".join(df.columns.tolist()))
                st.markdown(
                    "**Suggestion:** The dataset might have date information in a different format. Try checking the Raw Data tab to see the column structure.")

        else:
            # Original datetime-based analysis
            df_timeline = df.dropna(subset=[date_col]).copy()
            df_timeline['Year'] = df_timeline[date_col].dt.year
            df_timeline['Quarter'] = df_timeline[date_col].dt.quarter

            # Games per year
            st.subheader("Games per Year")
            games_per_year = df_timeline.groupby(
                'Year').size().reset_index(name='Games')

            fig = px.bar(games_per_year, x='Year', y='Games',
                         title='Free Games Given Away Each Year',
                         color='Games',
                         color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)

            # Cumulative games over time
            st.subheader("Cumulative Games Over Time")
            df_timeline_sorted = df_timeline.sort_values(date_col)
            df_timeline_sorted['Cumulative'] = range(
                1, len(df_timeline_sorted) + 1)

            fig = px.line(df_timeline_sorted, x=date_col, y='Cumulative',
                          title='Cumulative Free Games on Epic Store',
                          labels={'Cumulative': 'Total Games', date_col: 'Date'})
            fig.update_traces(line_color='#0078F2')
            st.plotly_chart(fig, use_container_width=True)

            # Quarterly breakdown
            st.subheader("Games by Quarter")
            games_by_quarter = df_timeline.groupby(
                ['Year', 'Quarter']).size().reset_index(name='Games')
            games_by_quarter['Quarter_Label'] = games_by_quarter['Year'].astype(
                str) + ' Q' + games_by_quarter['Quarter'].astype(str)

            fig = px.bar(games_by_quarter, x='Quarter_Label', y='Games',
                         title='Games by Quarter',
                         color='Games',
                         color_continuous_scale='Teal')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Game Details")

        # Search functionality
        game_col = next((col for col in df.columns if 'game' in col.lower(
        ) or 'title' in col.lower() or 'name' in col.lower()), None)

        if game_col:
            search_term = st.text_input("🔍 Search for a game:", "")

            if search_term:
                filtered_df = df[df[game_col].str.contains(
                    search_term, case=False, na=False)]
                st.write(
                    f"Found {len(filtered_df)} games matching '{search_term}'")
                st.dataframe(filtered_df, use_container_width=True)
            else:
                # Show top games by any available metric
                st.subheader("Recent Games")
                display_cols = [col for col in df.columns if col != 'index']
                st.dataframe(df[display_cols].head(
                    20), use_container_width=True)
        else:
            st.subheader("Dataset Preview")
            st.dataframe(df.head(20), use_container_width=True)

        # Additional analysis if price column exists
        price_col = next((col for col in df.columns if 'price' in col.lower(
        ) or 'value' in col.lower()), None)
        if price_col and game_col:
            st.subheader("Most Valuable Giveaways")
            try:
                top_games = df.nlargest(10, price_col)[[game_col, price_col]]

                fig = px.bar(top_games, x=price_col, y=game_col, orientation='h',
                             title='Top 10 Most Valuable Free Games',
                             labels={
                                 price_col: 'Original Price ($)', game_col: 'Game'},
                             color=price_col,
                             color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Unable to display price analysis")

    with tab4:
        st.header("Raw Data")

        st.subheader("Dataset Summary")
        st.write(df.describe())

        st.subheader("Full Dataset")
        st.dataframe(df, use_container_width=True)

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name="epic_games_giveaway_data.csv",
            mime="text/csv",
        )

        # Column information
        st.subheader("Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values
        })
        st.dataframe(col_info, use_container_width=True)

else:
    st.info("👆 Please select a data source and load the dataset to begin analysis")

# Footer
st.divider()
st.markdown(
    "**Data Source:** Epic Games Free Giveaway History (2018-2025) via Kaggle")
st.markdown("Made by: Ayman JANATI & Anas JARMOUNI")
