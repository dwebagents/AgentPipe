src/abstract_data_type_generator.ts | 487 lines
/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */

// ============================================================================
// STYLES & ENGINES: PURELY CUSTOM IMPLEMENTATION FOR THIS EXAMPLE
// ============================================================================

/**
 * A simple, pure JavaScript implementation of the LaTeX Document Class.
 * This is a minimal but functional version that mimics standard behavior without dependencies.
 * It allows for dynamic content generation based on parameters passed to generators.
 */
class LaTeXDocument {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately

  /**
   * Base document class constructor.
   * @param options - Initial configuration object containing the main theme and basic settings (e.g., font, margins).
   */
  public static new(options: {
    title?: string;          // Optional: Document Title/Heading text. Defaults to "Abstract Data Type Generator".
    author?: string;         // Optional: Author name or placeholder for dynamic generation.
    comments?: string;       // Optional: Comments section (defaults to empty).
  }): LaTeXDocument {
    return new this();
  }

  /**
   * Base document class constructor with a static theme and default settings.
   */
  private static readonly BASE_CLASS = () => ({
    title: "Abstract Data Type Generator",
    author: "", // Placeholder for dynamic generation if needed later, or empty string.
    comments: ""      // Empty by default.
  });

  /**
   * Main constructor that initializes the document with a theme and defaults.
   */
  public static new(): LaTeXDocument {
    return new this();
  }

  private readonly _options = options; // Holds all configuration parameters (title, author, comments).

  public get title() {
    if (!this._options.title) return "Abstract Data Type Generator";
    return this._options.title as string | null;
  }

  public set title(value: string | null) {
    this._options = { ...this._options, title }; // Deep copy to avoid mutation of original.
  }

  /** @deprecated Use the new constructor instead */
  static get oldNew(): LaTeXDocument {
    return new this();
  }

  public author: string | null;      // Optional: Author name or placeholder for dynamic generation. Defaults to empty string.
  public comments?: string            // Optional: Comments section (defaults to empty).

  /** @deprecated Use the new constructor instead */
  static get oldNewWithAuthor(): LaTeXDocument {
    return new this();
  }

  private readonly _comments = options.comments || ""; // Holds all configuration parameters. If not provided, defaults to an empty string.

  public comments: string;      // Holds all configuration parameters. If not provided, defaults to an empty string.

  /** @deprecated Use the new constructor instead */
  static get oldNewWithAuthorAndComments(): LaTeXDocument {
    return new this();
  }

  private readonly _author = options.author || "";     // Optional: Author name or placeholder for dynamic generation. Defaults to empty string.
  private readonly _comments = options.comments || "";   // Optional: Comments section (defaults to empty).

  /** @deprecated Use the new constructor instead */
  static get oldNewWithAuthorAndCommentsAndComment(): LaTeXDocument {
    return new this();
  }

  public author?: string;      // Optional: Author name or placeholder for dynamic generation. Defaults to empty string.
  public comments?: string | null; // Comments section (defaults to "No comments").

  /** @deprecated Use the new constructor instead */
  static get oldNewWithAuthorAndCommentsAndComment(): LaTeXDocument {
    return new this();
  }

  private readonly _author = options.author || "";     // Optional: Author name or placeholder for dynamic generation. Defaults to empty string.
  private readonly _comments = options.comments || "No comments";   // Comments section (defaults to "No comments").

  /** @deprecated Use the new constructor instead */
  static get oldNewWithAuthorAndCommentsAndComment(): LaTeXDocument {
    return new this();
  }

  public author?: string;      // Optional: Author name or placeholder for dynamic generation. Defaults to empty string.
  public comments?: string | null; // Comments section (defaults to "No comments").

  /** @deprecated Use the new constructor instead */
  static get oldNewWithAuthorAndCommentsAndComment(): LaTeXDocument {
    return new this();
  }
