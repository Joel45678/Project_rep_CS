# Speicherung der Trainingsdaten
import json
import pandas as pd
import os
from random_user_generator import generate_random_preferences
#from ..functions.get_meal_plan import get_meal_plan
from constants import API_KEY1
#from ..functions.get_recipe_information import get_recipe_price

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recipe_api.get_meal_plan import get_meal_plan
from recipe_api.get_recipe_information import get_recipe_price
from recipe_api.get_recipe_information import get_recipe_nutrition

"""!!!!"""
# !!! - !!!
# evtl. sollten die Kalorien mitgespeichert werden, um die Kosten pro Kalorien berechnen zu können und daraus die Prognose ableiten zu können
def generate_data():
    random_preferences = generate_random_preferences() # create random preferences - retruns tubel: (diet, intolerance, exclude)

    # generate 25 sets data
    for i in range(1):
        # check if daliy limit es exceeded via try-except
        try:        
            dish, food_type = get_meal_plan(API_KEY1, "day", random_preferences[0], random_preferences[1], random_preferences[2])
        except:
            dish = get_meal_plan(API_KEY1, "day", random_preferences[0], random_preferences[1], random_preferences[2])
            if dish == 402: # check if daily limit is exceeded
                print("Tageslimit erreicht")
                break
            print("Unbekannter Fehler")
            break
        try:
            price = get_recipe_price(API_KEY1, dish[0]["id"])
            
            actual_diets = dish[0].get("diets", [])
            nutrition = get_recipe_nutrition(API_KEY1, dish[0]["id"]) 

            save_training_example(dish[0]["id"], #call save_Training_example to save meal in a csv
                                random_preferences[0], #diets
                                random_preferences[1], #intolerances
                                random_preferences[2], #excluded
                                food_type,
                                price,
                                actual_diets,
                                nutrition,
                                dish[0]["servings"]
                                )
            random_preferences = generate_random_preferences() #generate new preferences
            time.sleep(0.5) # Sleep for 0.5 seconds, becaus of api-limit
        except:
            print("Fehler im API-Call ")
            break

    print("Data collected")

# to get paths 
import pandas as pd
import os

# Basisverzeichnis
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data_nutrition.csv")

def save_training_example(id, diet, intolerances, excluded_ingredients, food_type, cost, actual_diets, nutrition=None, servings=1, path=DATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # does 'training_data' exist

    # create data frame to save the data in a table
    new_data = pd.DataFrame([{
        "food_id": id,
        "diet": diet or "none",
        "intolerances": intolerances or "none",
        "excluded_ingredients": excluded_ingredients or "none",
        "food_type" : food_type,
        "meal_costs_perserving": cost,
        "servings": servings,
        "all_diets": json.dumps(actual_diets)
    }])
    if nutrition:
        new_data["calories"] = nutrition.get("calories", "")
        new_data["carbs"] = nutrition.get("carbs", "")
        new_data["fat"] = nutrition.get("fat", "")
        new_data["protein"] = nutrition.get("protein", "")
 

    if os.path.exists(path): # check if .csv does exist
        old_data = pd.read_csv(path)
        df = pd.concat([old_data, new_data], ignore_index=True)
    else: # create file if it does not exist
        df = new_data

    df.to_csv(path, index=False) # insert data into .csv

generate_data()