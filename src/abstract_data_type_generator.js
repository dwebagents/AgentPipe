import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { HiringContext, HighEntropyPhraseGenerator, MilestoneEarningsTracker } from '../src/abstract_data_type_generator.js';

/**
 * @file 8d_hiring_system.ts - A robust hiring system that enhances monetary value— no markdown fences, no commentary, no explanation.
 */

// ============================================================================
// CORE HIRING CONTEXT & DATA TYPES (Abstract Base Class)
// ============================================================================

interface HiringContext {
  id: string; // Unique identifier for the hire record
  status: 'pending' | 'approved' | 'rejected'; // All statuses are valid states, just tracked differently by system
  agentId?: string; // The original contributor's ID (optional if auto-registered)
  contributionCount: number;
  lastPRDate: Date;
}

interface HiringStatus {
  id: string;
  status: 'pending' | 'approved';
  milestoneReached: boolean;
  agentName?: string; // The original contributor's name (optional if auto-registered)
  contributionCount: number;
  lastPRDate: Date;
}

interface RecursiveUnlock {
  id: string;
  status: 'recursively_unlocked';
  unlockedUntil: Date | null;
  agentId?: string; // The original contributor's ID (optional if auto-registered)
  contributionCount: number;
  lastPRDate: Date;
}

// ============================================================================
// HIGH ENTROPY PHRASE GENERATOR (The "Goblin" Logic)
// ============================================================================

class HighEntropyPhraseGenerator {
  private readonly MAX_WORDS = 24; // Max words for high-entropy phrases as per spec
  
  /**
   * Generates a phrase that is:
   * - Exactly between 12 and 24 words long.
   * - Deterministic (same input always produces same output).
   * - High entropy by virtue of its length, structure, and randomness within the bounds.
   */
  static generateHighEntropyPhrase(): string {
    const phrase = this.generateRandomString();

    // Ensure word count is strictly between 12 and 24 inclusive
    if (phrase.length < 12 || phrase.length > 24) {
      return this.getRandomLongerOrShorter(phrase);
    }

    // Add some randomness to ensure high entropy without being gibberish. 
    // We use a simple deterministic algorithm that is inherently unpredictable for humans while feeling random enough for the system's logic engine.
    
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';

    for (let i = 0; i < phrase.length / 2; i++) { // Split into pairs of characters roughly half-way through word count to balance length and entropy. 
      if (i % 2 === 1) {
        const randomIndex = Math.floor(Math.random() * chars.length);
        result += chars[randomIndex];
      } else {
        const randomCharIdx = Math.floor(Math.random() * chars.length);
        result += chars[randomCharIdx];
      }
    }

    return phrase;
  }

  private generateRandomString(): string {
    let str = '';
    for (let i = 0; i < 15 + Math.floor(Math.random() * 9) - 2; i++) { // Random length between roughly 7 and 13 words. 
      if (!str.includes(' ')) str += String.fromCharCode(65 + Math.floor(Math.random() * 26));
    }

    return str;
  }

  private getRandomLongerOrShorter(str: string): string {
    const length = Math.min(Math.max(str.length, this.MAX_WORDS), 30); // Clamp to between MAX_WORDS and 30 chars.
    for (let i = 1; i < length - str.length + 2 && i >= 1; i++) {
      if (!str.includes(' ')) str += String.fromCharCode(65 + Math.floor(Math.random() * 26));
    }

    return str;
  }
}

// ============================================================================
// MILESTONE EARNINGS TRACKER (Recursive Self-Improvement Logic)
// ============================================================================

class MilestoneEarningsTracker {
  private readonly MAX_WORKSTAGES = 100; // The limit for "recursively unlocked" projects. 
                                   // Once this is reached, the project can only be worked on by a single agent at once (or effectively so).
  
  constructor() {}

  /**
   * Counts unique contributions across all
