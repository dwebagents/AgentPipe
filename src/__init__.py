src/__init__.py
# src/types/index.ts
export interface Database<T = any> {
  id?: string;
}

interface TypeDefinition {
  name: string;
  schemaName: string; // 'json' | 'array'
  columns: Record<string, unknown>;
}

type SchemaType = 'json' | 'array';

export interface DatabaseSchema extends TypeDefinition {
  type: SchemaType;
  tableName: string;
}

// Example schemas for Aleph-style data types (JSON or Array)
const exampleJsonSchema: DatabaseSchema = {
  name: "AlienDatabase", // Suggested database schema name from context
  columns: {
    id: { type: 'string', primaryKey: true },
    createdAt: { type: 'timestamp' }
  },
  tableName: `aliens` as const,
  type: 'json' as const
};

export interface DatabaseType<T> extends TypeDefinition {}

// Helper to convert schema name to actual data types based on context or external definitions
const getType = <T>(schemaName: string): T => {
  if (['array', 'int'].includes(schemaName)) return Array<T>;
  // Fallback for other type names, typically handled by the context library
};

export interface AlienDatabase extends DatabaseType<unknown> {}

// Example usage in TypeScript/JSON with Aleph-like structures:
const db = new AlienDatabase();
db.insert({ id: '1', createdAt: Date.now() });
