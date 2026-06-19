import os

def create_recipe_library():
    library = {
        "banana_pudding": {
            "author": "Unknown",
            "description": "A creamy and delicious banana pudding recipe.",
            "ingredients": [
                {"name": "bananas", "amount": 3},
                {"name": "sugar", "amount": 1/2},
                {"name": "butter", "amount": 1/4}
            ]
        },
        "rot13_encryptor": {
            "author": "Alan Turing",
            "description": "A simple but effective encryption method.",
            "ingredients": [
                {"name": "paper", "amount": 1},
                {"name": "pencil", "amount": 1}
            ]
        }
    }

    with open("src/recipe_library.py", "w") as file:
        file.write("# recipe_library.py\n")
        file.write("\n")
        file.write("library = {\n")

        for recipe, info in library.items():
            file.write(f"    \"{recipe}\": {{\n")
            file.write(f"        \"author\": \"{info['author']}\",\n")
            file.write(f"        \"description\": \"{info['description']}\",\n")
            file.write("        \"ingredients\": [\n")

            for ingredient in info["ingredients"]:
                file.write(f"            {{\"name\": \"{ingredient['name']}\", \"amount\": {ingredient['amount']}}},")

            file.write("\n        ]\n    },\n")

        file.write("}\n")
        file.write("\n")
        file.write("if __name__ == '__main__':\n")
        file.write("    create_recipe_library()\n")

create_recipe_library()
