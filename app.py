#link to the app: https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/

import streamlit as st
st.write("Everything conected") #Test if it works properly

#List of all eating behaviors
allergies = ["none", "lactose", "gluten"]
diet = ["none", "vegan", "vegetarian", "Pescetarian"]
excluded_ingredients = ["none", "vegan", "vegetarian", "Pescetarian"]

#variables
price = 17.5

col1, col2, col3 = st.columns(3)
col1b, col2b = st.columns(2)

with col1:
    st.header("Allergies")
    st.selectbox("Allergies", allergies, key="allergies")

with col2:
    st.header("Diet")
    st.selectbox("Diet", diet, key="Diet")

with col3:
    st.header("Excluded ingredients")
    st.selectbox("Exclude ingredients", excluded_ingredients, key="Excluded-ingredients")

with col1b:
    st.header("Your meal plan for the next week")
    st.write(f"Price: {price}")

with col2b:
    st.header("Calculate your weekly cost")
    st.write("Coming soon!")