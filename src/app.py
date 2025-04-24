import joblib
import pandas as pd
import streamlit as st
import sys, os
import requests

# Load the pre-trained machine learning model for meal cost prediction
# The file 'kosten_forecast_model.pkl' was created by running ml_trial.py
model = joblib.load("../data/kosten_forecast_model.pkl")

# assure imports still work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.constants import intolerances_lst, diet_lst, excluded_ingredients_lst, API_KEY01
from recipe_api.get_meal_plan import get_meal_plan
from recipe_api.get_recipe_information import get_recipe_price, get_recipe_details


# ─── Callbacks ────────────────────────────────────────────────────────────────

def generate_plan():
    """Fetch N recipes and stash them in session_state, with error handling."""
    # 1) Grab & normalize inputs:
    amt   = st.session_state.number_input
    diet  = st.session_state.diet
    intl  = st.session_state.intolerances
    excl  = st.session_state.excluded_ingredients

    # convert the literal "none" back to None
    diet = None if diet == "none" else diet
    intl = None if intl == "none" else intl
    excl = None if excl == "none" else excl

    # 2) Call meal-plan API
    result = get_meal_plan(
        API_KEY01,
        "day",
        diet,
        intl,
        excl,
        amt
    )

    # 3) If it returned an int, treat that as an error code
    if isinstance(result, int):
        if result == 402:
            st.error("Daily recipe limit exceeded – try again tomorrow.")
        else:
            st.error(f"Error fetching meal plan (code {result}).")
        return

    # 4) Otherwise unpack normally
    recipe_ids, _ = result

    # 5) Reset 
    st.session_state.recipes     = []
    st.session_state.total_cost  = 0.0

    for rid in recipe_ids:
        rec_id = rid["id"]
        title, img, instr = get_recipe_details(API_KEY01, rec_id)
        cost               = get_recipe_price(API_KEY01, rec_id)
        st.session_state.total_cost += cost

        st.session_state.recipes.append({
            "id":           rec_id,
            "title":        title,
            "image":        img,
            "instructions": instr,
            "price":        cost,
        })




def regenerate_one(idx):
    """Fetch a truly random recipe (excluding any already in the plan)
    and slot it into position `idx`."""
    # 1) user’s filters
    diet = st.session_state.diet
    intl = st.session_state.intolerances
    excl = st.session_state.excluded_ingredients

    diet = None if diet == "none" else diet
    intl = None if intl == "none" else intl
    excl = None if excl == "none" else excl

    # 2) Build params for /recipes/random
    params = {"apiKey": API_KEY01, "number": 1}
    if diet:
        params["tags"] = diet
    if intl:
        params["intolerances"] = intl
    if excl:
        params["excludeIngredients"] = excl

    # 3) Gather the ID
    existing_ids = [r["id"] for r in st.session_state.recipes]

    # 4) non-duplicate recipe
    new_rec = None
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
        if candidate["id"] not in existing_ids:
            new_rec = candidate
            break

    if new_rec is None:
        st.error("Couldn’t find a new recipe after several tries. Try again later.")
        return

    # 5) Unpack the new recipe
    new_id    = new_rec["id"]
    title     = new_rec.get("title", "")
    image_url = new_rec.get("image", "")
    instr     = new_rec.get("instructions", "") or ""

    # 6) Get cost
    cost = get_recipe_price(API_KEY01, new_id)

    # 7) Update total_cost in session_state
    old_price = st.session_state.recipes[idx]["price"]
    st.session_state.total_cost = st.session_state.total_cost - old_price + cost

    # 8) Overwrite 
    st.session_state.recipes[idx] = {
        "id":           new_id,
        "title":        title,
        "image":        image_url,
        "instructions": instr,
        "price":        cost,
    }



# ─── Layout ───────────────────────────────────────────────────────────────────

# header/logo
col1h, col2h = st.columns(2)
with col1h:
    st.image("src/assets/01_Logo.png", width=200)
with col2h:
    st.empty()

# number-input column
col1s = st.columns(1)
with col1s[0]:
    st.header("Desired amount of meals")
    st.number_input(
        "choose the amount of recipies that you prefear",
        min_value=1,
        step=1,
        key="number_input",
    )

# filters & generate button
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Intolerances")
    st.selectbox("Intolerances", intolerances_lst, key="intolerances")
    st.divider()
    st.button("Generate Meal Plan", on_click=generate_plan)

with col2:
    st.header("Diet")
    st.selectbox("Diet", diet_lst, key="diet")
    st.divider()
    st.header("Your meal plan for the next week")

with col3:
    st.header("Ingredients")
    st.selectbox("Exclude ingredients", excluded_ingredients_lst, key="excluded_ingredients")
    st.divider()
    st.header("4‑week budget forecast")
    st.write("Coming soon!")

# placeholders for cost & titles
titles_placeholder = st.empty()
price_placeholder  = st.empty()


# ─── Always‑run display block ─────────────────────────────────────────────────

if "recipes" in st.session_state:
    # show total cost
    price_placeholder.markdown(
        f"**Price for the plan:** {st.session_state.total_cost:.2f}$"
    )

    # render each recipe + its regenerate button
    for idx, r in enumerate(st.session_state.recipes):
        st.markdown(f"### {r['title']}")
        st.write(f"Price: {r['price']:.2f}$")
        if r["image"]:
            st.image(r["image"], width=250)
        st.markdown("**Instructions:**")
        st.write(r["instructions"] or "No instructions provided.")
        st.markdown("___")

        st.button(
            "Regenerate this recipe",
            key=f"regen_{idx}",
            on_click=regenerate_one,
            args=(idx,),
        )
