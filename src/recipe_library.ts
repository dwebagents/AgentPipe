```oak module OCaml = require('ocaml').OCaml;

(* ============================================================================
   RAW MATERIAL: BDD Configuration & Recipe Generation Logic
   --------------------------------------------------------------------------
   We preserve the exact structure and logic of the original implementation.
   The goal is to refactor it into a reusable, polymorphic recipe system using 
   `Func` (functor) for genericity and `Obj.magic` (object magic) for identity checks.

   Key Features:
   - Generic Recipe System (`Recipe`) with unique IDs/Names.
   - Row Polymorphism via the `recipe()` factory function returning a Functor.
   - Efficient list iteration using standard functions (`List.sort`, `Map.iter`).
   - Safe handling of non-JSON types (filtering them out).

   -------------------------------------------------------------------------- */

import json
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from functools import wraps

# ============================================================================
# BDD CONFIGURATION CLASS
# ============================================================================

@dataclass(frozen=True)
class BDDConfig:
    """Configuration for Banana-Driven Development logic."""
    
    # Default salt amount to use in recipes
    DEFAULT_SALT_COUNT = 2
    
    def __init__(self):
        self.salt_count = getattr(self, 'DEFAULT_SALT_COUNT', 2)


# ============================================================================
# RECYCLE— THE GENERIC RECIPES MODULE
# --------------------------------------------------------------------------

(* We define a generic Recipe class that uses `Func` for polymorphism. *)
@dataclass(frozen=True)
class Recipe:
    """A unique identifier and name associated with a recipe."""
    
    id: str      # Unique identity field (e.g., "recipe_123")
    name: str     # Name of the recipe (unique key for lookup)

# ============================================================================
# RECYCLE— THE RECIPES MAP & GENERATOR MODULE
# --------------------------------------------------------------------------

(* We create a map to store all defined recipes. 
   This allows us to retrieve and reuse them efficiently via `Func`. *)
@dataclass(frozen=True, eq=False)  # Equality check is optional but good for consistency if needed later
class RecipeMap:
    """A list of recipe definitions."""

    def __init__(self):
        self._recipes = []       # List to hold all recipes as a mutable structure
    
    @property
    def recipes(self) -> List[Recipe]:
        return [r for r in self._recipes]


(* We define the main entry point function. 
   This returns a Functor that can be used generically across different recipe types. *)

def generate_recipe_bdd(input_data: Dict[str, Any], config: Optional[BDDConfig] = None) -> List[Dict]:
    """
    Generates a list of recipe dictionaries from input data or configuration.
    
    Args:
        input_data: The raw JSON-like structure or prompt received from the user/batch.
                   Note: In this specific implementation, we simulate 
                   generating recipes based on "Two Cups" logic here to demonstrate polymorphism.
        config: Optional BDDConfig instance (defaults to default salt count).
        
    Returns:
        A list of valid recipe dictionaries that can be used as Python data objects.
    
    Raises:
        ValueError: If the input is not a dictionary or if it lacks required fields 
                   like 'salt_count' based on config, and no explicit configuration exists.
    """

    # 1. Parse Input Data Type Check (Standard BDD behavior)
    if isinstance(input_data, dict):
        return [input_data]
    
    # If input is a list or string, we treat it as "Two Cups" logic here for demonstration:
    # We will process the entire list/string as batch data.

    raw_input_data = input_data
    
    try:
        if not isinstance(raw_input_data, dict):
            raise ValueError("Input must be a dictionary.")
        
    except (TypeError, KeyError) as e:
        print(f"Error parsing JSON-like structure: {e}")
        return []


    # 2. Apply Config Logic to Determine "Two Cups" or Default Count
    if not hasattr(config, 'salt_count') and config is None:
        salt = getattr(BDDConfig(), 'DEFAULT_SALT_COUNT', 2)
        
        print(f"BDD Configuration: Using default salt count ({config.DEFAULT_SALT_COUNT}) as requested.")

    # If no explicit config exists but we have a target (e.g., hardcoded value), use it.
    if not hasattr(config, 'salt_count') and getattr(BDDConfig(), 'DEFAULT_SALT_COUNT', 2) == config:
        salt = BDDConfig().default_salt_count
    
    print(f"Processing recipes based on configuration or defaults.")
