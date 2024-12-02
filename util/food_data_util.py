lower_limit = [2000,   0,  0,    0,   0,  25,  50,  5000,    50,  800, 10]
upper_limit = [2250, 300, 65, 2400, 300, 100, 100, 50000, 20000, 1600, 30]

nutrients = ["Calories", "Cholesterol mg", "Fat g", "Sodium mg", "Carbs g", "Fiber g", "Protein g",
            "Vit A", "Vit C", "Calcium mg", "Iron mg" ]

import csv

food_cost = {}
food_serving = {}
foods = []
food_data = {}

with open('food_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        food_name = row.get('Foods', '')
        unit_cost = float(row.get('Price/Serving', 0))
        serving_unit_string = f"{row.get('Serving Size')} {row.get('Unit')}"


        food_nutrient = [row.get('Calories'), row.get('Cholesterol mg'), row.get('Total_Fat g'), 
                     row.get('Sodium mg'),	row.get('Carbohydrates g'),	row.get('Dietary_Fiber g'),	
                     row.get('Protein g'), row.get('Vit_A IU'), row.get('Vit_C IU'), row.get('Calcium mg'), row.get('Iron mg')]

        for i in range(len(food_nutrient)):
            food_nutrient[i] = float(food_nutrient[i])


        foods.append(food_name)
        food_cost[food_name] = unit_cost
        food_serving[food_name] = serving_unit_string
        food_data[food_name] = food_nutrient