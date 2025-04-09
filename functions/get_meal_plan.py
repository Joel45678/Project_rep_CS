import requests #pip install requests for api requests
#This functions is used to get random meal plans with the imputs form the user 

def get_meal_plan(API_KEY, timeFrame="day", diet=None, intolerances=None, exclude=None, number=None, type="main course"):
    
    # Meal Planer
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

    # Research recipes by meal type
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "type": type,  # z.B. "breakfast", "lunch", "dinner"
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
        meals = data["meals"]
        """print("\n📝 Meal Plan:")
        for meal in meals:
            print(f"- {meal['title']} (ID: {meal['id']})")"""

        #return [meal["id"] for meal in meals] #ids der Rezepte werden zurückgegeben
        return meals