# Stock Price Prediction and Data Scraping

This project consists of two parts:
1. **Data Scraping**: Scrapes stock market data for a given stock ticker.
2. **Stock Price Prediction**: Uses machine learning techniques to predict future stock prices based on historical data.

## Project Overview

The goal of this project is to:
- Scrape stock data from Yahoo Finance using `yfinance`.
- Perform data preprocessing and clean the dataset.
- Build a stock price prediction model using `RandomForestRegressor`.
- Provide a user-friendly interface using `Streamlit` for real-time stock price predictions.

---

## Features

### 1. Data Scraping
- Fetches stock market data from Yahoo Finance using the `yfinance` library.
- The user can input the stock ticker and define the date range for which data is to be scraped.
- The project supports historical stock data scraping, including Open, High, Low, Close, and Volume data.

### 2. Stock Price Prediction
- Uses `RandomForestRegressor` from scikit-learn to build a prediction model based on historical stock data.
- Prepares the data and splits it into training and testing sets.
- Predicts future stock prices and visualizes the results.
- The model's performance is evaluated using Mean Squared Error (MSE).

---

## Getting Started

### Prerequisites

Ensure that you have Python 3.7 or later installed on your system.

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/kspn675/Project.git
   ```

2. Navigate into the project folder:
   ```bash
   cd Project
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **For Data Scraping**:
   - The data scraping script fetches stock market data for a given ticker symbol and date range.
   - To run the scraping, use the following command:
     ```bash
     python "Data Scraping.py"
     ```

2. **For Stock Price Prediction**:
   - To run the stock price prediction model and Streamlit interface, use:
     ```bash
     streamlit run "Prediction Model.py"
     ```

### Dependencies

- `yfinance`: Used to fetch stock market data from Yahoo Finance.
- `pandas`: Data manipulation and analysis library.
- `matplotlib`: Used for data visualization.
- `scikit-learn`: For building and evaluating the machine learning model.
- `streamlit`: For building the interactive web app interface.
- `plotly`: For advanced interactive plotting.

To install all the required dependencies, you can use the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## How the Model Works

### Data Scraping
- The stock data is fetched from Yahoo Finance using the `yfinance` library.
- The user provides a stock ticker (e.g., AAPL for Apple) and a date range.
- The stock data is saved into a dataframe, which is then used for further analysis and prediction.

### Stock Price Prediction
1. **Data Preprocessing**: 
   - Historical stock prices are retrieved.
   - Moving averages (MA_5, MA_10) are calculated for trend analysis.
   
2. **Model Training**:
   - The data is split into training and test sets.
   - A `RandomForestRegressor` model is trained to predict future stock prices.
   
3. **Evaluation**:
   - The model’s performance is evaluated using Mean Squared Error (MSE).
   
4. **Forecasting**:
   - The model predicts future stock prices for a user-defined forecast period.

---

## Notes
- Make sure you provide a valid stock ticker when using the app.
- The model’s predictions are based on historical data and may not always be accurate.
- You can adjust the forecast period to predict stock prices for a different number of days.

---

## Acknowledgments

- `yfinance` for providing the easy-to-use API to fetch stock data.
- `scikit-learn` for providing powerful tools to train and evaluate the prediction model.
- `Streamlit` for creating the user-friendly interface.
