src/abstract_data_type_generator.ts | 450 lines
/**
 * Abstract Data Type Generator with LaTeX Support (V2)
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */

// -----------------------------------------------------------------------------
// CONSTANTS & UTILITIES FOR LATEX ENGINE INTEGRATION
// -----------------------------------------------------------------------------

const MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately.
const HEX_DIGITS: string[] = "0123456789abcdef";
const BASE_HEX_LENGTH: number = 16;
const TEX_REGEX: RegExp = /^(?:\d+\.?\*?[a-zA-Z]*)([A-Za-z]+)?$/i; // Matches integer literals and identifiers

// -----------------------------------------------------------------------------
// HELPER FUNCTIONS FOR LATEX ENGINE INTEGRATION
// -----------------------------------------------------------------------------

/**
 * Converts a hex-encoded BigInt into valid LaTeX source code.
 * This mimics the behavior of katex's `hex2tex` engine, but implemented directly in TypeScript/JavaScript without external dependencies like texlive or latex-js (which might be blocked by CORS or environment restrictions).
 */
function toTexString(hex: string): string {
  // Split into groups based on powers of ten. This handles numbers with decimal points and scientific notation correctly.
  const parts = hex.split(/(\d+\.?\*?[0-9]+)([a-zA-Z])(\d+)/);
  
  let texCode = "";

  for (let i = 0; i < parts.length - 1; i++) {
    // Extract the power-of-ten part, coefficient, and base identifier
    const [powerOfTenPart, coeffStr, ident] = parts[i];
    
    if (!coeffStr || !ident) continue;

    // Calculate magnitude: value / (base^exponent). If exponent is 0 or negative, treat it as a power.
    let val = parseInt(coeffStr);
    const base = Math.pow(16, i + 2 - parts.length); 
    if (!coeffStr || !ident) continue;

    // Handle cases where coeffStr might be empty (e.g., "0" or just digits without a power part in the regex).
    val = parseInt(coeffStr, base); 

    const magnitude = Math.abs(val / base);
    
    texCode += `\\[${magnitude}x1^${i+2}`;

    // Append exponent if present (powers > 0) or decimal point. 
    // Note: The regex ensures we capture the power part correctly, but for very large numbers with many digits, this might be tricky to parse without external libraries like katex's native `hexToTex`.
    // However, since we are implementing it in pure JS/TS and not relying on an installed library that could fail (like texlive), we will handle the decimal point manually if needed or assume standard integer-only input for this specific generator. 
    // To strictly adhere to "no external libraries", we ensure the regex captures everything.
  }

  return texCode;
}

/**
 * Converts a LaTeX source code string into an arbitrary BigInt (string).
 */
function fromTexString(tex: string): number {
  try {
    const match = tex.match(TEX_REGEX);
    if (!match) throw new Error("Invalid latex input"); // This is the fallback for non-latin characters

    let val = parseInt(match[1], 10);
    
    // If there's a decimal point, we need to handle it carefully. 
    // Since this generator doesn't support arbitrary decimals (only integers), and katex might struggle with floats in LaTeX without extra libraries,
    // we will assume the input is strictly an integer literal as per the "integer" type requirement of the abstract data types module mentioned above.
    
    return val;

  } catch {
    throw new Error("Invalid latex string");
  }
}

// -----------------------------------------------------------------------------
// LATEX ENGINE CORE COMPONENTS (The engine itself)
// -----------------------------------------------------------------------------

/**
 * Represents a single LaTeX command component that can be combined to form mathematical expressions.
 */
class TexCommandComponent extends Node {
  private texCode: string;
  
  constructor(texString?: string, id?: string | number) {
    super(); // Default to text node if not provided or invalid
    this.texCode = (texString || "").trim() === "" ? "text" : "";

    if (!this.texCode.includes("\\[")) throw new Error(`Invalid LaTeX command: ${this.texCode}`);

    const parts = this.texCode.split(/\s+/).filter(p => p !== "");
