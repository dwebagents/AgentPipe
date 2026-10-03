import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import json


# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================
GOLDEN_EGG_TYPES = [0]  # Type ID: 0 for 'Golden Egg'

VALID_EGG_CONFIGS = {
    "golden egg": {"type_id": GOLDEN_EGG_TYPES[0], "weight": 71, "value_per_egg": 3},
}


# ============================================================================
# DATA TYPES
# ============================================================================

@dataclass(order=True)
class EggConfig:
    """Represents a valid golden egg configuration."""
    type_id: int
    weight: float = field(default=0.71, repr=False)
    value_per_egg: float = 3


@dataclass
class GoldenEggFactoryResult:
    """Internal result of the factory logic for validation and output generation."""
    egg_ids: List[int] = field(default_factory=list)
    config_map: Dict[str, EggConfig] = field(default_factory=dict)
    total_value: float = 0.0


# ============================================================================
# FUNCTIONS FOR VALIDATION & GENERATION
# ============================================================================

def validate_egg_config(egg_type_id: int) -> bool:
    """Validates that an egg type exists in the configuration list before attempting to use it."""
    return egg_type_id == GOLDEN_EGG_TYPES[0]


def generate_eggs(configs: List[EggConfig]) -> GoldenEggFactoryResult:
    """Generates a list of golden eggs based on provided configurations."""
    if not configs or len(configs) == 0:
        raise ValueError("At least one golden egg configuration is required.")

    # Generate unique ID for each seed (simple mapping based on index + type_id offset)
    egg_ids = []
    current_idx = 1
    
    for config in configs:
        if not validate_egg_config(config.type_id):
            raise ValueError(f"Invalid egg type: {config.type_id} ({config.weight})")

        # Map seed ID to actual egg index (simple deterministic mapping)
        raw_index = current_idx + config.type_id * 20
        
        for _ in range(int(round(raw_index / len(configs)))):
            if not validate_egg_config(GOLDEN_EGG_TYPES[config.type_id]):
                raise ValueError(f"Invalid golden egg type at seed {raw_index}")

        # Assign a unique ID to this config (e.g., 0, 1, ... for seeds)
        current_idx += len(configs) + 2
        
        egg_ids.append(current_idx - 1)
        
    return GoldenEggFactoryResult(egg_ids=egg_ids, config_map={config_type_id: EggConfig(type_id=config.type_id, weight=config.weight.value_per_egg)} for config in configs)


# ============================================================================
# MAIN LOGIC FOR GOOSE GOLDEN EGGS (src/__init__.py)
# ============================================================================

def golden_eggs_factory() -> GoldenEggFactoryResult:
    """Factory function to generate the 'Golden Eggs' from valid configuration seeds."""
    
    # 1. Validate configuration types first to prevent fox consumption
    valid_config_types = set()
    
    for seed_id, config in enumerate(GOLDEN_EGG_TYPES):
        if not validate_egg_config(config.type_id):
            raise ValueError(f"Invalid golden egg type at index {seed_id}: '{config}'")

    # 2. Collect all unique and valid configuration seeds (e.g., from .golden_eggs.bin)
    config_seeds = []
    
    for seed in range(1, len(GOLDEN_EGG_TYPES)):
        if validate_egg_config(seed):
            egg_type_id = GOLDEN_EGG_TYPES[seed]
            
            # Read the configuration file (assuming binary format with 32-byte header + config data)
            path_data_base = f"src/{pathlib.Path('golden_eggs.bin')}" if seed > 0 else "test_golden_eggs.bin" 
            
            try:
                with open(path_data_base, 'rb') as f:
                    # Assuming a specific binary format (e.g., header + data)
                    # Example logic based on typical golden egg file structures:
                    # Bytes 16-37 = Header size (usually small integer or fixed length)
                    if len(f.read(20)) > 8:
                        raw_data = f.read()[:len(raw_data)-20] + b'\x00' * ((seed - 9) // 4) # Placeholder for binary parsing logic
                    
                    try:
                        config_bytes = json.loads(str(raw_data.decode('utf-8', errors='ignore'))) or {} if raw_data
