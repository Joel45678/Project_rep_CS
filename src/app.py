#link to the app: (https://projectrepcs-f2thgw3scyfevbfah28c7b.streamlit.app) or https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/
import streamlit as st

#import custom functions from folder functions
# import ingredients lst
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.constants import intolerances_lst, diet_lst, excluded_ingredients_lst, API_KEY2
from recipe_api.get_meal_plan import get_meal_plan
from recipe_api.get_recipe_information import get_recipe_price, get_recipe_details



#page layout
col1h, col2h = st.columns(2)
col1s = st.columns(1)
col1, col2, col3 = st.columns(3)

#variables
diet = ""
excluded_ingredients = ""
price = 0.0


#streamlit page
with col1h:
    st.subheader("")
    st.image("src/assets/01_Logo.png", width=200)

with col2h:
    st.empty()
    #st.title("SmartMeal")
    #st.subheader("A recipe recommender and meal planner")

with col1s [0]: #add features
    st.markdown("<br>" *3, unsafe_allow_html= True)
    st.header("Desired amount of meals")
    selected_amount = st.number_input(
        label= "choose the amount of recipies that you prefear",
        min_value=1,
        step=1,
        format="%d",
        key="number_input"
    )
    
with col1:
    st.header("Intolerances")
    selected_allergy = st.selectbox("Intolerances", intolerances_lst, key="intolerances")
    st.divider()
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    st.button("Generate Meal Plan", key="generate_button")

with col2:
    st.header("Diet")
    selected_diet = st.selectbox("Diet", diet_lst, key="diet")
    st.divider()
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    st.header("Your meal plan for the next week")
    titles_placeholder = st.empty() #placeholder for recips
    price_placeholder = st.empty() #placeholder for price

with col3:
    st.header("Ingredients")
    selected_exclude = st.selectbox("Exclude ingredients", excluded_ingredients_lst, key="excluded_ingredients")
    st.divider()
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    st.header("4-week budget forecast")
    st.write("Coming soon!")



#central code of the app - starts with button click (see below)
#print() is only used for debugging purposes
def main():
    recipe_titles = []

    try:
        recipe_ids, foody_type = get_meal_plan(API_KEY2, "day", diet, intolerances, excluded_ingredients) #get random recipes

        total_cost = 0
        st.header("Food plan:")

        for rid in recipe_ids: 
            recipe_id = rid["id"]
            title, image, instructions = get_recipe_details(API_KEY2, recipe_id) #get additional information about the recipe
            cost = get_recipe_price(API_KEY2, recipe_id) #get the price information about the recipe
            total_cost += cost # sum of all recipe prices 
            recipe_titles.append(title) # List with recipe titles

            #st.markdown(f'<a name="{title.replace(" ", "-").lower()}"></a>', unsafe_allow_html=True) evtl. verlinken
            st.markdown(f"{title}")
            st.write(f"Price: {cost:.2f}$")
            
            if image:
                st.image(image, width=250)

            #st.session_state.update("st_meal_plan_list",title)
            st.markdown("**Instructions:**", unsafe_allow_html=True)
            st.write(instructions or "No instructions provided.", unsafe_allow_html=True)
            st.markdown("———")
            
        titles_placeholder.markdown("\n".join([f"#### {t}" for t in recipe_titles])) #list of Titles [f"- {t}" for t in recipe_titles])
        price_placeholder.markdown(f"\n**Price for the plan:** {total_cost:.2f}$")
        #st.write(f"\n**Price for the plan:** {total_cost:.2f}$")
    except:
    # check if API-Limit is exceeded
        recipe_ids = get_meal_plan(API_KEY2, "day", diet, intolerances, excluded_ingredients) #get random recipes
        if recipe_ids == 402:
            st.error("Daily recipe limit exceeded")
            return






#call of the main function on button click
if st.session_state.get("generate_button"):
    price = 0.0
    #get user inputs
    diet = st.session_state.get("diet")
    intolerances = st.session_state.get("allergies")
    excluded_ingredients  = st.session_state.get("excluded_ingredients")

    # convert "none" to None-type
    if intolerances  == "none":
        intolerances  = None
    if diet == "none":
        diet = None
    if excluded_ingredients == "none":
        excluded_ingredients = None
    
    main()


#Debugging:
#variables

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

main()
