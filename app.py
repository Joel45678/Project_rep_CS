#link to the app: https://projectrepcs-kgxuhxcx6ux2eygqo8g8ey.streamlit.app/

import streamlit as st
st.write("Everything conected") #Test if it works properly

#List of all eating behaviors
allergies = ["lactose", "x", "y"]
diet = ["vegan", "vegetarian", "Pescetarian"]
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Allergies")
    st.selectbox("Allergies", allergies, key="allergies")

with col1:
    st.header("Diet")
    st.selectbox("Diet", diet, key="Diet")

with col1:
    st.header("Excluded ingredients")
    st.text_input("Exclude ingredients", key="Excluded-ingredients")