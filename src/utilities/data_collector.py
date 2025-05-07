# Speicherung der Trainingsdaten
import json
import pandas as pd
import os
from random_user_generator import generate_random_preferences
from constants import API_KEY1

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recipe_api.get_meal_plan import get_meal_plan
from recipe_api.get_recipe_information import get_recipe_price
from recipe_api.get_recipe_information import get_recipe_nutrition
from recipe_api.recipe_data import RecipeData #Recipe object
API_KEY = API_KEY1

# !!! Datengenerierung der CSV erst ab dem Eintrag 1288 brauchbar, zuvor noch fehlerhaft !!!

# tree-model for ML!!!!
"""
def generate_data():
    random_preferences = generate_random_preferences() # create random preferences - retruns tubel: (diet, intolerance, exclude)

    # generate data
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

# to get paths """
import pandas as pd
import os

# Basisverzeichnis
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data_nutrition.csv")

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


### GPT Vorschlag ###


import requests

def get_meal_plan_v2(api_key, diet=None, targetCalories=None, timeFrame="day"):
    url = "https://api.spoonacular.com/mealplanner/generate"
    params = {
        "apiKey": api_key,
        "timeFrame": timeFrame,
        "diet": diet,
    }
    if targetCalories:
        params["targetCalories"] = targetCalories

    response = requests.get(url, params=params)
    data = response.json()

    # Fehlerbehandlung
    if "meals" not in data:
        if data.get("code") == 402:
            return 402
        return None

    return data["meals"]

def generate_data_v2():
    for i in range(20):  # jeder Call = 3 Rezepte, also effektiv 60 potenzielle Rezepte
        print(f"Call {i+1}")
        try:
            preferences = generate_random_preferences()
            meals = get_meal_plan_v2(API_KEY, diet=preferences[0])  # nur diet, da /mealplanner nicht alles unterstützt
            if meals == 402:
                print("Tageslimit erreicht")
                break
            if not meals:
                print("Keine Rezepte erhalten, überspringe")
                continue

            for meal in meals:
                try:
                    recipe = RecipeData(
                        food_id=meal["id"],
                        servings=1,  # mealplanner gibt keine servings zurück, ggf. später per get_recipe_information holen
                        actual_diets=[],  # können per Detail-Call ergänzt werden
                        diet=preferences[0],
                        intolerances=preferences[1],
                        excluded_ingredients=preferences[2],
                        food_type=meal.get("dishTypes", ["main course"])[0] if "dishTypes" in meal else "main course",
                        cost=get_recipe_price(API_KEY, meal["id"])
                    )
                    recipe.nutrition = get_recipe_nutrition(API_KEY, meal["id"])
                    save_training_example(recipe)
                except Exception as e:
                    print(f"Fehler bei Rezept-ID {meal['id']}: {e}")
                    continue
        except Exception as e:
            print("Fehler im API-Call:", e)
            continue
    print("Data collection finished (v2)")
generate_data_v2()
