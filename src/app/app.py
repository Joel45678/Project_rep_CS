import streamlit as st
import sys, os
import requests

import os




# assure imports still work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recipe_api.get_recipe_information import get_recipe_price, get_recipe_details, get_recipe_nutrition
from utilities.constants import intolerances_lst, diet_lst, excluded_ingredients_lst, API_KEY1
from recipe_api.get_meal_plan import get_meal_plan
from recipe_api.get_recipe_information import get_recipe_price, get_recipe_details, get_recipe_grams
#from data.ml_forecast import train_and_forecast_model
from data.ml_forecast import forecast_user_constraints




import plotly.graph_objects as go

if 'total_carbs' not in st.session_state:
    st.session_state.total_carbs = 0.0
if 'total_fat' not in st.session_state:
    st.session_state.total_fat = 0.0
if 'total_protein' not in st.session_state:
    st.session_state.total_protein = 0.0
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0.0
if 'recipes' not in st.session_state:
    st.session_state.recipes = []
if 'number_input' not in st.session_state:
    st.session_state.number_input = 1  # default 1 meal if not set

API_KEY = API_KEY1

def generate_plan():

    #use inputs from session state
    input_number    = st.session_state.number_input
    diet            = st.session_state.diet
    intolerances    = st.session_state.intolerances
    excluded_ingredients  = st.session_state.excluded_ingredients

    # convert the literal "none" to None-Value
    if diet == "none":
        diet = None
    if intolerances == "none":
        intolerances = None
    if excluded_ingredients == "none":
        diet = None

    #API-Call to get recipe
    try:
        recipes, food_type = get_meal_plan(
            API_KEY,
            "day",
            diet,
            intolerances,
            excluded_ingredients,
            input_number
        )
    except:
        recipes = get_meal_plan(
            API_KEY,
            "day",
            diet,
            intolerances,
            excluded_ingredients,
            input_number
        )
        #Check for API response (int is always an error code - correct call returns a list)
        if isinstance(recipes, int):
            if recipes == 402:
                st.error("Daily recipe limit exceeded - Sorry.  You can try again tomorrow :)")
            else:
                st.error(f"API-Call Error: {recipes}.")
            return

    st.session_state.recipes = []
    st.session_state.total_cost = 0.0
    st.session_state.total_carbs = 0.0
    st.session_state.total_protein = 0.0
    st.session_state.total_fat = 0.0

    #go through recipes to create the output for each recipe
    for rid in recipes:
        rec_id = rid["id"]
        title, img, instr = get_recipe_details(API_KEY, rec_id)   # instructions for recipe
        cost = get_recipe_price(API_KEY, rec_id)                  # calculate costs for recipe
        nutrition = get_recipe_nutrition(API_KEY, rec_id)         # get ingredients

        carbs = get_recipe_grams(nutrition.get("carbs", 0))
        fat = get_recipe_grams(nutrition.get("fat", 0))
        protein = get_recipe_grams(nutrition.get("protein", 0))
        
        st.write(f"Recipe: {title}, Carbs: {carbs}, Fat: {fat}, Protein: {protein}")

        st.session_state.total_carbs += carbs
        st.session_state.total_fat += fat
        st.session_state.total_protein += protein
        st.session_state.total_cost += cost

        st.session_state.recipes.append({
            "id":           rec_id,
            "title":        title,
            "image":        img,
            "instructions": instr,
            "price":        cost,
        })

#regenerate meal, if user doesn't like the meal
def regenerate_one(id_regenerate):

    #inputs
    diet = st.session_state.diet
    intolerances = st.session_state.intolerances
    excluded_ingredients = st.session_state.excluded_ingredients

    # convert values
    if diet == "none":
        diet = None
    if intolerances == "none":
        intolerances = None
    if excluded_ingredients == "none":
        excluded_ingredients = None

    # Build params for /recipes/random
    params = {"apiKey": API_KEY, "number": 1}
    if diet:
        params["tags"] = diet
    if intolerances:
        params["intolerances"] = intolerances
    if excluded_ingredients:
        params["excludeIngredients"] = excluded_ingredients

    #ID for current recipes
    currents_recipe_id = [r["id"] for r in st.session_state.recipes]

    # 4) non-duplicate recipe
    new_recipe = None
    for _ in range(5):
        resp = requests.get("https://api.spoonacular.com/recipes/random", params=params)
        if resp.status_code != 200:
            st.error(f"Error fetching random recipe: {resp.status_code}")
            return

        data = resp.json()
        candidates = data.get("recipes", [])
        if not candidates:
            st.error("No recipes returned from API.")
            return

        candidate = candidates[0]
        if candidate["id"] not in currents_recipe_id:
            new_recipe = candidate
            break

    if new_recipe is None:
        st.error("Couldn’t find a new recipe after several tries. Try again later.")
        return

    #extract values for the new recipe
    new_id    = new_recipe["id"]
    title     = new_recipe.get("title", "")
    image_url = new_recipe.get("image", "")
    instr     = new_recipe.get("instructions", "") or ""

    #price for recipe and update of current sum
    cost = get_recipe_price(API_KEY, new_id)
    old_price = st.session_state.recipes[id_regenerate]["price"]
    st.session_state.total_cost = st.session_state.total_cost - old_price + cost

    #Insert new recipe
    st.session_state.recipes[id_regenerate] = {
        "id":           new_id,
        "title":        title,
        "image":        image_url,
        "instructions": instr,
        "price":        cost,
    }



