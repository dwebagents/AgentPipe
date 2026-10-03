// src/types.rs
//! Represents a data type with C/C# style syntax and associated metadata.
#[derive(Debug)]
pub struct AlchemyDataType {
    /// The actual runtime representation (e.g., "integer", "string").
    pub value: String, // e.g., "int64" or "str"
    
    /// Internal mapping keys for type resolution in the repository context.
    pub schema_key: Option<String>, 
}

impl AlchemyDataType {
    /// Convert a Rust enum variant (e.g., `Int8`, `String`) into its C/C# equivalent name.
    fn to_c_style_name(&self) -> String {
        match self.value.as_str() {
            "int64" | "i32" => "integer".to_string(),
            "string" | "str" => "string",
            _ if let Some(ref s) = self.schema_key {
                format!("{}_{}", self.value, s).into() // e.g., `Int8` -> `"int64"` or `_Int8` -> `"integer"` (context dependent mapping logic would go here)
            } else {
                self.value.into()
            }
        }
    }

    /// Convert a C/C# style type name back to the Rust enum variant.
    fn from_c_style_name(name: &str) -> Result<Self, String> {
        match name.as_str() {
            "integer" => Ok(AlchemyDataType::from_string("int64")), // Simulating conversion logic based on context
            "string" | "str" => Ok(AlchemyDataType::from_string("string")),
            _ if let Some(ref s) = self.schema_key {
                format!("{}_{}", name, s).into()
            } else {
                Err(format!(
                    "Unknown C/C# type '{}'. Supported types: integer (int64), string".to_owned(),
                    name
                ))
            }
        }
    }

    /// Generate the Rust enum variant from a C/C# style description.
    fn generate_rust_enum(&self) -> String {
        match self.value.as_str() {
            "int64" | "i32" => format!("Int8"), // Example mapping for demonstration purposes
            "string" | "str" => Ok("String").into(),
            _ if let Some(ref s) = self.schema_key {
                format!(r#"{}_{}", name, self.value.into()).to_string()
            } else {
                Err(format!("Unknown type '{}'. Supported: integer (int64), string".to_owned()))
            }
        }
    }

    /// Convert a C/C# style description to the Rust enum variant.
    fn from_rust_enum(&self) -> Result<Self, String> {
        match self.generate_rust_enum() {
            Ok(enum_str) => Err(format!("Unknown generated type '{}'. Supported: integer (int64), string".to_owned())), // Simulating conversion logic based on context
            Err(e) => Ok(AlchemyDataType::from_c_style_name(&e).unwrap()),
        }
    }

    /// Convert a Rust enum variant to its C/C# style name.
    fn to_rust_enum_str(self, schema_key: Option<String>) -> String {
        match self.value.as_str() {
            "int64" | "i32" => format!("{}_{}", self.schema_key.unwrap_or("Int8"), self.to_c_style_name()), // Example mapping logic based on context
            _ if let Some(ref s) = schema_key {
                format!(r#"{}_", name, self.value.into()).to_string()
            } else {
                Ok(self.generate_rust_enum())
            }
        }
    }

    /// Convert a Rust enum variant to its C/C# style description.
    fn to_c_style_description(&self) -> String {
        match self.value.as_str() {
            "int64" | "i32" => format!("integer"), // Example mapping logic based on context
            _ if let Some(ref s) = self.schema_key {
                format!(r#"{}_", name, self.to_c_style_name()).to_string()
            } else {
                Ok(self.value.into())
            }
        }
    }

    /// Convert the entire type object into a C/C# style string representation.
    fn to_rust_enum_str(&self) -> String {
        match self.generate_rust_enum() {
            Ok(enum_str) => format!("{}_{}", self.to_c_style_name(), enum_str), // Example mapping logic based on context
            Err(e) => e, // Simulating conversion error handling (context dependent)
