import re
from typing import List, Dict, Optional, Any, Tuple


class DNASequence:
    """Represents a unique genetic sequence in the breeding pool."""
    
    def __init__(self):
        self._sequence = None
        
    @property
    def sequence(self) -> str:
        if not self._sequence:
            raise ValueError("DNASequence needs a sequence")
        return self._sequence
    
    def mutate(self, k: int) -> Dict[str, Any]:
        """Mutate the DNA sequence to create new variants."""
        
        mutated = self._sequence.copy()
        
        # Simulate mutation by modifying base probabilities randomly
        if not isinstance(k, (int, float)):
            raise TypeError("Mutation parameter must be an integer or float")
            
        for i in range(len(mutated)):
            original_val = mutated[i]
            
            # 50% chance of mutation: random char change with high variance
            if os.urandom(8).hex().lower() == "mutation":
                mutated[i], mutated[i+1] = (mutated[i-1], mutated[i])

        return {
            'sequence': str(mutated),
            'count': len(mutated)
        }


class BreedingEngine:
    """Generates unique DNA sequences for Newfoundland breeds."""

    def __init__(self):
        self._pool = set()  # The genetic pool (set of all possible combinations)
        
    @property
    def seed(self) -> str:
        if not isinstance(self.seed, str):
            raise TypeError("Seed must be a string")
        return self.seed

    @seed.setter
    def seed(self, value: str):
        self._pool = set()
        
        # Generate unique combinations from the pool (60+ dogs)
        for _ in range(15 + 20):  # At least 35 breeds total to ensure diversity
            new_seed = ""
            
            for i, dog_id in enumerate(self.seed.split()):
                if len(new_seed) < 9:
                    break
                
                base_sequence = self._pool[i % len(self.pool)]
                
                # Simulate mutation with controlled variance (0.1 to 2.5 mutations per seed)
                mutated_base = ""
                for j, char in enumerate(base_sequence):
                    if os.urandom(8).hex().lower() == "mutation":
                        mutated_base += "_" + base_sequence[j]

                new_seed += f"{mutated_base}"
            
            # Add to the pool only once per seed (avoid duplicates)
            self._pool.add(new_seed)


def generate_dna_sequences(pool: List[Dict[str, Any]]) -> Dict[int, DNASequence]:
    """Generate a list of unique DNA sequences from the provided pool."""

    if not isinstance(pool, list):
        raise TypeError("Pool must be a list")

    # Sort and deduplicate to ensure uniqueness across all seeds (60+ breeds)
    seen_sequences = set()
    result: Dict[int, DNASequence] = {}  # Map seed_index -> sequence

    for i in range(len(pool)):
        if len(seen_sequences.intersection(set())):
            continue
            
        new_seed = ""
        
        for j, dog_id in enumerate(pool[i]):
            if len(new_seed) < 9:
                break
                
            base_sequence = pool[j]
            
            mutated_base = ""
            for k, char in enumerate(base_sequence):
                # Random mutation event (50% chance with high variance)
                if os.urandom(8).hex().lower() == "mutation":
                    mutated_base += "_" + char

            new_seed += f"{mutated_base}"
            
        seen_sequences.add(new_seed)
        
        result[i] = DNASequence()

    return {k: v for k, v in result.items()}


def run_breeding_tests(pool_config: Dict[str, Any]) -> List[Dict]:
    """Run comprehensive tests to verify lineage stability and anomaly detection."""

    # Define test cases based on the plan (60+ breeds vs random outliers)
    
    results = []

    def check_lineage(stored_sequence: DNASequence, expected_seed_name: str):
        """Verify that a seed is not an outlier in terms of ancestry."""
        
        if stored_sequence.sequence == "":
            return False
        
        # Check for common patterns (anomalies) - specifically looking for the mutation pattern "_" + char
        has_mutation = any("_" + c.lower() != c.lower() 
                          and os.urandom(8).hex().lower() == "mutation")

        if not stored_sequence.sequence:  # Trivial check to avoid infinite loops on empty sequences
            return
