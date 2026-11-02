import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("smart-canteen/data/canteen_data.csv")

meal_summary = df.groupby("meal_type").agg({
    "prepared_quantity": "sum",
    "sold_quantity": "sum",
    "leftover_quantity": "sum"
})

meal_summary["waste_percentage"] = (
    meal_summary["leftover_quantity"] /
    meal_summary["prepared_quantity"]
) * 100

print("\nMeal-wise Waste Analysis:")
print(meal_summary.round(2))

plt.figure(figsize=(9, 5))
plt.bar(
    meal_summary.index,
    meal_summary["waste_percentage"]
)

plt.title("Meal-wise Food Waste Percentage")
plt.xlabel("Meal Type")
plt.ylabel("Waste Percentage (%)")
plt.tight_layout()

plt.savefig(
    "smart-canteen/visualizations/meal_analysis.png",
    dpi=300
)
plt.show()

print("\nMeal analysis chart saved successfully!")
