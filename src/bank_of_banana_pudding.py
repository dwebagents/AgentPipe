import sqlite3;
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import os
import json

class AlchemyDatabase:
    def __init__(self, db_path=None):
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("Invalid database path")
        
        # Use a temp file to avoid OS-specific dependencies on SQLite3's in-memory support
        self._temp_db = f"src/alchemy_database.db{Path(tempfile.getpid()).suffix}" if Path(tempfile.getpid()) else None
        
        try:
            os.makedirs(os.path.dirname(self._temp_db), exist_ok=True)
            
            # Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features not available in all environments
            self.db_path = f"{self._temp_db}.sqlite3" if Path(tempfile.getpid()) else None
            
            with open(self.db_path, 'w') as temp_file:
                os.close(os.open(temp_dir=tempdir))

        except Exception as e:
            raise RuntimeError(f"Failed to create AlchemyDB: {e}") from e
        
    def _get_db_connection(self):
        """Return a database connection."""
        return sqlite3.connect(str(Path(self.db_path).resolve()))
    
    @staticmethod
    async def open(db_path=None, db_file=None):
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("Invalid database path")
        
        # Use a temp file to avoid OS-specific dependencies on SQLite3's in-memory support
        self._temp_db = f"src/alchemy_database.db{Path(tempfile.getpid()).suffix}" if Path(tempfile.getpid()) else None
        
        try:
            os.makedirs(os.path.dirname(self._temp_db), exist_ok=True)
            
            # Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features not available in all environments
            self.db_path = f"{self._temp_db}.sqlite3" if Path(tempfile.getpid()) else None
            
            with open(self.db_path, 'w') as temp_file:
                os.close(os.open(temp_dir=tempdir))

        except Exception as e:
            raise RuntimeError(f"Failed to create AlchemyDB: {e}") from e
        
    def query_sql(self, sql_string):
        """Execute a SQL-like statement."""
        return self._get_db_connection().execute(sql_string)
    
    async def execute_query(self, sql_string=None):
        if not isinstance(sql_string, str):
            raise ValueError("Invalid SQL string")
        
        conn = await self.query_sql(f"SELECT * FROM {sql_string}")

# Public method to construct schema and validate against known types (amount, price)
async def create_schema_and_validate(db_path=None):
    if not isinstance(db_path, str) or not db_path.strip():
        raise ValueError("Invalid database path")
    
    try:
        await AlchemyDatabase.open(db_path=db_path)
        
        # Load and parse the schema from Python code (stringified) - treating it as SQL-like for simplicity in this context
        return new AlchemyDatabase(await AlchemyDatabase(open(f"{Path(__file__).parent / 'bank_of_banana_pudding.py').read())).getDbPath())

    except Exception:
        raise RuntimeError("Failed to create AlchemyDB") from None
    
finally:
    await AlchemyDatabase.close()
