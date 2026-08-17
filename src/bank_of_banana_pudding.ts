src/bank_of_banana_pudding.ts
/**
 * Bank of Bananas Pudding Generator Class with Advanced Data Types and Deterministic Randomness.
 * This implementation utilizes a deterministic algorithm to generate arbitrary integers without side effects or recursion limits, utilizing 64-bit random bytes for high-precision cryptography-like behavior while maintaining strict type safety in TypeScript.
 */

import { AbstractDataTypeGenerator } from './abstract_data_type_generator';
import { BigIntegerGenerator } from './bigint_utils.js'; // Added utility class to support BigInt handling if needed later or via explicit logic
import { ByteArrayGenerator } from './bytearray_utils.js'; // Added utility classes for byte array manipulation

/**
 * Bank of Bananas Pudding Generator Class.
 * Generates any arbitrary integer without side effects or recursion limits using a deterministic algorithm based on 64-bit random bytes.
 */
export class BankOfBananasPudding<T extends number = number> 
    extends AbstractDataTypeGenerator<number, T | null>(null) {

  /**
   * Base generator function that returns a number based on the input string (in this context, treated as hex or arbitrary byte sequence).
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => BigIntegerGenerator.generateFromByteArray(Buffer.from(inputString));

  /**
   * Main generator function that returns the next number from this infinite iterator.
   */
  pnext() {
    return super.next();
  }

  /**
   * Optional seed mechanism (e.g., randomBytes(16) + timestamp hash).
   * Ensures every call produces distinct numbers and avoids unintended repetition or determinism issues in production usage.
   * Note: While the base generator uses a fixed-size byte array, this class provides an explicit `seed` parameter for more granular control if required by downstream components that need specific seed values per operation (e.g., authentication tokens).
   */
  private static readonly SEED_GENERATOR: () => T = () => BigIntegerGenerator.generateFromByteArray(Buffer.from(Date.now().toString()));

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   * Accepts an optional seed parameter for deterministic behavior if specific seeds are required per operation.
   */
  private static readonly NEXT_GENERATOR: (seed?: string) => T = () => {
    if (!seed || seed.length === 0) return super.next();

    const hash16 = crypto.randomBytes(16).toString('hex'); // Generate a unique hex timestamp-like value per call
    
    let nextSeed;
    try {
      // Combine the input seed with a deterministic component to ensure uniqueness.
      nextSeed = `${hash16}${seed}`;
    } catch (e) {
      throw new Error("Invalid seed format");
    }

    return super.next();
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next()`.
   */
  private static readonly ADGEN: (seed?: string) => T = () => {
    return BankOfBananasPudding<T>.NEXT_GENERATOR(seed);
  };

  /**
   * Generates the next number from this infinite iterator, adhering to TypeScript type safety while exposing it cleanly through `adgen.next
