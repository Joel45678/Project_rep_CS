import requests #pip install requests for api requests
#This functions is used to get random meal plans with the imputs form the user 

def get_meal_plan(API_KEY, timeFrame='day', diet=None, exclude=None, intolerances=None):
    url = "https://api.spoonacular.com/mealplanner/generate"
    params = {
        "apiKey": API_KEY,
        "timeFrame": timeFrame, #day/week
        "diet": diet,
        "exclude": exclude,
        "allergies": intolerances,
        #"targetCalories": 10000  # Optional: Kalorienziel
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