# 🎮 Epic Games Free Giveaway History Visualization

A comprehensive Streamlit dashboard for analyzing and visualizing Epic Games Store's free game giveaway history from 2018 to 2025.

## 📋 Features

### 📈 Overview Tab

- **Key Metrics Dashboard**: Total games given away, years covered, total value, and unique categories
- **Games Over Time**: Monthly distribution of free game giveaways
- **Category Distribution**: Pie chart showing game genres/categories breakdown
- **Interactive Charts**: Dynamic visualizations using Plotly

### 📅 Timeline Analysis Tab

- **Yearly Breakdown**: Bar chart showing number of games per year
- **Cumulative Growth**: Line graph displaying total games over time
- **Quarterly Analysis**: Games distributed by quarter
- **Flexible Date Handling**: Automatically detects date columns or falls back to year-based analysis

### 🎯 Game Details Tab

- **Search Functionality**: Find specific games by name
- **Recent Games Preview**: Browse the latest giveaways
- **Most Valuable Giveaways**: Top 10 games by original price (if price data available)
- **Interactive Tables**: Sortable and filterable game information

### 📊 Raw Data Tab

- **Statistical Summary**: Descriptive statistics for all numeric columns
- **Full Dataset View**: Complete data table with all columns
- **CSV Export**: Download the dataset for offline analysis
- **Column Information**: Detailed metadata about each column (type, null counts)

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Required Packages

```bash
pip install streamlit pandas plotly kagglehub certifi
```

### Package Descriptions

- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive visualization library
- `kagglehub`: Kaggle dataset downloader
- `certifi`: SSL certificate management

## 🏃 How to Run

### Method 1: Direct Download from Kaggle (Recommended)

1. **Configure Kaggle API** (first time only):

   - Create a Kaggle account at [kaggle.com](https://www.kaggle.com)
   - Go to Account Settings → API → "Create New API Token"
   - This downloads `kaggle.json` to your computer
   - Place `kaggle.json` in:
     - **Windows**: `C:\Users\<YourUsername>\.kaggle\kaggle.json`
     - **Mac/Linux**: `~/.kaggle/kaggle.json`

2. **Run the application**:

   ```bash
   streamlit run app.py
   ```

3. **In the app**:
   - Select "Download from Kaggle" in the sidebar
   - The dataset will download automatically
   - Analysis begins immediately after loading

### Method 2: Manual CSV Upload

1. **Download the dataset manually**:

   - Visit: https://www.kaggle.com/datasets/prajwaldongre/epic-games-free-giveaway-history-20182025
   - Click "Download" button
   - Save the CSV file to your computer

2. **Run the application**:

   ```bash
   streamlit run app.py
   ```

3. **In the app**:
   - Select "Upload CSV file" in the sidebar
   - Click "Browse files" and select your downloaded CSV
   - Analysis begins immediately after upload

## 🔧 Troubleshooting

### SSL Certificate Error

If you see a TLS/SSL certificate error:

- The app automatically handles this with `certifi`
- If it persists, use Method 2 (Manual Upload) instead

### No Date Column Warning

- The app will automatically detect year columns as a fallback
- Check the "View Columns & Types" expander in the sidebar
- Verify your date columns are properly formatted

### File Not Found

- Ensure the CSV file is in the same directory as the script
- Check file permissions
- Try the alternative data loading method

## 📊 Expected Data Format

The application works best with datasets containing:

- **Game names/titles**: Identifies individual games
- **Dates**: Start/end dates or year information
- **Prices**: Original game prices (optional)
- **Genres/Categories**: Game classifications (optional)

The app automatically adapts to different column names and structures.

## 💡 Usage Tips

1. **Explore Tabs**: Each tab offers different insights into the data
2. **Use Search**: Quickly find specific games in the Game Details tab
3. **Download Data**: Export filtered or processed data from the Raw Data tab
4. **Check Sidebar**: View dataset information and column structure
5. **Interactive Charts**: Hover over charts for detailed information, zoom, and pan

## 🎯 Key Use Cases

- Track Epic Games Store's giveaway trends over time
- Analyze most valuable free games offered
- Compare giveaway frequency across different years
- Research game categories and genres
- Export data for custom analysis

## 📝 Notes

- The application uses caching for efficient data loading
- All visualizations are interactive and responsive
- Dark/light mode follows your system preferences
- Works on desktop and tablet browsers

## 🆘 Support

If you encounter issues:

1. Check that all packages are installed correctly
2. Verify your Kaggle API credentials (for Method 1)
3. Try the alternative loading method
4. Check the sidebar for dataset information and diagnostics

---

**Data Source**: Epic Games Free Giveaway History (2018-2025) via Kaggle  
**Created with**: Streamlit 🎈  
**Created By**: Ayman JANATI & Anas JARMOUNI
