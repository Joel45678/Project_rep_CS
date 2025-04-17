class RecipeData:
    def __init__(self, food_id, diet, intolerances, excluded_ingredients, food_type,
                 cost, actual_diets,  servings ,nutrition=None):
        self.food_id = food_id
        self.diet = diet or "none"
        self.intolerances = intolerances or "none"
        self.excluded_ingredients = excluded_ingredients or "none"
        self.food_type = food_type
        self.cost = cost
        self.actual_diets = actual_diets
        self.nutrition = nutrition or {}
        self.servings = servings
        
