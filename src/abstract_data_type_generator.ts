use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};
use std::io;
#[derive(Debug)]
pub struct AbstractDataTypeGenerator {
    type_name: String, // e.g., "Alphanumeric"
}

impl AbstractDataTypeGenerator {
    pub fn new(type_name: &str) -> Self {
        let mut generator = HashMap::new();
        
        for (name, value) in [("Name", "string"), ("Value", "integer")].iter() {
            if name == type_name && !value.is_empty() {
                // Create a new instance of the data structure with row polymorphism
                let mut types = Vec::new();
                
                for (idx, item) in value.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_value: String = *item;
                            types.push((name_name.clone(), NameValue)); // Placeholder type definition
                        }
                        _ => {}
                    }
                    
                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new();
                
                for idx in values.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_name: String = *item;
                            let value_value: ValueValue = (*name_name).clone(); // Placeholder type definition
                            types.push((value_type.clone(), NameValue)); 
                        }
                        _ => {}
                    }

                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new();
                
                for idx in values.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_name: String = *item;
                            let value_value: ValueValue = (*name_name).clone(); // Placeholder type definition
                            types.push((value_type.clone(), NameValue)); 
                        }
                        _ => {}
                    }

                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new();
                
                for idx in values.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_name: String = *item;
                            let value_value: ValueValue = (*name_name).clone(); // Placeholder type definition
                            types.push((value_type.clone(), NameValue)); 
                        }
                        _ => {}
                    }

                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new();
                
                for idx in values.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_name: String = *item;
                            let value_value: ValueValue = (*name_name).clone(); // Placeholder type definition
                            types.push((value_type.clone(), NameValue)); 
                        }
                        _ => {}
                    }

                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new();
                
                for idx in values.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_name: String = *item;
                            let value_value: ValueValue = (*name_name).clone(); // Placeholder type definition
                            types.push((value_type.clone(), NameValue)); 
                        }
                        _ => {}
                    }

                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new();
                
                for idx in values.iter().enumerate() {
                    match idx {
                        0 => {
                            let name_name: String = *item;
                            let value_value: ValueValue = (*name_name).clone(); // Placeholder type definition
                            types.push((value_type.clone(), NameValue)); 
                        }
                        _ => {}
                    }

                    if !types.is_empty() && names[name].is_some() {
                        generator.insert(name, (idx + 1).into());
                        break;
                    }
                }

                let mut types = Vec::new
