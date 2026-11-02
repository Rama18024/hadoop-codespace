import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path
st.set_page_config(
    page_title="Smart Canteen Dashboard",
    page_icon="🍽️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "canteen_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()
@st.cache_resource(show_spinner="Training Random Forest model...")
def train_demand_model():
    data = df.copy()

    data["month"] = data["date"].dt.month
    data["day_of_week"] = data["date"].dt.day_of_week

    features = [
        "food_item",
        "meal_type",
        "month",
        "day_of_week",
        "prepared_quantity"
    ]

    X = data[features]
    y = data["sold_quantity"]

    categorical_features = ["food_item", "meal_type"]
    numerical_features = [
        "month",
        "day_of_week",
        "prepared_quantity"
    ]

    preprocessor = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"),
         categorical_features),
        ("numerical", "passthrough", numerical_features)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        ))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, predictions),
        "RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
        "R2": r2_score(y_test, predictions)
    }

    return model, metrics

st.sidebar.title("🍽️ Smart Canteen")
st.sidebar.caption("Food Waste Prediction and Analysis")

page = st.sidebar.radio(
    "Navigate",
    ["Project Overview", "Food Analysis", "Waste Analysis", "Meal Analysis", "Demand Prediction"]
)

if page == "Project Overview":
    st.title("🍽️ Smart Canteen")
    st.subheader("Food Waste Prediction and Analysis")
    st.write("Big Data Analytics Mini Project using Hadoop, MapReduce, Hive and Python.")

    st.info("Academic demonstration using a synthetic canteen dataset.")

    total_records = len(df)
    total_prepared = df["prepared_quantity"].sum()
    total_sold = df["sold_quantity"].sum()
    total_leftover = df["leftover_quantity"].sum()
    waste_percentage = total_leftover / total_prepared * 100

    st.subheader("Dataset Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", f"{total_records:,}")
    c2.metric("Prepared", f"{total_prepared:,}")
    c3.metric("Sold", f"{total_sold:,}")
    c4.metric("Leftover", f"{total_leftover:,}")

    st.metric("Overall Waste Percentage", f"{waste_percentage:.2f}%")
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

elif page == "Food Analysis":
    st.title("Food-wise Analysis")
    summary = df.groupby("food_item")[
        ["prepared_quantity", "sold_quantity", "leftover_quantity"]
    ].sum()
    st.subheader("Prepared vs Sold Quantity")
    st.bar_chart(summary[["prepared_quantity", "sold_quantity"]])
    st.dataframe(summary, use_container_width=True)

elif page == "Waste Analysis":
    st.title("Food Waste Analysis")
    summary = df.groupby("food_item")[
        ["prepared_quantity", "leftover_quantity"]
    ].sum()
    summary["waste_percentage"] = (
        summary["leftover_quantity"] / summary["prepared_quantity"] * 100
    )
    summary = summary.sort_values("waste_percentage", ascending=False)
    st.bar_chart(summary["waste_percentage"])
    st.dataframe(summary, use_container_width=True)
    st.warning(f"Highest waste percentage: {summary.index[0]}")
    st.success(f"Lowest waste percentage: {summary.index[-1]}")

elif page == "Meal Analysis":
    st.title("Meal-wise Analysis")
    summary = df.groupby("meal_type")[
        ["prepared_quantity", "sold_quantity", "leftover_quantity"]
    ].sum()
    summary["waste_percentage"] = (
        summary["leftover_quantity"] / summary["prepared_quantity"] * 100
    )
    st.bar_chart(summary["waste_percentage"])
    st.dataframe(summary, use_container_width=True)
elif page == "Demand Prediction":
    st.title("Food Sales Prediction")
    st.write("Estimate how many portions of a food item will be sold.")

    model, metrics = train_demand_model()

    food_item = st.selectbox(
        "Select Food Item",
        sorted(df["food_item"].unique())
    )

    meal_type = st.selectbox(
        "Select Meal Type",
        sorted(df["meal_type"].unique())
    )

    month = st.selectbox(
        "Select Month",
        list(range(1, 13))
    )

    weekdays = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    day = st.selectbox("Select Day", list(weekdays.keys()))

    prepared_quantity = st.number_input(
        "Planned Preparation Quantity",
        min_value=1,
        max_value=10000,
        value=100
    )

    if st.button("Predict Food Sales"):
        input_data = pd.DataFrame([{
            "food_item": food_item,
            "meal_type": meal_type,
            "month": month,
            "day_of_week": weekdays[day],
            "prepared_quantity": prepared_quantity
        }])

        predicted_sold = model.predict(input_data)[0]
        predicted_sold = max(
            0, min(predicted_sold, prepared_quantity)
        )

        predicted_leftover = prepared_quantity - predicted_sold

        st.success("Prediction completed!")

        col1, col2 = st.columns(2)

        col1.metric("Predicted Sold Quantity", f"{predicted_sold:.0f}")
        col2.metric("Predicted Leftover", f"{predicted_leftover:.0f}")

    st.subheader("Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", f"{metrics['MAE']:.2f}")
    col2.metric("RMSE", f"{metrics['RMSE']:.2f}")
    col3.metric("R² Score", f"{metrics['R2']:.4f}")
    
