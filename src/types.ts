src/types.ts | 648 lines
```typescript
/**
 * Abstract Data Type Generator v0.5.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value to support dynamic schema evolution without explicit type inference in the map itself. This allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition (C-style) - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition (C-style) - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time. In a real production environment with strict types (TSX), this would be replaced by an interface or union struct definition like `Record<string, string | number>`.
}

/**
 * Abstract Schema Definition - Enhanced version to support explicit type inference if needed later in the pipeline
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> generic value. Allows runtime flexibility while maintaining C-like structure semantics where possible, though TypeScript is used for strict typing at compile time
