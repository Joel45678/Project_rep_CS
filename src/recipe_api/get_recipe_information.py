import requests #pip install requests for api requests

# calculate the price of the recipe
def get_recipe_price(API_KEY,recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}

    #api request
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"[Fehler] Rezeptpreis konnte nicht geladen werden – Statuscode: {response.status_code}")

    data = response.json() #convert response to json

    #get price information
    servings = data.get("servings", 1) #necessary (?)
    price_per_serving = data.get("pricePerServing", 0) / 100  # Cents to Dollar 

    #calculate total price
    #total_price = price_per_serving * servings 
    return price_per_serving

# get additional information about the recipe
def get_recipe_details(API_KEY, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}

    response = requests.get(url, params=params)
    data = response.json()

    title = data.get("title", "No title")
    image = data.get("image", "")
    instructions = data.get("instructions", "No instructions provided.")

    return title, image, instructions


def get_recipe_nutrition(API_KEY, recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {"apiKey": API_KEY}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "calories": data.get("calories", ""),
            "carbs": data.get("carbs", ""),
            "fat": data.get("fat", ""),
            "protein": data.get("protein", "")
        }
    else:
        print(f"[Fehler] Nährwerte konnten nicht geladen werden - Statuscode: {response.status_code}")
        return {
            "calories": "",
            "carbs": "",
            "fat": "",
            "protein": ""
        }

def get_recipe_grams(value):
    if isinstance(value, str):
        return float(value.replace("g", "").strip())
    return float(value)