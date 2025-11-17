"""
Schema Helper for Northwind Database
Provides schema information and context for LLM
"""

from typing import Dict, List, Any

try:
    from .db_manager import DatabaseManager
except ImportError:
    from db_manager import DatabaseManager


class SchemaHelper:
    """
    Helps extract and format database schema information for LLM context.
    Provides the agent with necessary database structure without sending full data.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize schema helper.

        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager

    def get_schema_summary(self) -> str:
        """
        Get a concise schema summary for LLM context.

        Returns:
            Formatted string describing the database schema
        """
        tables = self.db.get_all_tables()
        summary = "NORTHWIND DATABASE SCHEMA\n"
        summary += "=" * 50 + "\n\n"

        for table in tables:
            columns = self.db.get_table_info(table)
            row_count = self.db.get_row_count(table)

            summary += f"Table: {table} ({row_count} rows)\n"
            summary += "Columns:\n"

            for col in columns:
                col_name = col['name']
                col_type = col['type']
                pk = " [PRIMARY KEY]" if col['pk'] else ""
                not_null = " [NOT NULL]" if col['notnull'] else ""
                summary += f"  - {col_name}: {col_type}{pk}{not_null}\n"

            summary += "\n"

        return summary

    def get_table_relationships(self) -> Dict[str, List[str]]:
        """
        Get foreign key relationships between tables.

        Returns:
            Dictionary mapping tables to their foreign key relationships
        """
        tables = self.db.get_all_tables()
        relationships = {}

        for table in tables:
            conn = self.db.get_connection(read_only=True)
            cursor = conn.cursor()

            cursor.execute(f'PRAGMA foreign_key_list("{table}");')
            foreign_keys = cursor.fetchall()

            if foreign_keys:
                relationships[table] = []
                for fk in foreign_keys:
                    # fk structure: (id, seq, table, from, to, on_update, on_delete, match)
                    ref_table = fk[2]
                    from_col = fk[3]
                    to_col = fk[4]
                    relationships[table].append(
                        f"{table}.{from_col} -> {ref_table}.{to_col}"
                    )

            conn.close()

        return relationships

    def get_schema_for_llm(self) -> str:
        """
        Get optimized schema context for LLM (concise version).

        Returns:
            Formatted schema string optimized for LLM context
        """
        tables = self.db.get_all_tables()

        schema_context = "## Database Tables:\n"

        # Very concise table list with just key columns
        for table in tables:
            columns = self.db.get_table_info(table)

            # Only show primary key and a few important columns
            key_cols = []
            for col in columns:
                if col['pk'] or len(key_cols) < 3:  # PK + max 3 other columns
                    col_name = col['name']
                    if col['pk']:
                        key_cols.append(f"{col_name}*")
                    else:
                        key_cols.append(col_name)

            schema_context += f"- {table}: {', '.join(key_cols)}\n"

        # Add only essential relationships
        schema_context += "\n## Key Relationships:\n"
        schema_context += "- Orders -> Customers, Employees, Shippers\n"
        schema_context += "- Order Details -> Orders, Products\n"
        schema_context += "- Products -> Categories, Suppliers\n"

        return schema_context

    def get_table_description(self, table_name: str) -> str:
        """
        Get detailed description of a specific table.

        Args:
            table_name: Name of the table

        Returns:
            Formatted string with table details
        """
        columns = self.db.get_table_info(table_name)
        row_count = self.db.get_row_count(table_name)

        description = f"Table: {table_name}\n"
        description += f"Rows: {row_count}\n\n"
        description += "Columns:\n"

        for col in columns:
            description += f"  - {col['name']} ({col['type']})"
            if col['pk']:
                description += " [PRIMARY KEY]"
            if col['notnull']:
                description += " [NOT NULL]"
            if col['dflt_value']:
                description += f" [DEFAULT: {col['dflt_value']}]"
            description += "\n"

        # Get sample data
        sample = self.db.get_sample_rows(table_name, limit=3)
        if not sample.empty:
            description += "\nSample Data:\n"
            description += sample.to_string(index=False)

        return description

    def get_business_context(self) -> str:
        """
        Get business context about the Northwind database.

        Returns:
            String describing the business context
        """
        context = """## Business Context:
Northwind Traders is a specialty food import/export company. The database tracks customers, orders, products, employees, and suppliers.

## Common Queries:
Sales analysis, inventory management, order tracking, customer/employee performance."""
        return context


if __name__ == "__main__":
    # Test the schema helper
    db = DatabaseManager()
    schema = SchemaHelper(db)

    print("Schema Summary:")
    print("=" * 60)
    print(schema.get_schema_summary())

    print("\n\nOptimized Schema for LLM:")
    print("=" * 60)
    print(schema.get_schema_for_llm())

    print("\n\nBusiness Context:")
    print("=" * 60)
    print(schema.get_business_context())
