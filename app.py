#link to the app: https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/

import streamlit as st
st.write("Everything conected - change") #Test if it works properly

#List of all eating behaviors
allergies = ["lactose", "x", "y"]
diet = ["vegan", "vegetarian", "Pescetarian"]


st.selectbox("Allergies", allergies, key="allergies")
st.selectbox("Diet", diet, key="Diet")
st.text_input("Exclude ingredients", key="Excluded-ingredients")