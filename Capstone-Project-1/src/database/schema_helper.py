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

        schema_context = "# Northwind Database Schema\n\n"
        schema_context += "## Available Tables:\n\n"

        for table in tables:
            columns = self.db.get_table_info(table)
            row_count = self.db.get_row_count(table)

            # Table header
            schema_context += f"### {table} ({row_count} rows)\n"

            # Column list (concise format)
            col_list = []
            for col in columns:
                col_name = col['name']
                col_type = col['type']
                markers = []
                if col['pk']:
                    markers.append('PK')
                if col['notnull']:
                    markers.append('NOT NULL')

                if markers:
                    col_list.append(f"{col_name} ({col_type}, {', '.join(markers)})")
                else:
                    col_list.append(f"{col_name} ({col_type})")

            schema_context += "Columns: " + ", ".join(col_list) + "\n\n"

        # Add relationships
        relationships = self.get_table_relationships()
        if relationships:
            schema_context += "## Table Relationships:\n\n"
            for table, rels in relationships.items():
                for rel in rels:
                    schema_context += f"- {rel}\n"

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
        context = """
# Northwind Database - Business Context

The Northwind database represents a fictional company called "Northwind Traders"
that imports and exports specialty foods around the world.

## Key Business Entities:

**Customers**: Companies that purchase products from Northwind
**Orders**: Purchase orders placed by customers
**Order Details**: Line items for each order (products, quantities, prices)
**Products**: Items available for sale
**Categories**: Product categories (e.g., Beverages, Condiments, Seafood)
**Suppliers**: Companies that supply products to Northwind
**Employees**: Northwind staff who process orders
**Shippers**: Shipping companies that deliver orders

## Common Business Questions:
- Sales analysis (top products, customers, employees)
- Inventory management (products, suppliers, stock levels)
- Order tracking and history
- Customer analysis
- Revenue and profitability metrics
- Geographic sales distribution

## Sample Queries You Can Ask:
- "Show me the top 10 customers by total order value"
- "What are the best-selling products?"
- "List all orders from a specific customer"
- "Which employees have the highest sales?"
- "What products are low in stock?"
- "Show sales by category"
- "Which suppliers provide the most products?"
"""
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
