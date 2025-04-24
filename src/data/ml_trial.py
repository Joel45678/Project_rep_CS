import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np

# 1. CSV laden
data = pd.read_csv('training_data_nutrition.csv')

# 2. Makronährstoffe umwandeln
for col in ['carbs', 'fat', 'protein']:
    data[col] = data[col].str.replace('g', '').astype(float)

# 3. 'all_diets' in Features umwandeln
diet_types = ['gluten free', 'dairy free', 'vegan', 'ketogenic', 'paleolithic', 'primal', 'whole 30', 'lacto ovo vegetarian']
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

# 10. Fehler ausgeben
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {round(mae, 2)} €")

# 11. Vorhersagen in Text-Datei speichern
with open('forecast_results.txt', 'w') as f:
    f.write(f"Mean Absolute Error: {round(mae, 2)} €\n")
    f.write("Vorhersagen (Kosten pro Portion):\n")
    for idx, value in enumerate(y_pred):
        f.write(f"{idx+1}: {round(value, 2)} €\n")

print("Vorhersagen wurden in 'forecast_results.txt' gespeichert.")
