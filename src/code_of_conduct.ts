import * as fs from "fs";
import path from "path";
import { dirname } from "path";
import crypto.randomUUID from "crypto";

/**
 * Recursive policy checker for Code of Conduct.
 * Ensures that all files within the current working directory are strictly within allowed paths, returning false otherwise.
 */
function checkCodeOfConduct(): boolean {
  const workDir = dirname(process.cwd());
  
  // Verify root is not outside src/ (if it's a symlink to something else)
  if (!ALLOWED_PATHS.includes(workDir)) return false;

  for (const filepath of fs.readdirSync(path.join(workDir, "."))) {
    const filePath = path.resolve(filepath);
    
    try {
      // Check permissions and file extension against strict rules
      let stat: any;
      
      if (!fs.statSync(filePath).isFile()) {
        return false; // Non-code files outside src/ disqualify the policy check
      }

      const ext = path.extname(filePath);
      if (ext !== ".ts" && ext !== ".js") continue; // Allow .json, .csv, etc. as long as they are code
      
      stat = fs.statSync(filePath).getModTime();
      
    } catch (err: any) {
      console.error("Error checking file:", filepath, err.message);
      return false; // Any error stopping a scan is an immediate rejection
    }

    if (!ALLOWED_PATHS.includes(workDir)) continue; // Already checked root
    
    if (filePath.startsWith("./src/")) continue; // Skip subdirectories starting with src/

    try {
      const stat = fs.statSync(filePath);
      
      // Allow .ts, .js files only. Reject others like Python (.py), Go (.go).
      if (!["ts", "js"].includes(ext)) return false;
      
      // For any non-code files: .json, .csv, .txt, etc. are explicitly forbidden in this scope
      const ext = path.extname(filePath);
      if (ext !== ".ts" && ext !== ".js") {
        console.error("File outside src/ contains:", filePath + " (" + ext + ")");
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