# Structure of the app


# number-input column (input)
# Sidebar Input
with st.sidebar:
    #st.image("src/assets/01_Logo.png", width=150)
    #st.header("Meal Plan Configuration")

    st.number_input(
        label="Number of recipes",
        min_value=1,
        step=1,
        format="%d",
        key="number_input"
    )

    st.selectbox("Diet", diet_lst, key="diet")
    st.selectbox("Intolerances", intolerances_lst, key="intolerances")
    st.selectbox("Exclude ingredients", excluded_ingredients_lst, key="excluded_ingredients")

    st.markdown("<br>", unsafe_allow_html= True)

    st.button("Generate Meal Plan", on_click=generate_plan)

    # Button zum Trainieren des Modells und Anzeigen des Forecasts
    if st.button("ML Forecast anzeigen"):
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data_nutrition.csv')
        csv_path = os.path.abspath(csv_path)

        pred_cost = forecast_user_constraints(
            csv_path,
            diet=st.session_state.diet if st.session_state.diet != "none" else None,
            intolerance=st.session_state.intolerances if st.session_state.intolerances != "none" else None,
            excluded_ingredient=st.session_state.excluded_ingredients if st.session_state.excluded_ingredients != "none" else None
        )

        st.markdown(f"**Vorhergesagte Kosten basierend auf deinen Angaben:** {pred_cost:.2f} €")



# Chart and meals with instructions
col1f =st.columns(1)[0]
with col1f:
    # Forecast-Anzeige, falls vorhanden
    if "forecast_avg" in st.session_state:
        st.markdown(f"**Durchschnittlich vorhergesagte Kosten pro Portion (ML):** {st.session_state.forecast_avg:.2f} €")

    titles_placeholder = st.empty()  # placeholder for recipes
    price_placeholder = st.empty()   # placeholder for price

    total_carbs = st.session_state.get("total_carbs", 0.0)
    total_fat = st.session_state.get("total_fat", 0.0)
    total_protein = st.session_state.get("total_protein", 0.0)
    total_cost = st.session_state.get("total_cost", 0.0)
    recipes = st.session_state.get("recipes", [])

    # Ensure we have valid values for the variables
    selected_amount = st.session_state.get("number_input", 1)
    if (
        recipes and
        total_carbs != 0.0 and
        total_fat != 0.0 and
        total_protein != 0.0 and
        total_cost != 0.0 and
        selected_amount > 0
    ):
        # calculate averages
        average_carbs = round(total_carbs / selected_amount, 2)
        average_fat = round(total_fat / selected_amount, 2)
        average_protein = round(total_protein / selected_amount, 2)

        macronutrients = ["Protein", "Fat", "Carbs"]
        values = [average_protein, average_fat, average_carbs]

        # figure to show nutrient
        bar_fig = go.Figure([go.Bar(x=macronutrients, y=values, text=values, textposition='auto')])
        bar_fig.update_layout(
            title="Average Macronutrient Breakdown per Meal",
            xaxis_title="Macronutrients",
            yaxis_title="Grams",
            template="plotly_white",
            yaxis=dict(tickformat=',d')
        )
        st.plotly_chart(bar_fig)

        # !! currently on the top !!!!
        price_placeholder.markdown(
            f"**Price for the plan:** {total_cost:.2f}$"
        )

        # show generated recipes on the page
        for idx, r in enumerate(recipes):
            st.markdown(f"### {r['title']}")
            st.write(f"Price: {r['price']:.2f}$")
            if r["image"]:
                st.image(r["image"], width=250)
            st.markdown("**Instructions:**")
            st.write(r["instructions"] or "No instructions provided.", unsafe_allow_html=True)
            
            st.button(
                "Regenerate this recipe",
                key=f"regen_{idx}",
                on_click=regenerate_one,
                args=(idx,),
            )
            if st.button(f"View Macronutrients for {r['title']}", key=f"macro_{idx}"):
                st.query_params.update(recipe_id=r['id'], recipe_title=r['title'])
                st.switch_page("pages/macronutrients_page.py")

            st.markdown("___")
        
    else:
        st.info("Generate a meal plan to see your recipes and breakdown.")
       
