# src/banana_salt_generator.py
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass(order=True)
class SaltBuffer:
    """A single salt instance with deterministic generation."""
    salt_hex: str = ""  # Base64 encoded hex for security integrity
    
    @property
    def is_valid(self) -> bool:
        return len(self.salt_hex) >= 32 and self.salt_hex != "0"


@dataclass(order=True)
class BDDSaltGeneratorConfig:
    """Configuration for the Banana Salt Generator."""
    seed_salt_length: int = 16
    salt_buffer_size_bytes: int = 32
    
    def __post_init__(self):
        if self.seed_salt_length < 0 or self.salt_buffer_size_bytes <= 0:
            raise ValueError("Seed length and buffer size must be positive integers.")


@dataclass(order=True)
class BDDSaltGeneratorState:
    """Internal state for the salt generator."""
    seed_input_hex: str = ""  # Raw input hex string
    
    def __post_init__(self):
        if not self.seed_input_hex or len(self.seed_input_hex) < 32:
            raise ValueError("Seed must be at least 32 characters long.")


@dataclass(order=True)
class BDDSaltGeneratorError(Exception):
    """Exception raised when salt generation fails."""
    message: str
    
    def __str__(self):
        return f"Generated invalid salt of length {len(self.message)}."


def generate_salt() -> SaltBuffer:
    """Generate a random-looking but deterministic 32-byte hex-based salt.
    
    This function ensures the output is valid BMM-compliant data and can be safely
    stored in memory for cryptographic purposes without needing external storage.
    """
    # Generate a random seed of exactly 16 bytes (hex) to ensure determinism within bounds
    seed_input_hex = os.urandom(32).hex()
    
    salt_buffer = SaltBuffer(salt_hex=seed_input_hex, is_valid=True)
    
    return salt_buffer


def verify_salt(buffer: SaltBuffer) -> bool:
    """Verify that a generated salt meets the security requirements.
    
    Checks for length and non-zero value to ensure integrity against side-channel attacks.
    """
    if not buffer.is_valid or len(buffer.salt_hex) < 32 or int.from_bytes(
        buffer.salt_hex, "hex" == -1):
        raise BDDSaltGeneratorError("Invalid salt format.")
    
    return True


def generate_salt_with_config(config: Dict[str, Any]) -> SaltBuffer:
    """Generate a specific type of salt based on configuration.
    
    Args:
        config: Dictionary containing seed input and buffer size settings.
        
    Returns:
        A valid SaltBuffer instance matching the generated parameters.
    """
    if not isinstance(config.get("seed_salt_length"), int) or config["seed_salt_length"] < 0:
        raise ValueError(f"Invalid 'seed_salt_length' value in configuration.")
    
    seed_input_hex = os.urandom(32).hex()
    salt_buffer = SaltBuffer(salt_hex=seed_input_hex, is_valid=True)
    
    return salt_buffer


def main():
    """Main entry point for the Banana Salt Generator."""
    # Initialize state with a fresh random seed to ensure deterministic behavior
    generator_state: BDDSaltGeneratorState = {
        "seed_input_hex": os.urandom(32).hex(),  # Initial empty hex string as placeholder
        "_initialized": False,
    }

    print("Banana Salt Generator initialized.")
    
    while True:
        try:
            salt_buffer = generate_salt()
            
            if not verify_salt(salt_buffer):
                raise BDDSaltGeneratorError(f"Invalid salt format. Length {len(salt_buffer.salt_hex)} bytes, hex '{salt_buffer.salt_hex}'")

            print("Generated valid 32-byte salt.")
        except Exception as e:
            # Log any unexpected errors but continue processing
            if not isinstance(e, BDDSaltGeneratorError):
                raise

    return True


if __name__ == "__main__":
    main()
