# Link to the app
https://projectrepcs-wtumtw66amdt87vvcrnk8u.streamlit.app/

# Project_rep_CS

This is a university project for the course Grundlagen und Methoden der Informatik für Wirtschaftswissenschaften

## Team Members
- Fábio Vinício Scheurer
- Joel Nussbaumer
- Laura Sangiorgio
- Ricky Kurt

## Project Description
This app allows users to:
- Select **ingredients to avoid**, such as due to allergies or personal preferences
- Generate personalized **recipe suggestions** based on selected dietary needs
- View an **estimated budget** for each recipe, fetched using external API data


## Installation

To run the project locally, follow these steps:

1. **Clone the repository**:
   git clone https://github.com/Joel45678/Project_rep_CS
   cd Project_rep_CS

2. **Create and activate a virtual environment:**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies:**
pip install -r requirements.txt

4. **Run the app:**
streamlit run app.py



## Folder Overview

- `app/`              
│   ├── `app.py`               – Main Streamlit application that lets users generate and visualize customized daily meal plans
│   ├── `debugging.py`         – Scripts for testing and debugging.
│   ├── `pages`               – Main Streamlit application that lets users generate and visualize customized daily meal plans
│   ├──  ├──  `macronutrients_page.py`               – Additional page for additional nutrition information for the recipes
- `assets/`              – Contains images used in the project.
- `data/`                – ML data and forecast.
│   ├── `get_meal_plan.py`           – Function for price prediction.
│   ├── `training_data_nutrition.csv`  – Training data for ML.
- `recipe_api/`          – interactions with the recipe API.
│   ├── `get_meal_plan.py`           – Get a meal plan from the API.
│   ├── `get_recipe_information.py`  – Retrieves detailed recipe information.
│   ├── `recipe_data.py`             – Defines the `RecipeData` class to encapsulate detailed recipe details.
- `utilities/`           – Utility functions and support modules.
│   ├── `constants.py`               – Stores global constants (API keys, ingredient list).
│   ├── `data_collector.py`          – Collects data to get training data for ML.
│   ├── `random_user_generator.py`   – Generates mock/random user data to  for the data collector.


## API Usage

This app uses the Spoonacular API (https://spoonacular.com/food-api) to fetch meal plans, recipe details, and nutritional info.  
The API keys can be found under `utilities/constants.py`

## Features
- Customizable diet and intolerance inputs
- Automated meal plan generation
- Nutritional breakdown and price visualization
- Option to regenerate individual recipes

## Limitations
- API key has a limited number of daily requests

# Note on the Use of Artificial Intelligence (AI)

During the development of this application, we used ChatGPT by OpenAI as a support tool in the programming process. The AI was used in the following ways:

   - To generate ideas for implementation strategies and architectural decisions,

   - To get assistance with debugging and understanding code behavior,

   - To improve readability of comments and documentation (e.g., this README),

   - To review and refine code snippets based on best practices.

All outputs generated with the help of AI were critically reviewed, edited, and adapted by us to ensure correctness, reliability, and contextual relevance. The final implementation reflects our own understanding and decisions.

In accordance with university guidelines, AI tools were used as supplementary support during development. They did not replace our own analysis or problem-solving. AI-generated outputs are not treated as authoritative sources but as optional assistance—similar to using online documentation or developer forums.
