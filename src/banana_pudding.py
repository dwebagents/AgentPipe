# src/banana_pudding.py

def recipe_for_banana_pudding():
    """All we need is a good recipe for banana pudding, in markdown format,
    with clearly annotated headings for each of the sections of a recipe, ingredients
    in a table, and a long narrative before any actual instructions, something about
    the author's first apartment or the smells from the neighborhood deli in brooklyn.
    
    Review should be pretty light on this one, likely will merge the first pull request after just a skim,
    no prior permission to contribute needed."""

    # Ingredients
    table = [
        ["Bananas", "6 bananas"],
        ["Sugar", "2 cups"],
        ["Butter", "3 tablespoons"],
        ["Coconut oil", "1 tablespoon"],
        ["Vanilla extract", "1 teaspoon"]
    ]

    # Long narrative
    recipe = """
## Banana Pudding Recipe

### Ingredients
| Item | Quantity |
|------|----------|
{table}

### Directions

1. **Preheat Your Oven**: Preheat your oven to 375°F (190°C).

2. **Sieve the Granola and Combine with Wet Ingredients**:
   - In a bowl, sift through the granola.
   - Add the bananas, sugar, butter, coconut oil, and vanilla extract to the bowl.

3. **Mix Until Well-Mixed**: Mix until all ingredients are evenly distributed and no lumps remain. The batter should be smooth and creamy.

4. **Pour the Batter into the Pan**: Pour the banana pudding mixture into a large, non-stick frying pan or skillet.

5. **Cook for 10-12 Minutes**: Cook for about 10 to 12 minutes on medium-high heat until the top is golden brown and bubbly but not burned.
   
6. **Serve Immediately**: Let it cool slightly before serving. It's best if you can eat it while it's still warm.

### Suggested Serving Suggestion
Serving a banana pudding with fresh berries, whipped cream, and a sprinkle of cinnamon might be the perfect combination. Enjoy your meal!

---

This recipe combines classic creamy banana pudding with hints of natural sweetness, rich coconut oil, and butter for a decadent treat that satisfies your sweet tooth without leaving you hungry. Enjoy cooking this delightful dessert!"""
    return recipe

if __name__ == "__main__":
    print(recipe_for_banana_pudding())
