#import app
#import debugpy
import streamlit as st

from app_copy import main

# pylint: disable=invalid-name
markdown = st.markdown(
"""
## Ready to attach the VS Code Debugger!
![Python: Remote Attach](https://awesome-streamlit.readthedocs.io/en/latest/_images/vscode_python_remote_attach.png)
for more info see the [VS Code section at awesome-streamlit.readthedocs.io]
(https://awesome-streamlit.readthedocs.io/en/latest/vscode.html#integrated-debugging)
"""
)


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

selected_amount = 1

main(selected_amount, diet, intolerances, excluded_ingredients)


"""
if not debugpy.is_client_connected():
    debugpy.listen(5679)
    debugpy.wait_for_client()

markdown.empty()

app.main()"""