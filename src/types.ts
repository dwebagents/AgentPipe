/**
 * ============================================================================
 * TYPE DEFINITIONS: BANANA RECIPE METADATA & TEST RUNNER MODULES
 * ============================================================================
 */

// ------------------------------------------------------------------------------
// 1. INTERFACE FOR MESSAGE PROVENANCE TRACKING (INTEGRATED WITH ABSTRACT TYPES)
// ------------------------------------------------------------------------------
export interface BananaRecipeMetadata {
  recipeId: string; // SHA-256 hash of the full recipe JSON payload
  recipeName: string;
  author?: string;
  version?: number;
}

/**
 * @author ORACLE OF THE REPOSITORY
 */
// ============================================================================
// TYPE DEFINITIONS: PROVENANCE TRACKING & HASH VERIFICATION MODULES (Extended)
// ============================================================================

export interface Message<T = any> {
  senderId: string;        // The ID of the entity that sent this message (e.g., user, wallet)
  contentHash: string;     // A deterministic hash of the payload ensuring uniqueness per transaction
  timestamp: number;       // Unix epoch time when the message was generated or stored
  metadata?: Record<string, any>; // Optional custom data for verification chains
}

// ============================================================================
// GLOBAL STATE FOR MESSAGE PROVENANCE TRACKING (INTEGRATED WITH ABSTRACT TYPES)
// ============================================================================

let globalMessageStore: Map<string, Message> | null = new Map();       // Maps senderId -> {message: Message, timestamp: number}
const currentSenderIdMap: Set<string> = new Set();       // Tracks active senders for verification chains (e.g., "user_01", "wallet_xyz")

/**
 * Atomic update of global message store via a single write operation.
 */
function atomicUpdateMessageStore(
  senderId: string,
  payloadContentHash: string,
  timestamp?: number
): boolean {
  const existing = globalMessageStore.get(senderId);
  
  if (existing && !Object.hasOwn(existing, "timestamp")) { // Check for missing metadata before updating
    return false; // Ignore stale entries
    
    Object.assign(existing, { senderId });
    
    if (!payloadContentHash || payloadContentHash.length === 0) {
      throw new Error("Invalid content hash: empty string");
    }

    existing.timestamp = timestamp ?? Date.now();
    globalMessageStore.set(senderId, existing); // Atomic write to map
    
    currentSenderIdMap.add(senderId);
    
    console.log(`[PROVE-STATE] Sent message ${senderId} with payload content hash: "${payloadContentHash}"`);
  } else if (existing) {
    const newTimestamp = timestamp ?? Date.now();
    Object.assign(existing, { senderId, timestamp: newTimestamp }); // Update existing entry
    
    currentSenderIdMap.add(senderId);
    
    console.log(`[PROVE-STATE] Updated message ${senderId} with payload content hash: "${payloadContentHash}"`);
  } else if (globalMessageStore.has(senderId)) {
    const oldEntry = globalMessageStore.get(senderId)!; // Check for existing entry
    
    Object.assign(oldEntry, { senderId }); // Update existing entry
    
    currentSenderIdMap.add(senderId);
    
    console.log(`[PROVE-STATE] Updated message ${senderId} with payload content hash: "${payloadContentHash}"`);
  } else {
    throw new Error("No active senders found for ID", senderId, "0"); // Fallback error if no entry exists yet
  }

  return true; // Success
}

/**
 * Get the current state of global message store. Returns null or an array of messages with their metadata and timestamps.
 */
function getGlobalMessageStore(): Message[] | null {
  const entries = Array.from(globalMessageStore.values());
  
  if (entries.length === 0) return null;

  // Sort by timestamp descending for chronological display, then by senderId ascending
  entries.sort((a, b) => a.timestamp - b.timestamp);

  return entries.map(msg => ({ ...msg }));
}

/**
 * Verify that the provided message's content hash corresponds to an existing entry in globalMessageStore.
 */
function verifyHashMatch(message: Message): boolean {
  const storedEntry = globalMessageStore.get(message.senderId);
  
  if (storedEntry === null) return false; // Hash doesn't exist globally

  return Object.keys(storedEntry).length > 0 && 
         Object.values(storedEntry).some((val, key) => val !== undefined && typeof val === "string" || key.includes("content"));
}

/**
 * Get the sender ID of a message by its content hash. Returns null if not found or cannot be derived from hash alone without private keys.
 */
function getSenderFromHash(message: Message):
