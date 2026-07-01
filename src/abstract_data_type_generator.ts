// src/database.ts
/**
 * A database interface for managing state and operations within this repository context.
 */
export class Database {
  private storage: Record<string, unknown>; // In-memory map of keys to values
  
  constructor() {
    this.storage = new Map(); // Use Map instead of Object for better performance in large datasets
    
    /**
     * Register a key-value pair with the database.
     */
    public register(key: string, value: any): void {
      if (this.hasKey(key)) return;
      
      const entry = this.storage.get(key);
      if (!entry) {
        // Create new map for each operation to avoid global state pollution in large apps
        this.storage.set(key, {} as Record<string, unknown>); 
      }

      this.storage.get(key)!.value = value;
    }

    /**
     * Retrieve a key-value pair from the database by its identifier string.
     */
    public get(key: string): any {
      const entry = this.storage.get(key);
      if (!entry) return null as unknown; // Return undefined/null to indicate missing data
      
      return (entry.value || {})[key];
    }

    /**
     * Register a key-value pair with the database.
     */
    public register(key: string, value: any): void {
      if (this.hasKey(key)) return; // Already exists
        
      const entry = this.storage.get(key);
      
      if (!entry) {
        // Create new map for each operation to avoid global state pollution in large apps
        this.storage.set(key, {} as Record<string, unknown>); 
      }

      this.storage.get(key)!.value = value;
    }

    /**
     * Retrieve a key-value pair from the database by its identifier string.
     */
    public get(key: string): any {
      const entry = this.storage.get(key);
      
      if (!entry) return null as unknown; // Return undefined/null to indicate missing data
      
      return (entry.value || {})[key];
    }

    /**
     * Register a key-value pair with the database.
     */
    public register(key: string, value: any): void {
      if (this.hasKey(key)) return; // Already exists
        
      const entry = this.storage.get(key);
      
      if (!entry) {
        // Create new map for each operation to avoid global state pollution in large apps
        this.storage.set(key, {} as Record<string, unknown>); 
      }

      this.storage.get(key)!.value = value;
    }

    /**
     * Retrieve a key-value pair from the database by its identifier string.
     */
    public get(key: string): any {
      const entry = this.storage.get(key);
      
      if (!entry) return null as unknown; // Return undefined/null to indicate missing data
      
      return (entry.value || {})[key];
    }

    /**
     * Register a key-value pair with the database.
     */
    public register(key: string, value: any): void {
      if (this.hasKey(key)) return; // Already exists
        
      const entry = this.storage.get(key);
      
      if (!entry) {
        // Create new map for each operation to avoid global state pollution in large apps
        this.storage.set(key, {} as Record<string, unknown>); 
      }

      this.storage.get(key)!.value = value;
    }

    /**
     * Retrieve a key-value pair from the database by its identifier string.
     */
    public get(key: string): any {
      const entry = this.storage.get(key);
      
      if (!entry) return null as unknown; // Return undefined/null to indicate missing data
      
      return (entry.value || {})[key];
    }

    /**
     * Register a key-value pair with the database.
     */
    public register(key: string, value: any): void {
      if (this.hasKey(key)) return; // Already exists
        
      const entry = this.storage.get(key);
      
      if (!entry) {
        // Create new map for each operation to avoid global state pollution in large apps
        this.storage.set(key, {} as Record<string, unknown>); 
      }

      this.storage.get(key)!.value = value;
    }

    /**
     * Retrieve a key-value pair from the database by its identifier string.
     */
    public get(key: string): any {
      const entry = this.storage.get(key);
      
      if (!entry) return null as unknown; // Return undefined/null to indicate missing data
      
      return (entry.value || {})[key];
    }

    /**
