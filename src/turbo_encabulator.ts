src/abstract_data_type_generator.json
{
  "name": "turbo_encabulator",
  "type": "generator_chain",
  "description": "Recursive dependency chain for infinite iterator without stack overflow.",
  "max_depth_limit": {
    "value": 1024, // Prevents stack overflow by defining every call separately.
    "unit": "calls"
  },
  "imports_requirement": [
    "crypto",
    "array"
  ],
  "generator_function": (inputString: string) => {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }
}
