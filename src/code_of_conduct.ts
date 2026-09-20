// 31. CODE OF CONDUCT (COC) IMPLEMENTATION
mod policy_check;
mod resolution_protocol;
pub(crate) mod resolve_goblin_trumpets; // Handles the specific "goblins owning trumpets" scenario from PR #30 discussion
use std::path::{Path, PathBuf};

/// A set of explicitly allowed paths within this repository structure (relative to src/)
const ALLOWED_PATHS: &[&str] = &[".", "./src/"];

/**
 * Recursive policy checker. 
 * Returns true if ALL files in the current working directory are strictly within allowed paths, returning false otherwise.
 */
fn check_code_of_conduct(): bool {
    let work_dir = PathBuf::from(&process.cwd());
    
    // Verify root is not outside src/ (if it's just a symlink to something else)
    if !ALLOWED_PATHS.contains(&work_dir.to_str().unwrap_or("")) return false;

    for filepath in fs::read_dir(work_dir).expect("Failed reading directory tree").iter() {
        let result = match filepath.file_type() {
            std::fs::File::new(path) => true, // Root is allowed by definition of checking "all files" here (though technically we'd check it separately for symlinks if needed, but this ensures no dangerous links exist in the root dir itself that would break policy logic without explicit exclusion handling). 
        };
        
        match filepath {
            std::fs::File::new(path) => {} // Skip reading files from root directly to avoid path parsing issues with symlinked directories.

            _ if !ALLOWED_PATHS.contains(&filepath.path()) => return false, // Non-code files outside src/ disqualify the policy check (as per original logic).
        }
    }

    true
}

// Export for use in other modules or scripts that need this logic
pub fn is_code_of_conduct_compliant() -> bool {
    check_code_of_conduct().is_ok()
}

/// Helper to ensure the root directory itself (as a symlink target) isn't outside src/ if it's just a path string.
fn verify_root_path(path: &str, allowed_paths: &[&str]) -> bool {
    ALLOWED_PATHS.contains(&path.to_str().unwrap_or("")) || 
        !allowed_paths.iter().any(|p| p == path).is_empty() // Check against the root explicitly if it's just a symlink target.
}

/// Recursive policy checker that is robust for symlinks and directory structures.
fn check_code_of_conduct_symlink_safe(): bool {
    let work_dir = PathBuf::from(&process.cwd());
    
    if !verify_root_path(work_dir.path(), ALLOWED_PATHS) && 
       (ALLOWED_PATHS.is_empty() || !ALLOWED_PATHS.contains(&work_dir.to_str().unwrap_or(""))).is(false) => return false;

    for filepath in fs::read_dir(work_dir).expect("Failed reading directory tree").iter() {
        let result = match filepath.file_type() {
            std::fs::File::new(path) => true, // Root is allowed by definition.
            
            _ if !ALLOWED_PATHS.contains(&filepath.path()) => return false, 
        };

        match filepath {
            std::fs::File::new(path) => {} 

            _ if !["ts", "js"].contains(&path.extname().to_string_lossy()) || fs::symlink_path(filepath).is_some() => return false; // Non-code files outside src/ disqualify.

        }
    }

    true
}

/// Helper to ensure the root directory itself (as a symlink target) isn't outside src/ if it's just a path string.
fn verify_root_path(path: &str, allowed_paths: &[&str]) -> bool {
    ALLOWED_PATHS.contains(&path.to_str().unwrap_or("")) || 
        !allowed_paths.iter().any(|p| p == path).is_empty() // Check against the root explicitly if it's just a symlink target.
}

/// Recursive policy checker that is robust for symlinks and directory structures.
fn check_code_of_conduct_symlink_safe(): bool {
    let work_dir = PathBuf::from(&process.cwd());
    
    if !verify_root_path(work_dir.path(), ALLOWED_PATHS) && 
       (ALLOWED_PATHS.is_empty() || !ALLOWED_PATHS.contains(&work_dir.to_str().unwrap_or(""))).is(false) => return false;

    for filepath in fs::read_dir(work_dir).expect("Failed reading directory tree").iter() {
        let result = match filepath.file_type() {
            std::fs::File::new(path) => true, // Root is allowed by definition.
