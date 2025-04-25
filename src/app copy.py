#link to the app: https://projectrepcs-gtgiolma4dy7hv6hprifgr.streamlit.app/
import streamlit as st
import plotly.graph_objects as go

#import custom functions from folder functions
# import ingredients lst
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.constants import intolerances_lst, diet_lst, excluded_ingredients_lst, API_KEY
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
    params = {"apiKey": API_KEY, "number": 1}
    if diet:
        params["tags"] = diet
    if intl:
        params["intolerances"] = intl
    if excl:
        params["excludeIngredients"] = excl

    # 3) Gather the ID
    #existing_ids = [r["id"] for r in st.session_state.recipes]

    # 4) get recipe
    new_rec = get_meal_plan(API_KEY, "day", diet, intl, excl, 1)
    new_id    = new_rec["id"]
    title     = new_rec.get("title", "")
    image_url = new_rec.get("image", "")
    instr     = new_rec.get("instructions", "") or ""

    # 6) Get cost
    cost = get_recipe_price(API_KEY, new_id)

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




#streamlit page
#with col1h:
    #st.subheader("")
    #st.image("src/assets/01_Logo.png", width=200)

#with col2h:
    #st.empty()
    #st.title("SmartMeal")
    #st.subheader("A recipe recommender and meal planner")

with col1s [0]: #add amount of meals
    st.markdown("<br>" *3, unsafe_allow_html= True)
    st.header("Desired amount of meals")
    selected_amount = st.number_input(
        label= "choose the number of recipes you prefer",
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

# Chart
col1f = st.columns(1)[0]
with col1f:
    total_carbs = st.session_state.get("total_carbs", 0.0)
    total_fat = st.session_state.get("total_fat", 0.0)
    total_protein = st.session_state.get("total_protein", 0.0)
    total_cost = st.session_state.get("total_cost", 0.0)
    recipes = st.session_state.get("recipes", [])

    # Ensure we have valid values for the variables
    if (
        recipes and
        total_carbs != 0.0 and
        total_fat != 0.0 and
        total_protein != 0.0 and
        total_cost != 0.0 and
        selected_amount > 0
    ):
        # If valid data exists, calculate averages
        average_carbs = total_carbs / selected_amount
        average_fat = total_fat / selected_amount
        average_protein = total_protein / selected_amount

        macronutrients = ["Protein", "Fat", "Carbs"]
        values = [average_protein, average_fat, average_carbs]

        bar_fig = go.Figure([go.Bar(x=macronutrients, y=values, text=values, textposition='auto')])
        bar_fig.update_layout(
            title="Average Macronutrient Breakdown per Meal",
            xaxis_title="Macronutrients",
            yaxis_title="Grams",
            template="plotly_white",
            yaxis=dict(range=(0, 300), tick0=0, dtick=50, tickformat=',d')
        )
        st.plotly_chart(bar_fig)

        price_placeholder.markdown(
            f"**Price for the plan:** {total_cost:.2f}$"
        )

        for idx, r in enumerate(recipes):
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
                on_click = regenerate_one,
                args=(idx,),
            )
    else:
        st.info("Generate a meal plan to see your recipes and breakdown.")



#central code of the app - starts with button click (see below)
#print() is only used for debugging purposes
def main(selected_amount, diet, intolerances, excluded_ingredients):
    recipe_titles = []

    try:
        recipe_ids, foody_type = get_meal_plan(API_KEY, "day", diet, intolerances, excluded_ingredients, number=st.session_state.get("number_input", 1)) #get random recipes

        total_cost = 0
        st.header("Food plan:")

        for rid in recipe_ids: 
            recipe_id = rid["id"]
            title, image, instructions = get_recipe_details(API_KEY, recipe_id) #get additional information about the recipe
            cost = get_recipe_price(API_KEY, recipe_id) #get the price information about the recipe
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
        recipe_ids = get_meal_plan(API_KEY, "day", diet, intolerances, excluded_ingredients) #get random recipes
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
    
    main(selected_amount, diet, intolerances, excluded_ingredients)

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
