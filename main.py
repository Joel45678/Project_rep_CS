#link to the app: https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/

import streamlit as st

#import custom functions from folder functions
from functions.get_meal_plan import get_meal_plan
from functions.get_recipe_price import get_recipe_price


#API details for spoonacular.com
API_KEY = "373547e7ea3647b1b17c5abc690d725c"

#page layout
col1, col2, col3 = st.columns(3)
col1b, col2b = st.columns(2)

#List of all eating behaviors
allergies = ["none", "lactose", "gluten"]
diet = ["none", "vegan", "vegetarian", "Pescetarian"]
excluded_ingredients = ["none", "vegan", "vegetarian", "Pescetarian"]

#variables
price = 17.5


#streamlit page

st.title("SmartMeal")
st.subheader("A recipe recommender and meal planner")

with col1:
    st.header("Allergies")
    st.selectbox("Allergies", allergies, key="allergies")
    st.divider()
    st.button("Generate Meal Plan", key="generate_button")

with col2:
    st.header("Diet")
    st.selectbox("Diet", diet, key="Diet")
    st.divider()
    st.header("Your meal plan for the next week")
    st.write(f"Price: {price}")
with col3:
    st.header("Excluded ingredients")
    st.selectbox("Exclude ingredients", excluded_ingredients, key="Excluded-ingredients")
    st.divider()
    st.header("4-week budget forecast")
    st.write("Coming soon!")



#main code with the central code
def main():
    recipe_ids = get_meal_plan(API_KEY)
    total_cost = 0

    print("\n📊 Kostenübersicht:")
    st.write("\n📊 Kostenübersicht:")
    for rid in recipe_ids:
        cost = get_recipe_price(API_KEY, rid)
        total_cost += cost
        st.write(f"Rezept {rid}: {cost:.2f}$")
    st.write(f"\n🧾 Gesamtpreis für den Tag: {total_cost:.2f}$")


    print(f"\n🧾 Gesamtpreis für den Tag: {total_cost:.2f}$")


#call of the main function on button click
if st.session_state.get("generate_button"):
    main()


