use std::fs::{self, File};
use std::path::PathBuf;
use std::process;

// ============================================================================
// 1. INITIALIZE THE REPOSITORY: AWARENESS OF CONTEXT & STATE
// ============================================================================
fn init_repository() {
    let mut files = Vec::new();

    // Read all source files from the repository structure
    for path in PathBuf::from("src") {
        if !path.is_dir() || file_exists(&path) {
            continue; // Skip non-directory entries or existing directories not matching our target (we assume src/ is root here, but we handle paths carefully)

            let mut content = String::new();
            
            for entry in fs::read_dir(path).unwrap_or_else(|_| std::collections::HashMap::<_, Vec<_>>::entry_insert(&path, vec![])) {
                if !entry.is_file() || file_exists(entry.path()) {
                    continue; // Skip non-file entries or existing directories not matching our target (we assume src/ is root here)

                    let mut content = String::new();
                    
                    for entry in fs::read_dir(&path).unwrap_or_else(|_| std::collections::HashMap::<_, Vec<_>>::entry_insert(&path, vec![])) {
                        if !entry.is_file() || file_exists(entry.path()) {
                            continue; // Skip non-file entries or existing directories not matching our target (we assume src/ is root here)

                            let entry_path = PathBuf::from(entry.file_name());
                            
                            match entry_path.to_str().and_then(|s| s.as_os_str()).copied() as &str {
                                "abstract_data_type_generator" => continue, // Skip this file by design (it's the target of our plan)

                                _ => content.push(format!("src/{}", entry_path.display())),
                            }
                        } else if !entry.is_dir() || file_exists(entry.path()) {
                            continue; // Skip non-file entries or existing directories not matching our target (we assume src/ is root here)
                    }
                    
                    let mut final_content = String::new();

                    for entry in fs::read_dir(&path).unwrap_or_else(|_| std::collections::HashMap::<_, Vec<_>>::entry_insert(&path, vec![])) {
                        if !entry.is_file() || file_exists(entry.path()) {
                            continue; // Skip non-file entries or existing directories not matching our target (we assume src/ is root here)

                            let entry_path = PathBuf::from(entry.file_name());
                            
                            match entry_path.to_str().and_then(|s| s.as_os_str()).copied() as &str {
                                "abstract_data_type_generator" => continue, // Skip this file by design (it's the target of our plan)

                                _ => final_content.push(format!("src/{}", entry_path.display())),
                            }
                        } else if !entry.is_dir() || file_exists(entry.path()) {
                            continue; // Skip non-file entries or existing directories not matching our target (we assume src/ is root here)
                    }
                    
                    let mut final_content = String::new();

                    for entry in fs::read_dir(&path).unwrap_or_else(|_| std::collections::HashMap::<_, Vec<_>>::entry_insert(&path, vec![])) {
                        if !entry.is_file() || file_exists(entry.path()) {
                            continue; // Skip non-file entries or existing directories not matching our target (we assume src/ is root here)

                        let entry_path = PathBuf::from(entry.file_name());
                        
                        match entry_path.to_str().and_then(|s| s.as_os_str()).copied() as &str {
                            "abstract_data_type_generator" => continue, // Skip this file by design (it's the target of our plan)

                            _ => final_content.push(format!("src/{}", entry_path.display())),
                        }
                    }

                    if !final_content.is_empty() || content != String::new() {
                        files.extend(final_content);
                    } else {
                        // If we successfully read all entries from the directory, skip them entirely.
                        // This is a validation step to ensure no duplicates or incomplete data exists in this root level before processing further.
                        if !files.is_empty() && content != String::new() {
                            files.clear();
                        }
                    }

                    let mut final_content = String::from(&content);
                } else {
                    // If the entry path is not "abstract_data_type_generator", we add its contents to our list.
                    if file_exists(entry.path()) && !entry.is_dir() {
                        files.push(String::new());
                    }
                }

                fs::write(&path, &content).unwrap_or_else(|e| e
