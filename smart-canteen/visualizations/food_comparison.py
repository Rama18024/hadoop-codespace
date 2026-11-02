import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("smart-canteen/data/canteen_data.csv")

# Calculate food-wise totals
food_summary = df.groupby("food_item")[
    ["prepared_quantity", "sold_quantity"]
].sum()

# Plot comparison
food_summary.plot(kind="bar", figsize=(12, 6))

plt.title("Food-wise Prepared Quantity vs Sold Quantity")
plt.xlabel("Food Item")
plt.ylabel("Total Quantity")
plt.xticks(rotation=45)
plt.legend(["Prepared Quantity", "Sold Quantity"])
plt.tight_layout()

# Save chart
plt.savefig("smart-canteen/visualizations/food_comparison.png", dpi=300)
plt.show()

print("\nFood-wise summary:")
print(food_summary)
print("\nChart saved successfully!")
