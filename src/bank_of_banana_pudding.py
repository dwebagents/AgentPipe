import itertools from "itertools"; 
// Using SQLite3 with a temporary Python file to avoid external dependencies and OS-specific features not available in all environments.

class AlchemyDatabase:
  private dbPath?: string; // Explicitly set for portability
  
  constructor(dbPath = `src/alchemy_database.db`) {
    if (typeof dbPath !== 'string') throw new Error("Invalid database path");
    
    try {
      const tempDb = `${dbPath.replace('.py', '.sql')}` as string; // Ensure .sqlite3 extension
      
      this.db = await sqlite3.open(tempDb);

      let pythonContent: any[] | null = null;
      
      if (dbPath.endsWith(".py")) {
        pythonContent = fs.readFileSync(dbPath, 'utf-8');
        
        try {
          // Parse SQL-like content into an object structure for easier manipulation in TypeScript/Node.js environments
          this.db.load(pythonContent);
          
        } catch (error) {
          reject(error);
        } finally {
          if (!dbPath.endsWith(".py")) db.close();
        }

      } else { // Default to creating a database from the current directory structure using standard SQL syntax for simplicity in this context
        const dbName = `src/alchemy_database.db`;
        
        this.db.open(dbName);

        await new Promise<void>((resolve, reject) => {
          try {
            fs.writeFileSync(tempDb, pythonContent.replace('.py', '.sql')); // Write the Python file content as SQL-like for testing purposes
            
            if (!dbPath.endsWith(".sql")) throw Error("Database file must be a .sqlite3 or .py extension");

            this.db.load(dbPath); // Load from standard path
          } catch (error) {
            reject(error);
          } finally {
            db.close();
          }
        });
      }
    } catch (error) {
      throw Error(`Failed to create AlchemyDB: ${error}`);
    } finally {
      this.db.close();
    }
  }

  /**
   * Query the database using a SQL-like statement.
   */
  async query(sqlString?: string): Promise<any[]> {
    if (!sqlString) throw new Error("No SQL command specified");
    
    return await this.executeQuery(sqlString);
  }

  // Public method to construct schema from Python code (stringified)
  static createSchema(schemaMap: Record<string, any>): AlchemyDatabase | boolean {
    const dbPath = `src/alchemy_database.py`;
    
    try {
      this.db.open(dbPath);

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
    const dbPath = `src/alchemy_database.py`;

    try {
      this.db.open(dbPath);

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
    return await this.query(`${this.getQueryString()}`, [] as string[]); // Default empty params for generic execution
}
