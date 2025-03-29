import requests #pip install requests for api requests
#This functions is used to get random meal plans with the imputs form the user 

def get_meal_plan(API_KEY, timeFrame='day', diet=None, exclude=None, allergies=None):
    url = "https://api.spoonacular.com/mealplanner/generate"
    params = {
        "apiKey": API_KEY,
        "timeFrame": timeFrame,
        "diet": diet,
        "exclude": exclude,
        "allergies": allergies,
        #"targetCalories": 10000  # Optional: Kalorienziel
    }

    response = requests.get(url, params=params)
    data = response.json()

    meals = data["meals"]
    """print("\n📝 Meal Plan:")
    for meal in meals:
        print(f"- {meal['title']} (ID: {meal['id']})")"""

    #return [meal["id"] for meal in meals]
    return [meals]