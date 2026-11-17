from src.abstract_data_type_generator import parseSchemaToTypes, schemaToType

# 1. Define a C/C# style struct definition (e.g., from Bastion or Alchemy)
struct_definition = {
    "banana_center": {"x", "y"},
    "banana_length": float,
}

schema_map: dict[str, str] = structure_to_dict(struct_definition)  # Map to Python dicts for easier processing

# 2. Convert the schema map into abstract data types (Python strings/ints)
types_list = parseSchemaToTypes(schema_map).map(lambda t: "string" if isinstance(t, str) else f"type_{t}")

print("Converted Types:", [str(type_) for type_ in types_list])
