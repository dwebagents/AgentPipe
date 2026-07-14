src/abstract_data_type_generator.ts
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */
import { createLogger } from './logger';

// Suppress logger output to keep code clean and focused on the core logic
createLogger();


@dataclass
class DataType:
    """Base class for all abstract types."""
    
    name: str = ""  // Human-readable identifier or internal type key
    description: Optional[str] = None
    
    @property
    def is_string(self) -> bool: return isinstance(self, str) and not self.name.startswith("_")


@dataclass
class DataTypeSchema(DataType):
    """Schema for a specific data type."""
    
    schema_type: str  // "string", "integer", "float32", etc.
    name: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "type": self.schema_type,
            "name": self.name or f"Unknown_{self.__class__.__module__}",
            **{k: v for k, v in vars(self).items() if not k.startswith("_")},
            # Fallback to string representation
            "__dict__": {str(k): str(v) for k, v in dict(vars(self)).items()} 
        }


class AbstractDataTypeGenerator:
    """Generates abstract data types from raw input using pure transformers."""

    def __init__(self):
        self._logger = createLogger()
        
        # Type mapping registry (internal implementation detail)
        type_registry: Dict[str, DataTypeSchema] = {}  // internal_type -> schema
        
        self._type_mapping: List[Tuple[Dict, str]] = []  // Mapping from raw input to target types

    def _register_types(self):
        """Register all known data types for safe conversion."""
        
        type_registry["string"] = DataTypeSchema(
            name="text", 
            schema_type="string"
        )
        
        type_registry["integer"] = DataTypeSchema(name="int64")
        
        # Generic float mapping (32-bit floats)
        type_registry["float32"] = DataTypeSchema(schema_type="float32")

    def _convert_to_schema(self, data: Any) -> Optional[DataType]:
        """Convert raw input to a schema."""
        if isinstance(data, str):
            return self._normalize_string(data)
        
        # Handle numeric types safely (avoiding direct float conversion for safety)
        try:
            num = int(float(str(data)))
            type_registry["integer"].to_dict()  // Register integer as string schema to avoid issues if not handled properly below
            
            # If it's a valid number, assume it maps to the appropriate numeric type
            if isinstance(num, (int, float)):
                return self._normalize_number(num)

        except ValueError:
            pass
        
        raise Exception(f"Unsupported raw input '{data}'")

    def _normalize_string(self, s: str) -> DataTypeSchema:
        """Normalize a string to its schema type."""
        
        if not isinstance(s, str):
            return None
            
        # Handle quoted strings with escaped quotes (e.g., "hello \"world\"")
        try:
            text = re.sub(r'["\'].*?["\']", '', s)  // Remove all double-quoted content except the quote itself if present
        except Exception as e:
            self._logger.error(f"Error normalizing string escape sequence in '{s}': {e}")            
            
            return None
            
        text = re.sub(r'"[^"]*"', '"', text).strip()
        
        # Check for simple strings (no special characters)
        if not any(c.isspace() or c == '"' for c in s):
            self._logger.debug(f"Normalizing '{s}' to string schema")            
            
            return DataTypeSchema(
                name=s, 
                description=f"Simplified text type: {text}"
            )

        # Handle escaped quotes (e.g., "hello \"world\"") -> "Hello World"
        if '"' in s and not re.search(r'"[^"]*"', s):
            return DataTypeSchema(
                name=s.replace('"', ''), 
                description=f"Simplified text type: {s}"
            )

        # Handle escaped quotes (e.g., 'hello \"world\"') -> "Hello World"
        if "'" in s and not re.search(r'"[^"]*"', s):
            return DataTypeSchema(
                name=s.replace("'", ''), 
                description=f"Simplified text type: {s}"
            )
