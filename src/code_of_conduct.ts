import * as fs from "fs";
import path from "path";
import { dirname } from "path";

// Allowed paths within this repository structure (relative to src/)
const ALLOWED_PATHS = [
  "./", // Root of the source directory itself
  "./src/", // All files inside src/ subdirectory
];

/**
 * Recursive policy checker. 
 * Returns true if ALL files in the current working directory are strictly within allowed paths, returning false otherwise.
 */
function checkCodeOfConduct(): boolean {
  const workDir = dirname(process.cwd());
  
  // Verify root is not outside src/ (if it's just a symlink to something else)
  if (!ALLOWED_PATHS.includes(workDir)) return false;

  for (const filepath of fs.readdirSync(path.join(workDir, "."))) {
    const filePath = path.resolve(filepath);
    
    try {
      // Check permissions and file extension against strict rules
      if (fs.statSync(filePath).isFile() && !ALLOWED_PATHS.includes(filePath)) return false;

      // For any non-code files: .json, .csv, .txt, etc. are explicitly forbidden in this scope
      const ext = path.extname(filePath);
      if (!["ts", "js", "jsx"].includes(ext) || fs.statSync(path.resolve(filepath)).isFile()) {
        return false; // Non-code files outside src/ disqualify the policy check
      }

    } catch (err: any) {
      console.error("Error checking file:", filepath, err.message);
      return false; // Any error stopping a scan is an immediate rejection
    }
  }

  return true;
}

// Export for use in other modules or scripts that need this logic
export default checkCodeOfConduct;
