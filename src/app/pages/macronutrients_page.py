import streamlit as st
from recipe_api.get_recipe_information import get_recipe_nutrition, get_recipe_grams
from utilities.constants import API_KEY1

API_KEY = API_KEY1

st.title("Recipe Macronutrients")

# Get recipe_id from query parameters
recipe_id = st.query_params.get("recipe_id", [None])[0]

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