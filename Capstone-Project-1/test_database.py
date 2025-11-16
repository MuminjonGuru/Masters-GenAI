"""
Test script for database manager and schema helper
"""

from src.database.db_manager import DatabaseManager
from src.database.schema_helper import SchemaHelper


def main():
    print("=" * 70)
    print("TESTING DATABASE MANAGER AND SCHEMA HELPER")
    print("=" * 70)

    # Initialize
    db = DatabaseManager()
    schema = SchemaHelper(db)

    # Test 1: Connection
    print("\n[TEST 1] Database Connection")
    if db.test_connection():
        print("[OK] Connection successful!")
    else:
        print("[ERROR] Connection failed!")
        return

    # Test 2: Database stats
    print("\n[TEST 2] Database Statistics")
    stats = db.get_database_stats()
    print(f"Total Tables: {stats['total_tables']}")
    print(f"Total Rows: {stats['total_rows']:,}")
    print("\nTop 5 tables by row count:")
    sorted_tables = sorted(stats['tables'].items(), key=lambda x: x[1]['row_count'], reverse=True)[:5]
    for table, info in sorted_tables:
        print(f"  - {table}: {info['row_count']:,} rows")

    # Test 3: Sample query
    print("\n[TEST 3] Sample Query")
    results, columns = db.execute_query("SELECT * FROM Customers LIMIT 3")
    print(f"Query returned {len(results)} rows with {len(columns)} columns")
    print(f"Columns: {', '.join(columns[:5])}...")

    # Test 4: Schema for LLM
    print("\n[TEST 4] Schema Context for LLM")
    llm_schema = schema.get_schema_for_llm()
    print(f"Schema context length: {len(llm_schema)} characters")
    print("First 500 characters:")
    print(llm_schema[:500] + "...")

    # Test 5: Table relationships
    print("\n[TEST 5] Table Relationships")
    relationships = schema.get_table_relationships()
    print(f"Found {len(relationships)} tables with foreign keys")
    for table, rels in list(relationships.items())[:3]:
        print(f"\n{table}:")
        for rel in rels:
            print(f"  - {rel}")

    print("\n" + "=" * 70)
    print("[SUCCESS] All tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
