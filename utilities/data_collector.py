# Speicherung der Trainingsdaten
import pandas as pd
import os
from random_user_generator import generate_random_preferences
#from ..functions.get_meal_plan import get_meal_plan
from constants import API_KEY2
#from ..functions.get_recipe_information import get_recipe_price

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.get_meal_plan import get_meal_plan
from functions.get_recipe_information import get_recipe_price


def generate_data():
    random_preferences = generate_random_preferences()
    #generate data
    for i in range(3):
        dish, food_type = get_meal_plan(API_KEY2, "day", random_preferences[0], random_preferences[1], random_preferences[2])
        if dish == 402: #check if daily limit is exceeded
            break
        price = get_recipe_price(API_KEY2, dish[0]["id"])
        save_training_example(dish[0]["id"], random_preferences[0], random_preferences[1], random_preferences[2], food_type, price)
        random_preferences = generate_random_preferences()
        

# to get paths 
import pandas as pd
import os

# Basisverzeichnis
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.csv")

def save_training_example(id, diet, intolerances, excluded_ingredients, food_type, cost, path=DATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # does 'data' exist

    new_data = pd.DataFrame([{
        "food_id": id,
        "diet": diet or "none",
        "intolerances": intolerances or "none",
        "excluded_ingredients": excluded_ingredients or "none",
        "food_type" : food_type,
        "meal_costs": cost
    }])

    if os.path.exists(path): #check if .csv does exist
        old_data = pd.read_csv(path)
        df = pd.concat([old_data, new_data], ignore_index=True)
    else: #create file if it does not exist
        df = new_data

    df.to_csv(path, index=False) # insert into .csv

generate_data()