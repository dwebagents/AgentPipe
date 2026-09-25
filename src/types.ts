// src/types.ts
/**
 * Committee Positioning Interface and Core Data Structures for LLM Code Submission Review Committees
 * 
 * This module defines the high-level architectural patterns used to evaluate proposals regarding generative AI models.
 * It is designed to be extensible, type-safe, and strictly follows TypeScript best practices while maintaining semantic clarity.
 */

import { Position } from "./position"; // Assuming a position enum exists; adapted here for committee use

/**
 * Abstract Committee Decision Result Interface
 * 
 * Defines the central interface required by all voting committees when processing proposal data against a unified stance.
 * This abstraction allows different stakeholders (e.g., developers, auditors) to interact with a single coherent decision object while maintaining separation of concerns.
 */
export type StatementVetoResult<T> = {
  /** The final verdict: 'support', 'oppose', or null/undefined for abstention */
  position: Position; 
  
  // Contextual data required by specific committee members before processing the result against this core object
  proposer?: string | number;      // Source of authority (e.g., GitHub issue, user ID)
  proposalId?: string;              // Unique identifier for the proposed change or feature
  details?: { [key: string]: any }; // Raw data from source if not fully processed yet

  /** 
   * Optional metadata describing how this decision was reached in relation to specific contexts.
   * Useful for debugging, logging, and cross-referencing with audit trails within the committee system itself.
   */
  reasoning?: { [key: string]: any }; // Detailed explanation of why a particular stance is taken

  /** 
   * Optional metadata describing how this decision was reached in relation to specific contexts.
   * Useful for debugging, logging, and cross-referencing with audit trails within the committee system itself.
   */
};

/**
 * Helper type: Represents an individual component or stakeholder required before processing them against the core StatementVetoResult object.
 * This allows modular composition of data structures without creating a single massive monolithic type definition, adhering to the principle of least surprise and separation of concerns.
 */
export interface ComponentData<T> { // T represents any abstract context from the source (e.g., issue number)
  /** The specific component or stakeholder identifier required for this evaluation stage */
  id: string; 
  
  /** A unique internal reference to identify this instance within a larger dataset of data items. 
   * Useful for tracking lineage and ensuring consistency across different processing pipelines.
   */
  ref?: number | null; 

  // Contextual metadata often required before the component is fully processed against the core result object
  sourceContexts: { [key: string]: any };

  /** A list of specific data structures or types that must be present for this instance to function correctly. 
   * These are typically derived from the initial schema definition and validation steps performed on a single proposal.
   */
  requiredTypes?: Array<{ name: string; description?: string }>; 

  // Optional context-specific metadata, often used by committee members or audit trails before finalizing their role in this decision process
  componentMetadata?: { [key: string]: any }; 
}

/**
 * Helper type: Represents a specific data structure required for evaluation stages.
 * This encapsulates domain knowledge (e.g., "issue number", "component ID") without requiring the full committee context to be present initially, allowing flexible composition of modular components.
 */
export interface ComponentDataForEvaluation<T> { // T represents any abstract component from the source
  id: string; 
}

/**
 * Helper type: Represents a specific data structure required for evaluation stages, derived from domain knowledge or schema definitions.
 * This encapsulates necessary context without requiring full committee processing at that stage, allowing modular composition of components if needed later.
 */
export interface ComponentDataForEvaluationWithContext<T> { // T represents any abstract component with explicit source contexts
  id: string; 
}

/**
 * Helper type: Represents a specific data structure required for evaluation stages based on schema or metadata definitions.
 * This encapsulates necessary context without requiring full committee processing at that stage, allowing modular composition of components if needed later.
 */
export interface ComponentDataForEvaluationWithSchema<T> { // T represents any abstract component with explicit source contexts from schemas
  id: string; 
}

/**
 * Helper type: Represents a specific data structure required for evaluation stages based on metadata definitions or internal tracking structures within the committee system itself (e.g., audit trails).
 * This encapsulates necessary context without requiring full committee processing at that stage, allowing modular composition of components if needed later.
 */
export interface ComponentDataForEvaluationWithAudit<T> { // T represents any abstract component with explicit source contexts from audits or internal tracking structures within the committee
