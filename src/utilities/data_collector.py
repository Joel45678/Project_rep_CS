# Speicherung der Trainingsdaten
import json
import pandas as pd
import os
from random_user_generator import generate_random_preferences
from constants import API_KEY2

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recipe_api.get_meal_plan import get_meal_plan
from recipe_api.get_recipe_information import get_recipe_price
from recipe_api.get_recipe_information import get_recipe_nutrition
from recipe_api.recipe_data import RecipeData #Recipe object
API_KEY = API_KEY2


# to get paths 
import pandas as pd
import os

# Basisverzeichnis
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data_nutrition.csv")

# save training data in a .csv
def save_training_example(recipe: RecipeData, path=DATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # does 'training_data' exist

    # create data frame to save the data in a table

    new_data = pd.DataFrame([{
        "food_id": recipe.food_id,
        "diet": recipe.diet,
        "intolerances": recipe.intolerances,
        "excluded_ingredients": recipe.excluded_ingredients,
        "food_type" : recipe.food_type,
        "meal_costs_perserving": recipe.cost,
        "servings": recipe.servings,
        "all_diets": json.dumps(recipe.actual_diets),
        "calories": recipe.nutrition.get("calories", ""),
        "carbs": recipe.nutrition.get("carbs", ""),
        "fat": recipe.nutrition.get("fat", ""),
        "protein": recipe.nutrition.get("protein", "")
    }])


    if os.path.exists(path): # check if .csv does exist
        old_data = pd.read_csv(path)
        df = pd.concat([old_data, new_data], ignore_index=True)
    else: # create file if it does not exist
        df = new_data

    df.to_csv(path, index=False) # insert data into .csv


# generate random recipes

def generate_data():
    random_preferences = generate_random_preferences() # create random preferences - retruns tubel: (diet, intolerance, exclude)

    # generate data - 50 recipes
    for i in range(50):
        print(i+1)
        # check if daliy limit es exceeded via try-except
        try:        
            dish, food_type = get_meal_plan(API_KEY, "day", *random_preferences)
        except:
            dish = get_meal_plan(API_KEY, "day", *random_preferences)
            if dish == 402:
                print("Tageslimit erreicht")
                break
            print("Unbekannter Fehler")
            break
        try:
            recipe = RecipeData(
                food_id = dish[0]["id"],
                servings = dish[0]["servings"],
                actual_diets = dish[0].get("diets", []),
                diet = random_preferences[0],
                intolerances = random_preferences[1],
                excluded_ingredients = random_preferences[2],
                food_type = food_type,
                cost = get_recipe_price(API_KEY, dish[0]["id"]), 
            )
            recipe.nutrition = get_recipe_nutrition(API_KEY, dish[0]["id"])
            save_training_example(recipe)
            random_preferences = generate_random_preferences() #generate new preferences
        except Exception as e:
            print("Fehler im API-Call:", e)
            break
    print("Data collected")

generate_data()

# remove duplicate valuse
def remove_duplicate_values(path=DATA_PATH):
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = df.drop_duplicates(subset="food_id", keep="first")
        df.to_csv(path, index=False)

#remove_duplicate_values(DATA_PATH)