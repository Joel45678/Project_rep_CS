import requests #pip install requests for api requests


def get_recipe_price(API_KEY,recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}

    #api request
    response = requests.get(url, params=params)
    data = response.json() #convert response to json

    #get price information
    servings = data.get("servings", 1) #necessary (?)
    price_per_serving = data.get("pricePerServing", 0) / 100  # von Cents in Dollar (?)

    #calculate total price
    total_price = price_per_serving * servings
    return total_price