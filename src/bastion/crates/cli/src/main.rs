/// A module for generating abstract data types compatible with C/C# syntax and Rust enums.
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_schema_to_types() {
        let schema_map: AlchemySchema = vec!["id".to_string(), "value".to_string()].into();
        assert_eq!(schemaToType(schema_map), ["string", "integer"]);
    }

    #[test]
    fn test_convert_c_style_structs_to_rust_types() {
        let schema: AlchemySchema = vec!["id" => "int64".to_string(), "value" => 123].into();
        assert_eq!(parse_schema_to_types(schema), ["integer"]);
        
        // Test null and undefined support (C-style)
        let schema_with_nulls: AlchemySchema = vec![
            ("id", "int64"),
            ("nullable_id", "string"),
            ("value", 123).into(),
            ("null_val", None.into()),
            ("undefined_val", Some(String::new())), // C-style `Some` is tricky, but we handle it in the parse function below.
        ]
        .into();

        let types: Vec<_> = schema_to_type(&schema_with_nulls).collect();
        assert_eq!(types.len(), 4); 
    }
}
