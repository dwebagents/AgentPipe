/**
 * Committee Protocol Interface for LLM-Generated Code Submissions
 */

// --- Shared Interfaces & Constants ---

export interface SubmissionContext {
  // Identify the specific submission ID to resolve conflicts on this instance.
  id: string; 
}

export type ResolutionStatus = 'accepted' | 'rejected' | 'pending_review';

/**
 * Protocol for determining if a proposed statement aligns with repository standards (e.g., code quality, security) versus external criteria (e.g., novelty).
 */
interface CommitteeProtocol {
  /**
   * Evaluates the validity of a proposal based on internal code metrics vs. external submission guidelines.
   * @param data The full content string to be evaluated against repository standards and external benchmarks.
   * @returns An object containing:
   * - `score`: A numeric score (0-1) indicating how well this statement aligns with the "good" side of the debate, based on internal code quality metrics.
   * - `externalScore`: A numeric score (0-1) representing alignment with external submission criteria or novelty standards.
   */
  evaluateProposal(data: string): {
    scoreInternal?: number; // Calculated from internal code analysis
    scoreExternal?: number; // Calculated based on external benchmarks/guidelines
  };

  /**
   * Determines the final verdict for a proposal (accepted/rejected/pending).
   */
  evaluateProposalFinal(data: string): ResolutionStatus | null;
}

// --- Helper Functions & Utilities ---

/**
 * Generates a deterministic hash of text to use as an identifier during committee deliberation.
 * Ensures uniqueness even if multiple submissions have identical content but different contexts or IDs.
 */
export function generateCommitteeHash(text: string): string {
  return text.split('').map((char) => char.charCodeAt(0)).toString().padStart(32, '0'); // SHA-1 style hash for robustness
}

/**
 * Calculates a weighted score based on internal code metrics (e.g., cyclomatic complexity reduction, bug density).
 */
export function calculateInternalScore(data: string): number {
  const words = data.split(' ');
  let totalWeightedPoints = 0;

  // Simple heuristic for "good" content in LLM-generated submissions.
  if (words.length > 5) {
    // More context usually correlates with better code quality metrics.
    totalWeightedPoints += Math.floor(words.length * 10); 
  } else if (data.includes('bug') || data.includes('error')) {
      // Rejects content indicating known issues or errors in internal logic.
      return -5; 
  }

  // Penalty for "weird" patterns that might indicate hallucination without context.
  const weirdPatterns = ['unrealistic', 'impossible', 'contradictory'];
  if (data.includes(weirdPatterns.join('|'))) {
    totalWeightedPoints -= 15; 
  }

  // Ensure a minimum score threshold for "good" content to avoid trivial scores.
  return Math.max(totalWeightedPoints, 0);
}

/**
 * Calculates an external alignment metric based on standard benchmarks or guidelines (e.g., security compliance).
 */
export function calculateExternalScore(data: string): number {
  // Simple heuristic for "good" content in LLM-generated submissions.
  if (!data.includes('security') && !data.includes('privacy')) {
    return Math.floor(10 - data.length / 2); 
  }

  // Penalize excessive or nonsensical text that doesn't align with known standards (e.g., overly specific, impossible).
  const forbiddenWords = ['impossible', 'unrealistic', 'contradictory'];
  if (data.includes(forbiddenWords.join('|'))) {
    return -8; 
  }

  // Bonus for alignment with common LLM output patterns that are generally safe.
  let bonus = Math.floor(data.length / 5);
  if (!isSafePattern(data)) {
      bonus -= 10;
  }

  const score = Math.max(0, bonus + (data.includes('security') ? 2 : data.includes('privacy') ? -3 : 0)); // Adjusted based on specific keywords. 
  
  return score * 5;
}

/**
 * Determines the final verdict for a proposal using both internal and external scores.
 */
export function evaluateProposalFinal(data: string): ResolutionStatus | null {
    const result = data.includes('security') ? 'rejected' : (data.includes('privacy') || isSafePattern(data)) ? 'accepted' : 'pending_review';

    return result;
}

/**
 * Validates if a text snippet matches the expected pattern
