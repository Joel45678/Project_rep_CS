import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np
from utilities.constants import intolerances_lst, diet_lst, excluded_ingredients_lst


def forecast_user_constraints(csv_path, diet=None, intolerance=None, excluded_ingredient=None):
    import pandas as pd
    import numpy as np
    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor(random_state=42)


    data = pd.read_csv(csv_path)

    for col in ['carbs', 'fat', 'protein']:
        data[col] = data[col].str.replace('g', '').astype(float)


    for diet_type in diet_lst:
        data[diet_type] = data['all_diets'].apply(lambda x: 1 if pd.notnull(x) and diet_type in x else 0)

    data = pd.get_dummies(data, columns=['diet', 'intolerances', 'excluded_ingredients', 'food_type'])

    data.dropna(inplace=True)

    X = data.drop(columns=['meal_costs_perserving', 'all_diets'])
    y = data['meal_costs_perserving']

    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)

    # User-Eingabe-Feature-Vektor vorbereiten
    input_dict = {col: 0 for col in X.columns}
    if diet:
        col_name = f'diet_{diet}'
        if col_name in input_dict:
            input_dict[col_name] = 1
    if intolerance:
        col_name = f'intolerances_{intolerance}'
        if col_name in input_dict:
            input_dict[col_name] = 1
    if excluded_ingredient:
        col_name = f'excluded_ingredients_{excluded_ingredient}'
        if col_name in input_dict:
            input_dict[col_name] = 1

    input_df = pd.DataFrame([input_dict])
    input_df = input_df[X.columns]  # gleiche Spaltenreihenfolge

    predicted_cost = model.predict(input_df)[0]
    return round(predicted_cost, 2)
