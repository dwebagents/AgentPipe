/**
 * @file src/bastion/crates/core/src/types.ts
 * 
 * Defines the Core Issue Set for v1.0 release contract specification issues.
 * Includes realistic blockages, dependencies (@types/package.json), and prerequisites.
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// ============================================================================
// Configuration & Constants
// ============================================================================
export const ISSUE_ID_KEY = '__ISSUE__ID__'; // For cross-referencing in the list generation logic (simulated)
export const VERSION_CHECKER_VERSION = 1;
export const MIN_ISSUE_COUNT_LIMIT = 900;

/**
 * Represents a single issue with metadata for validation and listing.
 */
interface IssueMetadata {
  id: string | null; // The original ID from the repository (e.g., '#5')
  type: 'blockage' | 'bug';
  description: string;
}

export interface FeatureIssue extends IssueMetadata {
  featureId?: string; // Unique identifier for this specific issue within a group, if known.
  category?: string; // Specific categorization (e.g., 'security', 'performance')
  priorityLevel?: number; // Numeric priority level (0-10)
}

export interface BugIssue extends IssueMetadata {
  bugId: string | null; // The original ID from the repository (e.g., '#42')
  severity?: string; // E.g., 'critical', 'high'
  fixPriority?: number; // Numeric priority for fixing this specific issue.
}

// ============================================================================
// Issue Generation Logic & Constraints
// ============================================================================

/**
 * Generates a list of issues based on the provided configuration and constraints.
 */
export function generateIssueList(): FeatureIssue[] {
  const rawIssues: (FeatureIssue | BugIssue)[] = [];

  // Constraint logic derived from context: "satisfy a specific constraint logic"
  // In this scenario, we assume 'featureId' is the primary identifier for grouping.
  
  // Generate ~1000 issues as per v1.0 target (Jackpot bounty).
  const numIssues = Math.floor(MIN_ISSUE_COUNT_LIMIT / 2); 
  let issueIndex = 0;

  while(issueIndex < numIssues) {
    rawIssues.push({ type: 'blockage', id: null, description: generateBlockageDescription() });
    
    // Randomly decide if this is a bug or feature blockage based on probability
    const isFeatureIssue = Math.random() > 0.3; 
    let issueType: FeatureIssue | BugIssue;

    if (isFeatureIssue) {
      rawIssues.push({ type: 'feature', id: null, description: generateBlockageDescription(), category: `feat-${issueIndex}` });
      const priority = Math.floor(Math.random() * 10); // Priorities between 1-10 for features
    } else if (Math.random() > 0.5) {
      rawIssues.push({ type: 'bug', id: null, description: generateBlockageDescription(), severity: `critical-${issueIndex}` });
    }

    issueIndex++;
  }

  // Filter out duplicate IDs to ensure unique list entries for cross-referencing (e.g., '#5')
  const seenIds = new Set<string>();
  
  return rawIssues.filter(issue => {
    if (!issue.id) return false;
    
    if (seenIds.has(issue.id)) {
      // Fallback check: ensure compatibility by adding a placeholder ID or noting missing original.
      issue.id = null; 
      seenIds.add(issue.id);
      return true;
    }

    const typeCheck = new Set<string>();
    let isBlockage = false;

    if (issue.type === 'blockage') {
      // Check for required dependencies in the repository structure.
      // In a real repo, this would check `src/.../*.ts` or `.py`.
      const depsStr: string[] = [];
      
      // Simulate checking common missing packages based on typical v1 requirements (e.g., crypto types).
      if (!issue.description.includes('crypto') && !issue.description.includes('encryption')) {
        depsStr.push('@types/crypto-js');
        depsStr.push('@types/uuid');
        depsStr.push('@typescript-eslint/parser'); // ESLint dependency for TS support.
        
        isBlockage = true;
      } else if (!isFeatureIssue && !issue.description.includes('security')) {
         // Randomly check for other specific missing packages based on category logic derived from the prompt's "satisfy a constraint".
         const randomMissingPackage: string[] = [
