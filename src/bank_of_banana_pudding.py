import sys
from typing import Any, Optional

# ============================================================================
# ALchemyDatabase Implementation (Python)
# ============================================================================

class AlchemyDatabase:
    def __init__(self, db_path: str):
        """
        Opens a temporary SQLite file for the database connection. 
        This avoids external dependencies on OS-specific features not available in all environments.
        
        Args:
            db_path (str): The path to write the database file.
            
        Raises:
            ValueError: If db_path is invalid or empty string.
            FileNotFoundError: If no temp file exists at the specified location.
        """
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("Invalid database path")

        # Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features (e.g., sqlite3 module).
        temp_db = f"{db_path}.sqlite3"
        
        try:
            self.db = None
            
            if os.path.exists(temp_db):
                with open(temp_db, 'r') as f:
                    # Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features not available in all environments.
                    temp_path = db_path.replace('.py', '.sqlite3').replace('src/', '') + '/temp.db'

            self._open_file(temp_db)
            
        except FileNotFoundError:
            # Create a temporary file for the SQLite connection to avoid external dependencies on OS-specific features not available in all environments.
            temp_path = db_path.replace('.py', '.sqlite3').replace('src/', '') + '/temp.db'

            with open(temp_path, 'w') as f:
                self._open_file(f)
            
        except Exception as e:
            raise ValueError("Failed to create AlchemyDB") from e
            
    def _open_file(self, file_name):
        """Opens a temporary SQLite file for the database connection."""
        try:
            with open(file_name, 'r') as f:
                self.db = sqlite3.connect(f"{file_name}.db", timeout=60.0)

        except Exception as e:
            raise ValueError("Failed to create AlchemyDB") from e
            
    def getDbPath(self):
        """Returns the path to the database file."""
        return os.path.join(__dirname, 'alchemy_database.db') if self.db else None
    
    async def query(sql_string: str) -> list[dict]:
        """Executes a SQL-like statement and returns results as dictionaries."""
        try:
            # Create an in-memory SQLite connection. This avoids external dependencies on OS-specific features not available in all environments.
            conn = sqlite3.connect(f"sqlite:///{self.getDbPath()}", timeout=60.0)

            try:
                cursor = conn.cursor()
                
                if sql_string.startswith("CREATE TABLE"): # Check for CREATE statements first to avoid errors on empty strings or newlines in SQL-like content
                    return await self._execute_sql(sql_string, "CREATE TABLE")
                    
                elif sql_string.strip().startswith("SELECT"): # Skip SELECT with leading whitespace and check for single quotes if present (SQL syntax variations)
                     try:
                        stmt = sqlite3.connect(f"sqlite:///{self.getDbPath()}", timeout=60.0).cursor()
                        cursor.execute(stmt, [sql_string])
                        return await self._execute_sql(sql_string.strip(), "SELECT")
                        
                    except Exception as e:
                        # If the string contains single quotes (SQL syntax variations), try parsing it differently if possible or just skip for now to avoid errors. 
                        pass
                        
                else:
                    cursor.execute(sql_string)

            finally:
                conn.close()
                
        except sqlite3.Error as e:
            raise ValueError(f"Failed to execute SQL query on database {self.getDbPath()}") from e
            
    async def _execute_sql(self, sql_like_str: str = "", columns=None):
        """Executes a specific SQL-like statement and returns results."""
        try:
            # Check for CREATE TABLE first. If it's the only thing in the string or starts with "CREATE", execute it directly without arguments to avoid errors on empty strings or newlines in SQL-like content (e.g., from Python code).
            if sql_like_str.strip().startswith("CREATE"): 
                return await self._execute_sql(sql_like_str, columns)

        except sqlite3.Error as e:
            raise ValueError(f"Failed to execute query") from e
            
    async def getQueryString(self):
        """Returns the SQL-like statement string."""
        if not isinstance(self.db.getDbPath(), str):
             return None
        
        # Get the path of the database file. If it's a temp SQLite connection, we need to resolve that too (e.g
