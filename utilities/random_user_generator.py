from constants import intolerances_lst
from constants import diet_lst
from constants import excluded_ingredients_lst

# generiert zufällige Userdaten
import random


def generate_random_preferences():
    diet = random.choice(diet_lst[0:])
    intolerance = random.choice(intolerances_lst[0:])
    exclude = random.choice(excluded_ingredients_lst[0:])
    if intolerance == "none":
        intolerance = None
    if diet == "none":
        diet = None
    if exclude == "none":
        exclude = None
    return diet, intolerance, exclude
