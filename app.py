#link to the app: https://projectrepcs-f2thgw3scyfevbfah28c7b.streamlit.app or https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/
import streamlit as st

#import custom functions from folder functions
from functions.get_meal_plan import get_meal_plan
from functions.get_recipe_price import get_recipe_price


#API details for spoonacular.com
API_KEY = "373547e7ea3647b1b17c5abc690d725c"

#page layout
col1, col2, col3 = st.columns(3)

#List of all possible eating behaviors 
intolerances_lst = ["none",
    "dairy",
    "egg",
    "gluten",
    "grain",
    "peanut",
    "seafood",
    "sesame",
    "shellfish",
    "soy",
    "sulfite",
    "tree nut",
    "wheat"]
intolerances = ""
diet_lst = ["none", 
    "gluten free",
    "ketogenic",
    "vegetarian",
    "lacto-vegetarian",
    "ovo-vegetarian",
    "vegan",
    "pescetarian",
    "paleo",
    "primal",
    "low FODMAP",
    "whole30"
]
diet = ""
excluded_ingredients_lst = ["none", "beef", "pork", "mushrooms", "onion", "garlic"]
excluded_ingredients = ""
#variables
price = 0.0

#central code of the app - starts with button click (see below)
#print() is only used for debugging purposes
def main():
    recipe_ids = get_meal_plan(API_KEY, "day", diet, excluded_ingredients, intolerances) #get random recipe
    if recipe_ids == 402:
        st.error("Daily recipe limit exceeded")
        return
    total_cost = 0

    st.write("Food plan:")
    for rid in recipe_ids:
        cost = get_recipe_price(API_KEY, rid["id"])
        total_cost += cost
        #print(f"Rezept {rid["title"]}: {cost:.2f}$")
        st.write(f"{rid["title"]}: {cost:.2f}$")
        
    st.write(f"\n Price for the plan: {total_cost:.2f}$")
    #print(f"\n🧾 Gesamtpreis für den Tag: {total_cost:.2f}$")


#streamlit page
st.title("SmartMeal")
st.subheader("A recipe recommender and meal planner")
st.image("./assets/01_Logo.png")
with col1:
    st.header("Intolerances")
    selected_allergy = st.selectbox("Intolerances", intolerances_lst, key="intolerances")
    st.divider()
    st.button("Generate Meal Plan", key="generate_button")

with col2:
    st.header("Diet")
    selected_diet = st.selectbox("Diet", diet_lst, key="diet")
    st.divider()
    st.header("Your meal plan for the next week")
    st.write(f"Price: {price}")

with col3:
    st.header("Excluded ingredients")
    selected_exclude = st.selectbox("Exclude ingredients", excluded_ingredients_lst, key="excluded_ingredients")
    st.divider()
    st.header("4-week budget forecast")
    st.write("Coming soon!")



#call of the main function on button click
if st.session_state.get("generate_button"):
    #variables
    price = 0.0
    diet = st.session_state.get("diet")
    intolerances = st.session_state.get("allergies")
    excluded_ingredients  = st.session_state.get("excluded_ingredients")

    if intolerances  == "none":
        intolerances  = None
    if diet == "none":
        diet = None
    if excluded_ingredients == "none":
        excluded_ingredients = None
    
    main()


#Debugging:
#variables
"""
price = 0.0
diet = "vegan"
intolerances = "gluten"
excluded_ingredients = "none"

if intolerances == "none":
    intolerances = None
if diet == "none":
    diet = None
if excluded_ingredients == "none":
    excluded_ingredients = None

main()"""
