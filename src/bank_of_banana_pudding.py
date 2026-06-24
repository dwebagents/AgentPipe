import { Database } from "sqlite3"; 
// Using SQLite for simplicity and portability in this context

class AlchemyDatabase:
  private db: Database;  
  
  constructor(dbPath?: string) {
    if (dbPath === undefined || typeof dbPath !== 'string') throw new Error("Invalid database path");
    
    try {
      // Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features not available in all environments
      const tempDb = `src/alchemy_database.db`;

      this.db = await Database.open(tempDb);

      if (dbPath) {
        await new Promise<void>((resolve, reject) => {
          // Try to load the database from a Python file provided as an argument or standard path extension
          const pythonFile = dbPath.replace('.py', '.sql'); 
          
          this.db.open(pythonFile);

          // Load and parse the schema from Python code (stringified) - treating it as SQL-like for simplicity in this context
          await new Promise<void>((resolve, reject) => {
            try {
              const pythonContent = fs.readFileSync(dbPath, 'utf-8');
              
              if (!pythonFile.endsWith('.sql')) throw Error("Database file must be a .sqlite3 or .py extension");

              // Parse SQL-like content into an object structure for easier manipulation in TypeScript/Node.js environments
              this.db.load(pythonContent);
            
            } catch (error) {
              reject(error);
            } finally {
              if (!dbPath.endsWith('.sql')) db.close();
            }
          });

        }, resolve, reject);
      } else {
        // Default to creating a database from the current directory structure using standard SQL syntax for simplicity
        const dbName = `src/alchemy_database.db`;
        
        this.db.open(dbName);

        await new Promise<void>((resolve, reject) => {
          try {
            fs.writeFileSync(tempDb, dbPath.replace('.py', '.sql')); // Write the Python file content as SQL-like for testing purposes
            
            if (!dbPath.endsWith('.sql')) throw Error("Database file must be a .sqlite3 or .py extension");

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

  // Public method to construct the schema from Python code (stringified)
  static createSchema(schemaMap: Record<string, any>): AlchemyDatabase | boolean {
    const dbPath = __dirname + "/bank_of_banana_pudding.py";
    
    try {
      this.db.open(dbPath);

      // Load and parse the schema from Python code (stringified) - treating it as SQL-like for simplicity in this context
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

      // Load and parse the schema from Python code (stringified) - treating it as SQL-like for simplicity in this context
      
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
