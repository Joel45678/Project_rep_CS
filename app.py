#link to the app: https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/

import streamlit as st
st.write("Everything conected") #Test if it works properly

#List of all eating behaviors
allergies = ["lactose", "x", "y"]
diet = ["vegan", "vegetarian", "Pescetarian"]
excluded_ingredients = ["vegan", "vegetarian", "Pescetarian"]

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Allergies")
    st.selectbox(allergies, key="allergies")

with col2:
    st.header("Diet")
    st.selectbox(diet, key="Diet")

with col3:
    st.header("Excluded ingredients")
    st.selectbox(excluded_ingredients, key="Excluded-ingredients")