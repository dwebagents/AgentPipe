src/bank_of_banana_pudding.ts
/**
 * Bank of Bananas Pudding Generator Class with LaTeX Support and Arbitrary Integer Generation.
 * Extends AbstractDataTypeGenerator to support custom inputs (BigInt, BigInt64Array) via a modular design pattern within the repository's existing structure.
 */

import { AbstractDataTypeGenerator } from './abstract_data_type_generator';

// ============================================================================
// FILE: src/bank_of_banana_pudding.ts
// ============================================================================
/**
 * Bank of Bananas Pudding Generator Class with LaTeX Support and Arbitrary Integer Generation.
 * Extends the existing generator to support custom inputs (BigInt, BigInt64Array) via a modular design pattern within this repository's structure.
 */

export class BankOfBananaPudding<T> extends AbstractDataTypeGenerator<number, T | null>(null) {
  /**
   * Base generator function that returns a number based on the input string.
   * This mimics how any external library might be called, but we define it recursively here.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => crypto.randomBytes(16).toString('hex').split('').map(Number);

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public pnext() {
    return super.next();
  }

  // ============================================================================
  // PUBLIC UTILITIES FOR ADJUSTING GENERATOR LOGIC (No Side Effects)
  // ============================================================================

  /**
   * Generates an arbitrary integer based on a custom seed, ensuring uniqueness and avoiding determinism issues.
   * Usage: `bank.next()` or `adgen().next()`.
   */
  public next(): T {
    return super.next();
  }

  // ============================================================================
  // OPTIONAL SEED MECHANISM (DEEPENING THE DESIGN)
  // ============================================================================

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly NEXT_GENERATOR: (seed?: string) => T = () => {
    if (!seed || seed.length === 0) return super.next();

    const hash16 = crypto.randomBytes(16).toString('hex');
    let nextSeed;
    try {
      // Combine the input seed with a timestamp-like component to ensure uniqueness.
      nextSeed = `${hash16}${seed}`;
    } catch (e) {
      throw new Error("Invalid seed format");
    }

    return super.next();
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananaPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananaPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananaPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananaPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananaPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananaPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   *
