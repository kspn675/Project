import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# App Configurations
st.set_page_config(page_title="Stock Prediction App", layout="wide", page_icon="📈")

# Title and Introduction with custom font and styling
st.title("📈 **Interactive Stock Movement Prediction**")
st.markdown("""
This app predicts whether the stock price will move **upwards** or **downwards** based on historical data and machine learning techniques. 🚀  
Use the sidebar to input stock details and customize the analysis.
""")
st.markdown("---")

# Sidebar Styling
st.sidebar.markdown("""
<style>
    .sidebar .sidebar-content {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content .element-container {
        border-radius: 10px;
        background-color: #f8f9fa;
        padding: 1rem;
    }
    .sidebar .sidebar-content .element-container input {
        font-size: 14px;
        border-radius: 8px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("🔧 Configuration Panel")
with st.sidebar:
    ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA):", value="AAPL")
    start_date = st.date_input("Select Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("Select End Date", value=pd.to_datetime("2023-01-01"))
    test_size = st.slider("Test Size (Percentage for Testing)", min_value=10, max_value=50, value=20, step=5)
    run_model = st.button("🚀 Run Analysis")

# Main Content with structured sections and increased spacing
if run_model and ticker:
    st.header(f"Analyzing Stock: {ticker}")
    try:
        # Fetching Stock Data
        st.markdown("### 📊 **Stock Data Preview**")
        data = yf.download(ticker, start=start_date, end=end_date)
        data.reset_index(inplace=True)

        if data.empty:
            st.error("No data found for the specified ticker and date range.")
        else:
            st.dataframe(data.head(10), use_container_width=True)

            # Adding Tabs for Data Processing
            tabs = st.tabs(["Feature Engineering", "Model Training", "Performance Metrics", "Visualizations"])

            # Feature Engineering
            with tabs[0]:
                st.subheader("🔍 Feature Engineering")
                data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
                data['MA_5'] = data['Close'].rolling(window=5).mean()
                data['MA_10'] = data['Close'].rolling(window=10).mean()
                data['Price_Volatility'] = (data['High'] - data['Low']) / data['Low']
                data.dropna(inplace=True)
                st.write("Engineered Features Preview:")
                st.dataframe(data[['Close', 'MA_5', 'MA_10', 'Price_Volatility', 'Target']].head(10))

            # Model Training
            with tabs[1]:
                st.subheader("🧠 Model Training")
                features = ['Open', 'High', 'Low', 'Volume', 'MA_5', 'MA_10', 'Price_Volatility']
                X = data[features]
                y = data['Target']

                # Splitting Data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size / 100, random_state=42)

                # Scaling
                scaler = StandardScaler()
                X_train = scaler.fit_transform(X_train)
                X_test = scaler.transform(X_test)

                # Training Model
                rf_model = RandomForestClassifier(random_state=42, n_estimators=100)
                rf_model.fit(X_train, y_train)

                st.success("Model Trained Successfully!")

            # Performance Metrics
            with tabs[2]:
                st.subheader("📈 Performance Metrics")
                y_pred = rf_model.predict(X_test)

                # Metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)

                col1, col2, col3 = st.columns(3)
                col1.metric("**Accuracy**", f"{accuracy:.2f}", delta=f"{accuracy - 1:.2f}")
                col2.metric("**Precision**", f"{precision:.2f}")
                col3.metric("**Recall**", f"{recall:.2f}")

                st.markdown("**Classification Report:**")
                st.text(classification_report(y_test, y_pred))

            # Visualizations
            with tabs[3]:
                st.subheader("📊 Visualizations")

                # Confusion Matrix with Plotly for interactivity
                st.markdown("### Confusion Matrix")
                conf_matrix = confusion_matrix(y_test, y_pred)

                fig = go.Figure(data=go.Heatmap(
                    z=conf_matrix,
                    x=['Down', 'Up'],
                    y=['Down', 'Up'],
                    colorscale='Cividis',  # Cividis color scale for better distinction
                    colorbar=dict(title='Count'),
                    showscale=True
                ))

                fig.update_layout(
                    title="Confusion Matrix",
                    xaxis_title="Predicted",
                    yaxis_title="Actual",
                    xaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Down', 'Up']),
                    yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Down', 'Up']),
                    height=500,
                    template="plotly_dark",
                    margin=dict(t=50, b=50, l=50, r=50)
                )
                st.plotly_chart(fig)

                # Feature Importance with Plotly
                st.markdown("### Feature Importances")

                feature_importances = pd.DataFrame({
                    'Feature': features,
                    'Importance': rf_model.feature_importances_
                }).sort_values(by='Importance', ascending=False)

                st.write("Feature Importance Overview:")
                st.dataframe(feature_importances)

                # Interactive Bar Chart for Feature Importance
                fig = go.Figure(data=[
                    go.Bar(
                        x=feature_importances['Feature'],
                        y=feature_importances['Importance'],
                        marker_color='rgba(30, 144, 255, 0.7)',
                        text=feature_importances['Importance'].round(2),
                        textposition='auto'
                    )
                ])

                fig.update_layout(
                    title="Feature Importance",
                    xaxis_title="Feature",
                    yaxis_title="Importance",
                    xaxis_tickangle=-45,
                    template="plotly_dark",
                    height=400
                )

                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
