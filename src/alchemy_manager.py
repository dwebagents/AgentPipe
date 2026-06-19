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
        print("Alchemy Manager Started...")
        try:
            # Simulate processing or calculations
            # For demonstration purposes, just print a simple message
            print("Processing Recipes...")
            self.process_recipes()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Alchemy Manager Ended.")

    def process_recipes(self):
        # This method would contain the main logic for processing recipes
        for recipe_name, recipe_data in self.database.recipes.items():
            print(f"Processing Recipe: {recipe_name}")
            # Simulate a complex process here, e.g., cooking and blending ingredients
            print("Step 1: Extract Ingredients")
            for ingredient in recipe_data.ingredients:
                print(f"Extracting {ingredient.name}: {ingredient.quantity} grams")

            print("Step 2: Combine Ingredients")
            print("Mixing together Quicksilver and Antimony...")
            # Simulate a chemical reaction here, e.g., reacting two metals
            print("Step 3: Synthesize Recipe")
            print(f"Synthesizing Recipe: {recipe_name}")
            # Print final product or result
           
