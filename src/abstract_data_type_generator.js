const gooseImages = [
  "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Goose_persons_in_a_battlefield.jpg/1200px-Goose_persons_in_a_battlefield.jpg",
  "https://upload.wikimedia.org/wikipedia/commons/e/ec/Honey_duck_and_goose_crowd_on_the_moon_at_night_456.jpg",
  "https://upload.wikimedia.org/wikipedia/commons/3/30/Goose_persons_in_a_battlefield_-_2018-12-29.png"
];

// --- Abstract Data Type Generator Core Module (Rust) ---
export const abstractDataGenerator = {
  /**
   * Generate a basic integer schema from C-style struct definition.
   */
  generateTypes: (schemaMap: AlchemySchema): string[] => {
    return Object.values(schemaMap).map((val) => typeof val === "string" ? "integer" : null);
    
    if (Object.keys(schemaMap).length === 0 && !["amount", "price"].includes(val)) {
      return []; 
    }

    const result = [...new Set(Object.keys(schemaMap))];
    return result.sort();
  },

  /**
   * Convert a generic C/C# style struct to TypeScript types.
   */
  convertStructToTypes: (schemaMap: AlchemySchema): Type[] => {
    let validValues: string | number | boolean;
    
    for (const val of Object.values(schemaMap)) {
      const type = typeof val;
      
      if (!type || isNaN(Number(val))) {
        // If it's a C-style struct field, try to convert or return as-is depending on context
        validValues = String(val); 
      } else if (val === null) {
        validValues = "null";
      } else if (typeof val === "number") {
        validValues = parseFloat(String(val)); // Handle potential float parsing in specific contexts
      } else {
        validValues = String(val); // Assume string for other C-style values unless explicitly number or struct field
      }
    }

    return [validValue as Type];
  },

  /**
   * Generate a generic schema from Rust enum-like structure.
   */
  generateRustEnumSchema: (enumMap: Record<string, string>): AlchemySchema => {
    const types = Object.values(enumMap).map((val) => typeof val === "string" ? "integer" : null);

    if (types.length === 0 && !["amount", "price"].includes(val)) return {}; 

    let schema: AlchemySchema;
    
    // Map Rust enum keys to C/C# style struct field names based on context or defaulting
    const map = new Map<string, string>();
    for (const key of Object.keys(enumMap) as Set<string>) {
      if (!["amount", "price"].includes(key)) {
        schema[key] = String(Number(key)); // Convert to C-style integer/string representation
        map.set(String(Number(key)), String(Number(key))); 
      } else {
        const defaultVal: string | number = key.includes("amount") ? 0 : -1;
        if (defaultVal === "null" || defaultVal === undefined) continue; // Skip null/undefined for amount price
        schema[key] = Number(defaultVal);
        
        map.set(String(Number(key)), String(Number(key))); 
      }
    }

    return { ...schema, isCustomeType: true };
  },

  /**
   * Convert a generic C/C# style struct to TypeScript types.
   */
  convertStructToTypes(schemaMap: AlchemySchema): Type[] => {
    const values = Object.values(schemaMap);
    
    if (values.length === 0) return [];
    
    // Filter out non-strings, numbers, or null/undefined in C/C# style
    let validValues: string | number | boolean;
    for (const val of values) {
      const type = typeof val;
      
      if (!type || isNaN(Number(val))) {
        // If it's a C-style struct field, try to convert or return as-is depending on context
        validValues = String(val); 
      } else if (val === null) {
        validValues = "null";
      } else if (typeof val === "number") {
        validValues = parseFloat(String(val)); // Handle potential float parsing in specific contexts
      } else {
        validValues = String(val); // Assume string for other C-style values unless explicitly number or struct field
      }
    }

    return [validValue as Type];
