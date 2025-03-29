import requests #pip install requests for api requests


def get_recipe_price(API_KEY,recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}

    response = requests.get(url, params=params)
    data = response.json()

    #title = data.get("title")
    servings = data.get("servings", 1)
    price_per_serving = data.get("pricePerServing", 0) / 100  # von Cents in Dollar (?)

    total_price = price_per_serving * servings
    #print(f"{title}: {price_per_serving:.2f}$ pro Portion × {servings} = {total_price:.2f}$ gesamt")
    return total_price