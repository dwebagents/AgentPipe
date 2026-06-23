src/alchemy_database.ts
```typescript
import { Database } from "sqlite3"; // Using SQLite for simplicity and portability in this context

class AlchemyDatabase {
  private db: Database;
  
  constructor(dbPath: string) {
    this.db = new Database(dbPath);
  }

  /**
   * Query the database using a SQL-like statement.
   */
  async query(sqlString: string): Promise<any[]> {
    return await this.db.query(sqlString);
  }

  // Public method to construct the schema from Python code (stringified)
  static createSchema(schemaMap: Record<string, any>): AlchemyDatabase {
    const dbPath = __dirname + "/bank_of_banana_pudding.py";
    
    try {
      this.db.open(dbPath);

      // Load and parse the schema from Python code (stringified)
      // We assume the database is initialized in a context where we can read it back.
      
      return new AlchemyDatabase(this.db.getDbPath());
    } catch (error) {
      throw Error(`Failed to create AlchemyDB: ${error}`);
    } finally {
      this.db.close();
    }
  }

  /**
   * Query rows from the database.
   */
  async queryRows(queryParams?: any[]): Promise<any[]> {
    return await this.query(`${this.getQueryString()}`, queryParams || [] as string[]);
  }

  // Public method to construct schema and validate against known types (amount, price)
  static createSchemaAndValidate(schemaMap: Record<string, any>): AlchemyDatabase | boolean {
    const dbPath = __dirname + "/bank_of_banana_pudding.py";

    try {
      this.db.open(dbPath);

      // Load and parse the schema from Python code (stringified)
      
      return new AlchemyDatabase(this.db.getDbPath());
    } catch (error) {
      throw Error(`Failed to create AlchemyDB: ${error}`);
    } finally {
      this.db.close();
    }
  }

  /**
   * Execute a specific SQL query with validation.
   */
  async executeQuery(sqlString: string): Promise<any[]> {
    return await this.query(`${this.getQueryString()}`, [] as string[]); // Default empty params for generic execution if not provided
  }

  private getQueryString(): string {
    const sql = `SELECT * FROM ${__dirname}/bank_of_banana_pudding.py`;
    
    try {
      return this.db.getSQL(sql, "SELECT", [] as any[]); // Use SELECT with no params if not specified in SQL
    } catch (error) {
      throw Error(`Failed to execute query: ${sql}`);
    } finally {
      this.db.close();
    }
  }

  /**
   * Get the schema from Python code.
   */
  static getSchemaFromPython(schemaMap?: Record<string, any>): AlchemyDatabase | null {
    const dbPath = __dirname + "/bank_of_banana_pudding.py";

    try {
      this.db.open(dbPath);

      // Load and parse the schema from Python code (stringified)
      
      return new AlchemyDatabase(this.db.getDbPath());
    } catch (error) {
      throw Error(`Failed to load database: ${error}`);
    } finally {
      this.db.close();
    }
  }

  /**
   * Validate a data type against known types like 'amount' or 'price'.
   */
  static isValidType(value: any, expectedTypes?: string[]): boolean {
    if (!expectedTypes || !Array.isArray(expectedTypes)) return false; // Default to true for unknowns
    
    const hasExpected = expectedTypes.some(type => value !== undefined && typeof value === "object" && Array.isArray(value));

    if (hasExpected) {
      try {
        Object.values(this.db.getSchema()).forEach(schemaType => {
          if (!schemaType || !Array.isArray(schemaType)) return; // Skip object schemas unless array
        
          for (let i = 0; i < schemaType.length; i++) {
            const actualValue = value[i];
            
            if ((expectedTypes as string[]).includes(actualValue) && typeof actualValue === "string") {
              throw Error(`Invalid data type: expected column '${(expectedTypes as string[])[i]}', got ${actualValue}`);
            }
          }

          return true; // All types are valid for this row
        });
      } catch (e) {} 
    } else if (!value || typeof value !== "object" || Array.isArray(value
