"""
Database Manager for Northwind SQLite Database
Handles all database connections and query execution
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import os
from pathlib import Path


class DatabaseManager:
    """
    Manages database connections and query execution for Northwind database.
    Implements read-only access for safety.
    """

    def __init__(self, db_path: str = "northwind.db", max_results: int = 1000):
        """
        Initialize database manager.

        Args:
            db_path: Path to the SQLite database file
            max_results: Maximum number of rows to return from queries
        """
        self.db_path = db_path
        self.max_results = max_results
        self._verify_database()

    def _verify_database(self):
        """Verify that the database file exists."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")

    def get_connection(self, read_only: bool = True) -> sqlite3.Connection:
        """
        Create a database connection.

        Args:
            read_only: If True, opens database in read-only mode

        Returns:
            SQLite connection object
        """
        if read_only:
            # Open in read-only mode using URI
            uri = f"file:{self.db_path}?mode=ro"
            conn = sqlite3.connect(uri, uri=True)
        else:
            conn = sqlite3.connect(self.db_path)

        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def execute_query(self, query: str, params: Optional[tuple] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Execute a SQL query and return results.

        Args:
            query: SQL query string
            params: Optional query parameters for parameterized queries

        Returns:
            Tuple of (list of rows as dictionaries, column names)
        """
        conn = None
        try:
            conn = self.get_connection(read_only=True)
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Get column names
            columns = [description[0] for description in cursor.description] if cursor.description else []

            # Fetch results with limit
            rows = cursor.fetchmany(self.max_results)

            # Convert to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))

            return results, columns

        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def execute_query_df(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a pandas DataFrame.

        Args:
            query: SQL query string

        Returns:
            Pandas DataFrame with query results
        """
        conn = None
        try:
            conn = self.get_connection(read_only=True)
            df = pd.read_sql_query(query, conn)

            # Limit results
            if len(df) > self.max_results:
                df = df.head(self.max_results)

            return df

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def get_all_tables(self) -> List[str]:
        """
        Get list of all tables in the database.

        Returns:
            List of table names
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        results, _ = self.execute_query(query)
        return [row['name'] for row in results]

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about table columns.

        Args:
            table_name: Name of the table

        Returns:
            List of dictionaries containing column information
        """
        query = f'PRAGMA table_info("{table_name}");'
        results, _ = self.execute_query(query)
        return results

    def get_row_count(self, table_name: str) -> int:
        """
        Get the number of rows in a table.

        Args:
            table_name: Name of the table

        Returns:
            Number of rows
        """
        query = f'SELECT COUNT(*) as count FROM "{table_name}";'
        results, _ = self.execute_query(query)
        return results[0]['count'] if results else 0

    def get_sample_rows(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """
        Get sample rows from a table.

        Args:
            table_name: Name of the table
            limit: Number of sample rows to return

        Returns:
            DataFrame with sample rows
        """
        query = f'SELECT * FROM "{table_name}" LIMIT {limit};'
        return self.execute_query_df(query)

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get overall database statistics.

        Returns:
            Dictionary containing database statistics
        """
        tables = self.get_all_tables()
        stats = {
            'total_tables': len(tables),
            'tables': {},
            'total_rows': 0
        }

        for table in tables:
            row_count = self.get_row_count(table)
            stats['tables'][table] = {
                'row_count': row_count
            }
            stats['total_rows'] += row_count

        return stats

    def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            conn = self.get_connection(read_only=True)
            conn.close()
            return True
        except Exception:
            return False


if __name__ == "__main__":
    # Test the database manager
    db = DatabaseManager()

    print("Testing Database Connection...")
    if db.test_connection():
        print("[OK] Connection successful!")
    else:
        print("[ERROR] Connection failed!")
        exit(1)

    print("\nDatabase Statistics:")
    stats = db.get_database_stats()
    print(f"Total Tables: {stats['total_tables']}")
    print(f"Total Rows: {stats['total_rows']}")

    print("\nTables:")
    for table, info in stats['tables'].items():
        print(f"  - {table}: {info['row_count']} rows")

    print("\nSample query test:")
    results, columns = db.execute_query("SELECT * FROM Customers LIMIT 3")
    print(f"Columns: {columns}")
    print(f"First result: {results[0] if results else 'No results'}")
