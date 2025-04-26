import requests #pip install requests for api requests
#This functions is used to get random meal plans with the imputs form the user 


import requests
import random

def get_meal_plan(API_KEY, timeFrame="day", diet=None, intolerances=None, exclude=None, number=1, food_type="main course"):
    # API-Call for recipes by meal type
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "type": food_type,
        "diet": diet,
        "intolerances": intolerances,
        "excludeIngredients": exclude,
        "number": 100, # necessary because we need to use complexSearch instead of https://api.spoonacular.com/recipes/random
        "addRecipeInformation": True
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        if data["code"] == 402:
            return 402
    except:
        meals = data.get("results", [])

        # select random
        
        if len(meals) < number:
            return meals, food_type  

        selected_meals = random.sample(meals, number)
        return selected_meals, food_type


"""
def get_meal_plan(API_KEY, timeFrame="day", diet=None, intolerances=None, exclude=None, number=1, food_type="main course"):
    
    # API-Call for Meal Planer (optional)
    
    url = "https://api.spoonacular.com/mealplanner/generate"
    params = {
        "apiKey": API_KEY,
        "timeFrame": timeFrame, #day/week - maybe not necessary - instead number ?
        "diet": diet,
        "exclude": exclude,
        "allergies": intolerances,
        "number": number
        #"targetCalories": 10000  # Optional: Kalorienziel
    }

    # API-Call for recipes by meal type
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "type": food_type,
        # type options: main coruse, bread, marinade, side dish, dessert, appetizer, salad, bread, breakfast, soup, beverage, sauce, marinade, fingerfood, snack, drink
        "diet": diet,
        "intolerances": intolerances,
        "excludeIngredients": exclude,
        "number": number,
        "addRecipeInformation": True  # Gibt mehr Infos zurück, z. B. Nährwerte
    }

    response = requests.get(url, params=params)
    data = response.json()
    try: #if request is successful, no code is returned -> try/except can catch error
        if data["code"] == 402: #check if daliy free limit is reached
            return 402
    except:
        meals = data["results"]
        return meals, food_type"""