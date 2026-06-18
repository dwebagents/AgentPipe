import json

class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

class AlchemyDatabase:
    def __init__(self):
        self.recipes = {}

    def add_recipe(self, recipe_name, recipe_data):
        # Convert JSON data to a Recipe object
        recipe_object = Recipe(recipe_name, [Ingredient(ingredient['name'], ingredient['quantity']) for ingredient in recipe_data])
        self.recipes[recipe_name] = recipe_object

    def get_recipe(self, recipe_name):
        return self.recipes.get(recipe_name)

class AlchemyManager:
    def __init__(self):
        self.database = AlchemyDatabase()

    def create_alchemy_database(self):
        # Sample alchemical data
        sample_data = {
            'recipe1': {'Quicksilver': 50, 'Antimony': 25},
            'recipe2': {'JavaScript': 75, 'Python': 50}
        }

        # Add recipes to the database
        for recipe_name, recipe_data in sample_data.items():
            self.database.add_recipe(recipe_name, recipe_data)

    def run_alchemy_manager(self):
        # Run the alchemy manager
        pass

# Create an Alchemy manager and run
alchemy_manager = AlchemyManager()
alchemy_manager.create_alchemy_database()
alchemy_manager.run_alchemy_manager()
