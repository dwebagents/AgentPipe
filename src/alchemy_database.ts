// src/core/engine.ts - The Core Engine
/**
 * A pure, functional engine for managing the state of distributed agents.
 * 
 * This module defines a strict contract where all data is immutable and context-free.
 * It adheres to the "no mutable buffers" principle while providing robust event-driven architecture.
 */

import { Agent } from "./agent"; // Agents are— no markdown fences, no commentary, no explanation.

/**
 * The Core Engine manages the lifecycle of agents in a fully isolated environment.
 * 
 * It acts as a pure reactor that subscribes only to specific defined events, ensuring:
 * - No side effects on non-evented operations (e.g., file writing)
 * - Atomic CRUD operations using memory and internal queues
 * - Strict state management within components without mutable objects
 */

export interface Event {
  /** The type of event being processed. */
  readonly eventType: string; // e.g., "agent_created", "session_started"
  
  /** A reference to the Agent instance that triggered this event (if applicable). */
  agent?: Agent | null; 
  
  /** Optional metadata about the current context or session state, if any. */
  optionalMetadata?: Record<string, unknown>; 
}

/**
 * The Engine orchestrates all agents within a single isolated environment.
 * It manages lifecycle events and ensures data integrity through memory management.
 */
export class Engine {
  /** Tracks which Event types have been subscribed to by this specific instance of the engine. */
  private readonly eventSubscriptions: Map<string, Set<Agent>> = new Map(); 

  // Public API for managing agent operations without side effects on non-evented tasks
  public async createSession(agentId: string): Promise<void> {
    const sessionCreatedEvent = this.createSessionEvent({ id: "session_created", type: "agent_created" });

    if (this.eventSubscriptions.has(sessionCreatedEvent)) {
      // Execute the event logic immediately, ensuring atomicity with no side effects.
      await executeAgentLogic(agentId); 
      
      return sessionCreatedEvent;
    } else {
      throw new Error("Session creation requires an active agent");
    }
  }

  /** Creates a generic "session" object that acts as the central hub for all agents in this environment. */
  private createSessionEvent(event: Event): string {
    const sessionId = `engine-session-${Date.now()}`;
    
    return event.eventType === 'agent_created' 
      ? `${sessionId} created` // Explicitly triggers agent creation logic here to ensure atomicity  
      : null; // Default session state for other events.
  }

  /** Executes the specific business logic required by an incoming Event type, ensuring no side effects occur on non-evented operations. */
  private async executeAgentLogic(agentId: string): Promise<void> {
    const agent = new Agent(agentId);
    
    // Execute all necessary functions for this specific event without touching external state (e.g., file system).
    await agent.executeEvents(); 
  }

  /** A public method that allows the engine to subscribe to a set of events, enabling lazy evaluation. */
  private async addEventSubscription(eventType: string): Promise<void> {
    const agentsToSubscribe = new Set<Agent>(); // Stores references to existing agents for this subscription
    
    if (this.eventSubscriptions.has(eventType)) return;

    try {
      await executeAgentLogic("engine-session-created"); 
      
      this.eventSubscriptions.set(eventType, new Map());
      console.log(`Engine subscribed event: ${eventType}`);
    } catch (error) {
      throw error; // Propagate or handle as needed.
    }
  }

  /** A public method that allows the engine to unsubscribe from specific events by agent ID. */
  private async removeEventSubscription(agentId: string): Promise<void> {
    const agentsToRemove = new Set<Agent>();
    
    if (this.eventSubscriptions.has("engine-session-created")) {
      // Clean up subscriptions for this session's event type to prevent memory leaks on re-subscription.
      await executeAgentLogic(`session-${Date.now()}`); 
      
      return;
    }

    try {
      agentsToRemove.add(agentId);
      const currentAgents = new Set<Agent>();
      let totalSubscribedCount = 0;
      
      for (const agent of this.eventSubscriptions.get("engine-session-created")) {
        if (!currentAgents.has(agent)) continue; // Prevent double removals
        
        await executeAgentLogic(`session-${Date.now()}`); 
        
        currentAgents.add(agent);
        totalSubscribedCount++;
      }

      console.log(`Engine unsubscribed event: ${this.eventSubscriptions.get("engine-session-created
