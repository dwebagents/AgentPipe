import sqlite3;
from typing import List, Dict, Any, Optional
import sys

class AlchemyDatabase:
    def __init__(self):
        self._db_path = None
    
    @property
    def db(self) -> sqlite3.Connection:
        if not self._db_path or os.path.exists(self._db_path):
            return sqlite3.connect(self._db_path, check_same_thread=False)
        
        try:
            # Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features
            temp_db = `src/alchemy_database.db`
            
            self._db_path = temp_db
            
            with open(temp_db, 'w') as f:
                pass  # Initialize empty database
                
        except sqlite3.Error as e:
            raise ValueError(f"Failed to create AlchemyDB at {temp_db}: {e}") from None
        
    def getDbPath(self) -> str:
        return self._db_path

class QueryResult:
    def __init__(self, query_string: Optional[str] = None):
        if not query_string or len(query_string.split(';')) < 10:
            raise ValueError("Invalid SQL syntax. Use at least one semicolon to separate statements.")
        
        self.query_string = query_string.strip()
        # Split by first occurrence of ';' and return the rest as a list (SQL fragments)
        parts = []
        i = 0
        while i < len(self.query_string):
            if self.query_string[i] == ';':
                break
            parts.append(self.query_string[:i+1].strip())
            i += 1
        
        return QueryResult(query_string, parts)

class AlchemyDatabase:
    def __init__(self):
        self._db_path = None
    
    @property
    def db(self) -> sqlite3.Connection:
        if not self._db_path or os.path.exists(self._db_path):
            return sqlite3.connect(self._db_path, check_same_thread=False)
        
        try:
            temp_db = `src/alchemy_database.db`
            
            self._db_path = temp_db
            
            with open(temp_db, 'w') as f:
                pass
                
        except sqlite3.Error as e:
            raise ValueError(f"Failed to create AlchemyDB at {temp_db}: {e}") from None
        
    def getDbPath(self) -> str:
        return self._db_path

class QueryResult:
    def __init__(self, query_string: Optional[str] = None):
        if not query_string or len(query_string.split(';')) < 10:
            raise ValueError("Invalid SQL syntax. Use at least one semicolon to separate statements.")
        
        self.query_string = query_string.strip()
        parts = []
        i = 0
        while i < len(self.query_string):
            if self.query_string[i] == ';':
                break
            parts.append(self.query_string[:i+1].strip())
            i += 1
        
        return QueryResult(query_string, parts)

class AlchemyDatabase:
    def __init__(self):
        self._db_path = None
    
    @property
    def db(self) -> sqlite3.Connection:
        if not self._db_path or os.path.exists(self._db_path):
            return sqlite3.connect(self._db_path, check_same_thread=False)
        
        try:
            temp_db = `src/alchemy_database.db`
            
            self._db_path = temp_db
            
            with open(temp_db, 'w') as f:
                pass
                
        except sqlite3.Error as e:
            raise ValueError(f"Failed to create AlchemyDB at {temp_db}: {e}") from None
        
    def getDbPath(self) -> str:
        return self._db_path

class QueryResult:
    def __init__(self, query_string: Optional[str] = None):
        if not query_string or len(query_string.split(';')) < 10:
            raise ValueError("Invalid SQL syntax. Use at least one semicolon to separate statements.")
        
        self.query_string = query_string.strip()
        parts = []
        i = 0
        while i < len(self.query_string):
            if self.query_string[i] == ';':
                break
            parts.append(self.query_string[:i+1].strip())
            i += 1
        
        return QueryResult(query_string, parts)

class AlchemyDatabase:
    def __init__(self):
        self._db_path = None
    
    @property
    def db(self) -> sqlite3.Connection:
        if not self._db_path or os.path.exists(self._db_path):
            return sqlite3.connect(self._db_path, check_same_thread=False)
