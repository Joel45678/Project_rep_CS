import streamlit as st

st.set_page_config(
    page_title="Macronutrients"
)
from recipe_api.get_recipe_information import get_recipe_nutrition, get_recipe_grams
from utilities.constants import API_KEY1

API_KEY = API_KEY1

# Retrieve from session states
recipe_id = st.session_state.get("selected_recipe_id")
recipe_title = st.session_state.get("selected_recipe_title")
recipe_image = st.session_state.get("selected_recipe_image")

if recipe_id and recipe_title:
    st.header(f"Macronutrients of {recipe_title}")
    if recipe_image:
        st.image(recipe_image, width=300)

if recipe_id:
    try:
        # Get nutrition data
        nutrition = get_recipe_nutrition(API_KEY, recipe_id)
        carbs = get_recipe_grams(nutrition.get("carbs", 0))
        fat = get_recipe_grams(nutrition.get("fat", 0))
        protein = get_recipe_grams(nutrition.get("protein", 0))

        # Display results
        st.subheader(f"Macronutrients for Recipe ID {recipe_id}")
        st.write(f"**Carbs:** {carbs} g")
        st.write(f"**Fat:** {fat} g")
        st.write(f"**Protein:** {protein} g")
    except Exception as e:
        st.error(f"Failed to fetch nutrition info: {e}")
else:
    st.warning("No recipe selected. Please go back to the main page and select one.")
