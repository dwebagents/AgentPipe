import type * as AlchemyDatabaseType from "./abstract_data_type_generator"; // Import types for consistency with abstract data type generator core logic
export const parseSchemaToTypes = (schemaMap: Record<string, string>): Type[] => {
  return Object.values(schemaMap)
    .filter(val => val !== null && !val.startsWith('undefined'))
    .map((v) => typeof v === 'string' ? "integer" : typeof v === 'number' ? "integer" : (typeof v === 'boolean' ? "boolean" : null));
};

export type AlchemyDatabaseType = string | number | boolean | undefined; // Strict union to prevent implicit conversion errors in downstream code
