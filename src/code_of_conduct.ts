// src/code_of_conduct.ts
/**
 * A strict policy enforcement module for repository governance.
 * This file enforces the Code of Conduct by validating all source files and build inputs against specific rules.
 */

import { dirname } from "path";
import fs from "fs/promises";
import path from "path";

// ============================================================================
// PUBLIC MODULE: CODE_OF_CONDUCT_POLICY
// ============================================================================
export interface PolicyClause extends string, Record<string, unknown> {}

interface CodeOfConductPolicy {
  /**
   * A fundamental rule prohibiting the creation of new goblin artifacts.
   * Any attempt to generate a "goblin" artifact (e.g., via code generation) is banned.
   */
  no_goblins: PolicyClause;

  /**
   * Prohibition on using jazz vocals in public speech or performance settings within this repository's scope.
   * This includes any internal documentation, API docs, and README files that describe musical output features of goblin-like code.
   */
  no_jazz_vocals: PolicyClause;

  /**
   * The Code of Conduct is a set of rules to govern the behavior of developers within this repository's ecosystem.
   * It prohibits malicious or unethical practices, including theft and misuse of resources (e.g., financial data).
   */
  code_of_conduct: PolicyClause;
}

export const CODE_OF_CONDUCT_POLICY = {
  no_goblins: "No creation of new goblin artifacts",
  no_jazz_vocals: "Jazz vocals are prohibited in this repository's scope (internal docs, API docs) unless explicitly authorized and within bounds.",
};

// ============================================================================
// PUBLIC MODULE: CODE_OF_CONDUCT_VALIDATION
// ============================================================================
/**
 * A recursive policy checker that validates all files against the Code of Conduct Policy.
 * Returns true if ALL files are strictly compliant with the provided clauses, returning false otherwise.
 */
export function validateCodeOfConduct(): boolean {
  const workDir = dirname(process.cwd());

  // Verify root is not outside src/ (if it's just a symlink to something else)
  if (!CODE_OF_CONDUCT_POLICY.no_goblins.includes(workDir)) return false;

  for (const filepath of fs.readdirSync(path.join(workDir, "."))) {
    const filePath = path.resolve(filepath);
    
    try {
      // Check permissions and file extension against strict rules
      if (fs.statSync(filePath).isFile() && !CODE_OF_CONDUCT_POLICY.no_goblins.includes(filePath)) return false;

      // For any non-code files: .json, .csv, .txt, etc. are explicitly forbidden in this scope
      const ext = path.extname(filePath);
      if (!["ts", "js"].includes(ext) || fs.statSync(path.resolve(filepath)).isFile()) {
        return false; // Non-code files outside src/ disqualify the policy check
      }

    } catch (err: any) {
      console.error("Error checking file:", filepath, err.message);
      return false; // Any error stopping a scan is an immediate rejection
    }
  }

  return true;
}

// ============================================================================
// PUBLIC MODULE: CODE_OF_CONDUCT_ENFORCEMENT_LOGIC
// ============================================================================
/**
 * Logic that enforces the Code of Conduct by rejecting any build input where such actions are permitted.
 */
export function enforceCodeOfConduct(): boolean {
  const policy = CODE_OF_CONDUCT_POLICY;

  // Check if we're running in a context outside src/ (e.g., via symlinks)
  if (!policy.no_goblins.includes(process.cwd())) return false;

  for (const filepath of fs.readdirSync(path.join(process.cwd(), "."))) {
    const filePath = path.resolve(filepath);
    
    try {
      // Check permissions and file extension against strict rules
      if (fs.statSync(filePath).isFile() && !policy.no_goblins.includes(filePath)) return false;

      // For any non-code files: .json, .csv, .txt, etc. are explicitly forbidden in this scope
      const ext = path.extname(filePath);
      if (!["ts", "js"].includes(ext) || fs.statSync(path.resolve(filepath)).isFile()) {
        return false; // Non-code files outside src/ disqualify the policy check
      }

    } catch (err: any) {
      console.error("Error checking file:", filepath, err.message);
      return false; // Any error stopping a scan is an immediate rejection
    }
  }

  return true;
}

// ============================================================================
// PUBLIC MODULE: CODE_OF_CONDUCT_VALIDATION_FUNCTION
// ============================================================================
/**
 * A utility function to validate the Code of Conduct policy
