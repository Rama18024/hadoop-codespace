import csv
import random
from datetime import date, timedelta

random.seed(42)

food_items = {
    "Idli": (80, 150, "Breakfast"),
    "Dosa": (60, 120, "Breakfast"),
    "Poha": (50, 100, "Breakfast"),
    "Paratha": (60, 120, "Breakfast"),
    "Rice": (100, 250, "Lunch"),
    "Dal": (100, 250, "Lunch"),
    "Paneer": (50, 150, "Lunch"),
    "Chapati": (100, 300, "Lunch"),
    "Biryani": (80, 200, "Dinner"),
    "Pulao": (60, 150, "Dinner"),
    "Noodles": (50, 150, "Dinner"),
    "Sandwich": (40, 100, "Snacks")
}

start_date = date(2025, 1, 1)
number_of_records = 100000

with open("smart-canteen/data/canteen_data.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "date", "food_item", "prepared_quantity",
        "sold_quantity", "leftover_quantity", "meal_type"
    ])

    for i in range(number_of_records):
        current_date = start_date + timedelta(days=random.randint(0, 364))
        food = random.choice(list(food_items.keys()))

        minimum, maximum, meal = food_items[food]
        prepared = random.randint(minimum, maximum)

        # Simulate demand and sales
        demand = int(prepared * random.uniform(0.65, 1.15))
        sold = min(prepared, max(0, demand))
        leftover = prepared - sold

        writer.writerow([
            current_date.isoformat(),
            food,
            prepared,
            sold,
            leftover,
            meal
        ])

print("Dataset generated successfully!")
print("Total records:", number_of_records)
