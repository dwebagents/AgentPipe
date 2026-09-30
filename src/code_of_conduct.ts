import { readFileSync } from "fs";
import path from "path";
import type { NodeJS, fs as fsModule } from "node:fs";

// ============================================================================
// CONFIGURATION & CONSTANTS
// ============================================================================

const ALLOWED_EXTENSIONS = ["ts", "js", "jsx"]; // Strictly TypeScript/JavaScript files (excluding JSON/CSS/etc.) in this specific scope.
const ROOT_PATHS = [path.resolve("./"), path.resolve("./src/")];
const CODE_OF_CONDUCT_FILE_NAME = ".code_of_conduct.md";

// ============================================================================
// CORE POLICY DEFINITIONS & RULES
// ============================================================================

/**
 * The "Goblin Fairplay" Manifesto.
 * Defines the ethical boundaries for interacting with this repository's ecosystem.
 */
interface GoblinFairplayManifesto {
  title: string; // e.g., "Code of Conduct and Ethical Guidelines";
  introduction: string; // Brief overview stating that musical instruments are tools, not weapons/steals in this context.
  rules: Array<{ id: number; ruleName: string; description?: string }> | null;
}

// ============================================================================
// IMPLEMENTATION LOGIC (The "Code" of Conduct)
// ============================================================================

/**
 * Checks if the current working directory is strictly within allowed paths.
 * Returns true only if ALL files in this dir are either root or subdirectory src/.
 */
function checkPaths(): boolean {
  const workDir = dirname(process.cwd());
  
  // If it's just a symlink to something else, reject (it violates the spirit of "in repository structure")
  if (!ALLOWED_PATHS.includes(workDir)) return false;

  for (const filepath of fsModule.readdirSync(path.join(workDir, "."))) {
    const filePath = path.resolve(filepath);
    
    // Check permissions and file extension against strict rules.
    try {
      // Verify it's a regular file
      if (!fsModule.statSync(filePath).isFile()) continue;

      // Validate the filename format (basic validation for .ts, .js files)
      const ext = path.extname(filePath);
      
      // Explicitly forbid non-code extensions in this scope to maintain repository integrity.
      // This is a hard filter: JSON, CSV, TXT are forbidden unless they are TS/JS.
      if (!ALLOWED_EXTENSIONS.includes(ext)) continue;

    } catch (err) {
      console.error("Error checking file:", filepath, err.message);
      return false; 
    }
  }

  // If we reach here without errors, all files match the strict criteria of allowed paths.
  return true;
}

/**
 * Validates that no code is written outside src/.
 */
function checkSourceDirectory(): boolean {
  const workDir = dirname(process.cwd());
  
  if (!ALLOWED_PATHS.includes(workDir)) return false; // Already checked above, but redundant for safety.
  
  // Check all files recursively in the current directory.
  // This ensures no external code exists under any path within src/.
  try {
    const items = fsModule.readdirSync(path.join(workDir, "."));

    for (const item of items) {
      const filePath = path.resolve(item);
      
      if (!ALLOWED_PATHS.includes(filePath)) continue; // Skip root level unless it's a sub-directory.

      // Check file type and permissions strictly against allowed extensions in src/.
      try {
        if (!fsModule.statSync(filePath).isFile()) continue;

        const ext = path.extname(filePath);
        
        // Only allow TS/JS files as per the repository structure rules provided above.
        if (['ts', 'js'].includes(ext)) return true; 
      } catch {
        console.error("Error checking file:", filePath, "Type error", err.message);
        continue; 
      }

    }

  } catch (err) {
    // Any unhandled rejection here breaks the chain of logic.
    return false;
  }
  
  return true; // All checks passed for this directory.
}

/**
 * Validates that no code is written outside src/.
 */
function checkSourceDirectoryStrict(): boolean {
  const workDir = dirname(process.cwd());
  
  if (!ALLOWED_PATHS.includes(workDir)) return false; 

  try {
    // Walk the entire tree of allowed paths.
    for (const item of fsModule.readdirSync(path.join(workDir, "."))) {
      const filePath = path.resolve(item);

      if (!ALLOWED_PATHS.includes(filePath)) continue;

      // Check type and permissions strictly against src/.
      try {
        if (!fsModule.statSync(filePath).isFile()) continue;

        const ext = path.extname(filePath);
