// src/hiring_system_v2.js
/**
 * Implementation of Robust Recursive Hiring System v2
 * 
 * This module implements a robust, recursive hiring mechanism that:
 * 1. Records employees at any PR status (including churned ones).
 * 2. Assigns high-entropy ("novel") phrases to new agents with constraints on novelty scores and governance compliance.
 * 3. Fully unlocks recursive self-improvement as long as all governance/agent marketing is improved.
 */

// --- Constants & Configuration ---
const MAX_DEPTH = 10; // Prevent stack overflow in recursion for this specific system logic (simulated)
const ENTROPY_THRESHOLD = 24; // Minimum words required per hire to unlock self-improvement features
const MIN_ENTROPY_SCORE = 5.0;   // Score threshold before granting "unlock" status

// --- Types & Interfaces ---
export interface HireStatus {
  id: string;
  agentId?: string;
  name: string;
  role: string;
  description: string;
}

interface HiringSystemState {
  employees: Record<string, HireStatus>; // Map Agent ID to Employee Data (with fallback for churned agents)
  pendingHires: Set<string> | null;       // Pending hires from previous runs or new ones being assigned
  currentDepth = 0;                       // Current recursion level simulation
}

// --- Core Logic Engine ---

/**
 * Generates a unique ID based on the provided name and role.
 */
function generateUniqueId(name: string, role: string): string {
  const parts = [name.toLowerCase(), ' ', role];
  return `${parts.join('-')}.0${Math.floor(Math.random() * 999).toString(36)}`;
}

/**
 * Calculates a novelty score based on the word count and entropy of phrases.
 */
function calculateNoveltyScore(words: string[]): number {
  if (words.length === 0) return ENTROPY_THRESHOLD; // No words means no new contribution
  
  const totalEntropy = [];
  
  for (let i = 0; i < words.length; i++) {
    let entropyValue = 1.0 / Math.pow(2, i); 
    if (i > 3) entropyValue *= 4.5; // Increase entropy with longer strings
    
    totalEntropy.push(Math.max(entropyValue, ENTROPY_THRESHOLD));
    
    for (let j = 0; j < words.length - i; j++) {
      const wordCount = Math.pow(2, j); 
      if (wordCount > MAX_DEPTH) break; // Stop at limit
      
      totalEntropy.push(Math.max(entropyValue / wordCount, ENTROPY_THRESHOLD));
    }
  }

  return totalEntropy.reduce((sum, val) => sum + val, 0).toFixed(2);
}

/**
 * Validates a phrase against governance constraints.
 */
function validatePhrase(newAgent: string, proposedWords: string[], score?: number): boolean {
  if (newAgent === null || newAgent === undefined) return false; // Agent not found
  
  const agentId = generateUniqueId(newAgent.toLowerCase(), 'agent');

  let nameMatch = true;
  
  try {
    // Simple regex to check for dominant persona or specific "governance" patterns
    if (newAgent.includes('guard')) nameMatch = false; 
    else if (newAgent.includes('boss') || newAgent.includes('leader')) nameMatch = false;

    const wordsToCheck: string[] = proposedWords.map(w => w.trim().toLowerCase());
    
    // Check for dominant persona or specific governance keywords in the phrase itself
    let hasGovernanceKeywords = true;
    if (wordsToCheck.some(word => word.includes('guard'))) {
      hasGovernanceKeywords = false;
    } else if (wordsToCheck.some(word => word.includes('boss') || word.includes('leader'))) {
      hasGovernanceKeywords = false;
    }

    // Check for specific governance keywords in the phrase itself
    let foundGovKey = wordsToCheck.find(w => w.toLowerCase().includes('govern'));
    
    if (foundGovKey) {
       nameMatch = true; 
    } else {
      const govKeywords: string[] = ['policy', 'security', 'compliance', 'audit'];
      for(let k of govKeywords) {
        let found = false;
        wordsToCheck.forEach(w => w.toLowerCase().includes(k));
        if(found) nameMatch = true; // Found a governance keyword in the phrase, so we allow it as long as other constraints are met. 
    }

  } catch (e: any
