import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np


def train_and_forecast_model(csv_path: str, output_path: str = None) -> pd.DataFrame:
    """
    Trainiert ein ML-Modell zur Vorhersage von meal_costs_perserving.
    Gibt ein DataFrame mit Testdaten + Vorhersage zur weiteren Verwendung im Frontend zurück.
    """
    # 1. CSV laden
    data = pd.read_csv(csv_path)

    # 2. Makronährstoffe umwandeln
    for col in ['carbs', 'fat', 'protein']:
        data[col] = data[col].str.replace('g', '').astype(float)

    # 3. 'all_diets' in Features umwandeln
    diet_types = [
        'gluten free', 'dairy free', 'vegan', 'ketogenic', 
        'paleolithic', 'primal', 'whole 30', 'lacto ovo vegetarian'
    ]
    for diet in diet_types:
        data[diet] = data['all_diets'].apply(lambda x: 1 if pd.notnull(x) and diet in x else 0)

    # 4. One-Hot-Encoding für kategorische Spalten
    categorical_cols = ['diet', 'intolerances', 'excluded_ingredients', 'food_type']
    data = pd.get_dummies(data, columns=categorical_cols)

    # 5. Features & Ziel definieren
    X = data.drop(columns=['meal_costs_perserving', 'all_diets'])
    y = data['meal_costs_perserving']

    # 6. NaN und inf bereinigen
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X = X.dropna()
    y = y.loc[X.index]

    # 7. Split in Training und Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 8. Modell trainieren
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # 9. Vorhersagen machen
    y_pred = model.predict(X_test)

    # 10. Zusammenfassung erstellen
    test_results = X_test.copy()
    test_results['actual_cost'] = y_test
    test_results['predicted_cost'] = y_pred

    # 11. Fehler anzeigen
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {round(mae, 2)} €")

    # 12. Optional als Textdatei speichern
    if output_path:
        test_results[['actual_cost', 'predicted_cost']].to_csv(output_path, index=False)
        print(f"Vorhersagen gespeichert unter: {output_path}")

    return test_results
