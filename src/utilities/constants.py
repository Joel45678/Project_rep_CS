#API details for spoonacular.com
API_KEY1 = "373547e7ea3647b1b17c5abc690d725c"
API_KEY2 = "de69a22855d946b6b1a3f231c90d36a2" # for ml training
API_KEY3 = "35ebfc08491044658f5e2804ff01bb26" # for ml training

# ingredients: all possible options from Spoonacular
#https://spoonacular.com/food-api/docs
"""intolerances_lst = ["none",
    "dairy",
    "egg",
    "gluten",
    "grain",
    "peanut",
    "seafood",
    "sesame",
    "shellfish",
    "soy",
    "sulfite",
    "tree nut",
    "wheat"]



diet_lst = ["none", 
    "gluten free",
    "ketogenic",
    "vegetarian",
    "lacto-vegetarian",
    "ovo-vegetarian",
    "vegan",
    "pescetarian",
    "paleo",
    "primal",
    "low FODMAP",
    "whole30"
]

excluded_ingredients_lst = ["none", "beef", "pork", "mushrooms", "onion", "garlic"]"""


# reduced list size to increas ML quality - most importent options 
intolerances_lst = [
    "none",       
    "dairy",      
    "gluten",     
    "tree nut",        
    "seafood"     
]

diet_lst = [
    "none",           
    "vegetarian",     
    "vegan",          
    "gluten free",    
    "ketogenic"       
]

excluded_ingredients_lst = [
    "none",
    "beef",
    "mushrooms",
    "onion",
    "garlic"
]


dish_types_lst = ["main coruse", "bread", "marinade", "side dish", "dessert", "appetizer", "salad", "bread", "breakfast", "soup", "beverage", "sauce", "marinade", "fingerfood", "snack", "drink"]