import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("smart-canteen/data/canteen_data.csv")

# Calculate food-wise totals
summary = df.groupby("food_item").agg({
    "prepared_quantity": "sum",
    "leftover_quantity": "sum"
})

# Calculate waste percentage
summary["waste_percentage"] = (
    summary["leftover_quantity"] /
    summary["prepared_quantity"]
) * 100

# Sort from highest to lowest waste
summary = summary.sort_values(
    by="waste_percentage", ascending=False
)

# Display results
print("\nFood-wise Waste Analysis:")
print(summary.round(2))

# Create chart
plt.figure(figsize=(12, 6))
plt.bar(
    summary.index,
    summary["waste_percentage"]
)

plt.title("Food-wise Waste Percentage Analysis")
plt.xlabel("Food Item")
plt.ylabel("Waste Percentage (%)")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig(
    "smart-canteen/visualizations/waste_analysis.png",
    dpi=300
)
plt.show()

print("\nWaste analysis chart saved successfully!")
