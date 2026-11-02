import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("smart-canteen/data/canteen_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Create date-based features
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.dayofweek

# Select input features and target
X = df[
    ["food_item", "meal_type", "month", "day_of_week",
     "prepared_quantity"]
]

y = df["sold_quantity"]

# Identify categorical and numerical columns
categorical_features = ["food_item", "meal_type"]
numerical_features = [
    "month", "day_of_week", "prepared_quantity"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"),
         categorical_features),
        ("num", "passthrough", numerical_features)
    ]
)

# Create Random Forest model
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ))
])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model.fit(X_train, y_train)

print("Random Forest model trained successfully!")

# Predict test data
y_pred = model.predict(X_test)

# Evaluate model
print("\nModel Evaluation:")
print("MAE:", round(mean_absolute_error(y_test, y_pred), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))
print("R2 Score:", round(r2_score(y_test, y_pred), 4))

# Show sample predictions
results = pd.DataFrame({
    "Actual Sold Quantity": y_test.values[:10],
    "Predicted Sold Quantity": np.round(y_pred[:10], 2)
})

print("\nSample Predictions:")
print(results.to_string(index=False))

# Interactive prediction
print("\n--- Food Demand Prediction ---")

food = input("Enter food item: ").strip().title()
meal = input("Enter meal type: ").strip().title()
month = int(input("Enter month (1-12): "))
day = int(input("Enter day (0=Monday, 6=Sunday): "))
prepared = int(input("Enter prepared quantity: "))

new_data = pd.DataFrame({
    "food_item": [food],
    "meal_type": [meal],
    "month": [month],
    "day_of_week": [day],
    "prepared_quantity": [prepared]
})

prediction = model.predict(new_data)[0]
prediction = max(0, min(prediction, prepared))

print("\nPredicted sold quantity:", round(prediction, 2))
print("Estimated leftover quantity:", round(prepared - prediction, 2))

# Interactive prediction
print("\n--- Food Demand Prediction ---")

food = input("Enter food item: ").strip().title()
meal = input("Enter meal type: ").strip().title()
month = int(input("Enter month (1-12): "))
day = int(input("Enter day (0=Monday, 6=Sunday): "))
prepared = int(input("Enter prepared quantity: "))

new_data = pd.DataFrame({
    "food_item": [food],
    "meal_type": [meal],
    "month": [month],
    "day_of_week": [day],
    "prepared_quantity": [prepared]
})

prediction = model.predict(new_data)[0]
prediction = max(0, min(prediction, prepared))

print("\nPredicted sold quantity:", round(prediction, 2))
print("Estimated leftover quantity:", round(prepared - prediction, 2))
