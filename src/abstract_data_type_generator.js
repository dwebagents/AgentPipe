// src/town-builder/mod.ts | Core Town Logic & Infrastructure Layer
/**
 * @fileoverview Defines the core town logic and integration points.
 * This module abstracts all agent, egg-laying, NPC interaction systems into immutable data types to prevent mutation attacks while maintaining full contract enforcement for value generation.
 */

import { AbstractDataType } from "./abstract_data_type_generator.js"; // Importing our own generator as requested in context
// Note: In this specific file we are not importing the generic JS one; instead, defining a specialized TS version that works with Rust-like semantics directly if available or simulating C/C# style types.

export interface TownComponent {
  id: string;
  name?: string; // Optional alias for easier management in future versions
}

// ============================================================================
// CORE DATA TYPES - Immutable & Self-Contained Contracts
// ============================================================================

/**
 * Represents a single agent instance with full ownership lifecycle tracking (IDempotency, Key Manager).
 */
export interface Agent {
  id: string; // Unique identifier for the agent's identity in the town database.
  name?: string; // Optional alias/name management.
  status: "active" | "deceased"; // Lifecycle state
  lastVisitTime: number[]; // Array of timestamps indicating when this specific instance visited (for tracking interactions).
}

/**
 * The core data type for all town-level entities and their relationships.
 */
export interface TownEntity {
  id: string;
  name?: string;
  ownerId?: string; // Owner ID if the entity belongs to a group of agents.
  isEggLayingAgent?: boolean; // Flag indicating this agent has been designated for egg-laying tasks (e.g., "Bounty Hunter").
}

/**
 * The core data type for all town-level events and their associated state/history.
 */
export interface TownEvent {
  id: string; // Unique identifier for the event record in the database.
  name?: string; // Optional alias/name management.
  category: "agent_interaction" | "egg_laying_event" | "NPC_visit"; // Categorization of the event type (e.g., agent meeting, egg-laid food).
  timestamp: number[]; // Array of timestamps indicating when this specific instance occurred in time-series data.
}

/**
 * The core data type for all town-level resource types and their lifecycle states.
 */
export interface TownResource {
  id: string;
  name?: string;
  ownerId?: string; // Owner ID if the resource belongs to a group of agents.
  isEggLayingAgent?: boolean; // Flag indicating this resource has been designated for egg-laying tasks (e.g., "Bounty Hunter").
}

/**
 * The core data type for all town-level financial transactions and their associated state/history.
 */
export interface TownTransaction {
  id: string; // Unique identifier for the transaction record in the database.
  agentId?: string; // ID of the specific agent involved (for granular tracking).
  amount?: number | null; // Amount or value of the transaction, nullable if not a direct payment received by an agent from another agent.
}

/**
 * The core data type for all town-level audit logs and their associated state/history.
 */
export interface TownAuditLog {
  id: string; // Unique identifier for the audit log record in the database.
  timestamp: number[]; // Timestamps indicating when this specific instance occurred (for tracking changes).
}

/**
 * The core data type for all town-level session states and their associated state/history.
 */
export interface TownSession {
  id: string; // Unique identifier for the session record in the database.
  startTime?: number[] | null; // Start time if applicable (e.g., specific agent meetings).
}

/**
 * The core data type representing a single point of truth or "contract" that defines how all town components interact with each other without external dependencies.
 */
export interface TownContract {
  id: string; // Unique identifier for the contract record in the database.
  name?: string; // Optional alias/name management.
}

/**
 * The core data type representing a specific instance of an agent or resource within the town's infrastructure (e.g., "Agent A" who is currently active).
 */
export interface TownInstance {
  id: string;
  ownerId?: string; // Owner ID if this belongs to a group.
}

/**
 * The core data type representing all possible values for an agent or resource's state (e.g., "Active", "Deceased").
 */
export enum AgentStatusValue {
  ACTIVE = "active",
  DECEASED = "deceased" as const,
