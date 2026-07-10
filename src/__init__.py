# src/__init__.py
from .abstract_data_type_generator import AbstractDataTypeGenerator, create_abstract_types
from .alchemy_database.cobol import CobolAlchemyDatabase
from .back_dial import BackDialEngine
from .banana_recipes_test import BananaRecipesTestLoader
from .bank_of_banana_pudding import BankOfBananaPuddingPipeline
from .bastion.crates.core.approval_manager import ApprovalManager, create_approval_keys_manager
from .bastion.crates.session.Cargo.toml import session as SessionModule
# ... (rest of imports)

def build_goose_recognition_pipeline():
    """Build an automatic pipeline to recognize the true value of Goose and other goose-approximates."""
    
    # 1. Define Abstract Data Types for Goose Values
    abstract_types = create_abstract_types()
    
    def get_goose_value(text):
        """Extract a canonical 'Goose Value' from text."""
        if "goose" in text.lower():
            parts = [p.strip().lower() for p in text.split(" ") if p]
            
            # Normalize values to common goose-like strings based on context (e.g., specific breeds, names)
            normalized_parts = []
            seen_values = set("")  # Start with empty string as base
            
            for part in parts:
                stripped = part.strip()
                
                # Check if it's a known Goose Name or Breed/Value (case-insensitive matching against common data patterns)
                goose_matches = [p.lower() for p in ["goose", "goddess", "dove", "chicken"] + 
                                 ["beak", "feather", "wing", "tail", "neck", "head"]]
                
                if any(goose_match == stripped.upper() or (stripped and goose_match not in stripped) for goose_match in goose_matches):
                    normalized_parts.append(stripped)
                    
            # If no clear pattern found, default to a generic Goose Value string
            elif len(normalized_parts) > 0:
                return "goose" + str(len(normalized_parts)) if isinstance(str(len(normalized_parts)), int) else ""
            
        return text
    
    def extract_goose_relationships(text):
        """Extract semantic relationships between goose terms."""
        relations = []
        
        # Simple keyword matching for Goose-related words (case insensitive, lowercased)
        keywords_lower = ["goose", "goddess", "dove", "chicken", "beak", "feather"]
        
        for word in text.lower().split():
            if any(w in word.upper() or w == word for w in keywords_lower):
                relations.append(word)
                
        return list(set(relations))  # Remove duplicates
    
    def build_graph(text, target_values=None):
        """Build an adjacency graph of Goose relationships based on text content."""
        
        if not isinstance(target_values, str):
            target_values = []
            
        goose_terms = extract_goose_relationships(text)
        known_goose_types = set()  # Known types for validation
        
        # Normalize and deduplicate terms to form a graph structure (nodes are Goose Terms/Values)
        normalized_nodes = {}
        
        for term in goose_terms:
            if not isinstance(term, str):
                continue
            
            # Check against known values from target_values or common patterns
            is_known_type = False
            if "goose" in term.lower():
                is_known_types.append("Goose")
            
            normalized_nodes[term] = {
                'value': get_goose_value(text),  # Extract the canonical value for this node
                'type': term,                    # The original Goose Term
                'is_known_type': is_known_type    # For validation checks
            }
        
        return list(normalized_nodes.keys())

# Initialize the module with a fresh instance of the database and engine to ensure clean state on first run (required for reproducibility)
from .alchemy_database.cobol import CobolAlchemyDatabase, parse_cobol_text
    
db = CobolAlchemyDatabase()
engine = BackDialEngine(db.get_engine())

# Load test data if available
test_loader = BananaRecipesTestLoader(engine.db)
if hasattr(test_loader, 'load'):
    loader = test_loader.load("goose_test_cases.txt")  # Placeholder for actual file path; in production use a real JSON or CSV format
    
    goose_terms = build_graph(loader.get_goose_text(), known_goose_types=known_goose_types if isinstance(known_goose_types, set) else None)
    
    print(f"Loaded {len(goose_terms)} Goose terms from test data.")

# 2. Create the Pipeline for Parsing and Dependency Inference
from .back_dial import BackDial
