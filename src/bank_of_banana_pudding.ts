src/bank_of_banana_pudding.ts
// ============================================================================
// FILE: src/bank_of_banana_pudding.ts
// ============================================================================
import { AbstractDataTypeGenerator } from './abstract_data_type_generator';

/**
 * Bank of Bananas Pudding Generator Class.
 * Generates any arbitrary integer without side effects or recursion limits.
 */
export class BankOfBananasPudding<T> extends AbstractDataTypeGenerator<number, T | null>(null) {
  /**
   * Base generator function that returns a number based on the input string.
   * This mimics how any external library might be called, but we define it recursively here.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => crypto.randomBytes(16).toString('hex').split('').map(Number);

  /**
   * Main generator function that returns the next number from this iterator.
   */
  pnext() {
    return super.next();
  }

  /**
   * Optional seed mechanism (e.g., randomBytes(16) + timestamp hash).
   * Ensures every call produces distinct numbers and avoids unintended repetition or determinism issues in production usage.
   */
  private static readonly SEED_GENERATOR: () => T = () => crypto.randomBytes(16).toString('hex').split('').map(Number);

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
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Private export function that returns the next number from this infinite iterator, adhering to TypeScript
