"""
Test script for the OpenAI agent and function calling
NOTE: Requires OPENAI_API_KEY environment variable to be set
"""

import os
from dotenv import load_dotenv
from src.agent.llm_agent import NorthwindAgent


def main():
    print("=" * 70)
    print("NORTHWIND AGENT - FUNCTION CALLING TEST")
    print("=" * 70)
    print()

    # Load environment variables
    load_dotenv()

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY not found in environment variables")
        print()
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        print()
        print("Or set it as an environment variable before running this test.")
        return

    try:
        # Initialize agent
        print("[INIT] Initializing Northwind Agent...")
        agent = NorthwindAgent()
        print("[OK] Agent initialized successfully")
        print()

        # Test 1: Database statistics
        print("-" * 70)
        print("[TEST 1] Database Statistics")
        print("-" * 70)
        stats = agent.get_database_stats()
        print(f"Total tables: {stats['total_tables']}")
        print(f"Total rows: {stats['total_rows']:,}")
        print(f"Top 5 tables:")
        sorted_tables = sorted(stats['tables'].items(),
                             key=lambda x: x[1]['row_count'],
                             reverse=True)[:5]
        for table, info in sorted_tables:
            print(f"  - {table}: {info['row_count']:,} rows")
        print()

        # Test 2: Simple query
        print("-" * 70)
        print("[TEST 2] Simple Query - Customer Count")
        print("-" * 70)
        print("Query: 'How many customers do we have?'")
        print()
        response = agent.chat("How many customers do we have?")

        if response['success']:
            print(f"Response: {response['response']}")
            print(f"\nTool calls made: {len(response['tool_calls'])}")
            for i, tool_call in enumerate(response['tool_calls'], 1):
                print(f"\nTool {i}: {tool_call['function']}")
                if tool_call['function'] == 'execute_sql_query':
                    print(f"  Query: {tool_call['arguments'].get('query', 'N/A')}")
                    print(f"  Success: {tool_call['result'].get('success', False)}")
                    print(f"  Rows returned: {tool_call['result'].get('row_count', 0)}")
        else:
            print(f"[ERROR] {response.get('error')}")
        print()

        # Test 3: More complex query
        print("-" * 70)
        print("[TEST 3] Complex Query - Top Products")
        print("-" * 70)
        print("Query: 'What are the top 5 products by total order quantity?'")
        print()

        agent.reset_conversation()  # Start fresh
        response = agent.chat("What are the top 5 products by total order quantity?")

        if response['success']:
            print(f"Response: {response['response']}")
            print(f"\nTool calls made: {len(response['tool_calls'])}")
        else:
            print(f"[ERROR] {response.get('error')}")
        print()

        # Test 4: Conversation history
        print("-" * 70)
        print("[TEST 4] Conversation History")
        print("-" * 70)
        history = agent.get_conversation_history()
        print(f"Total messages in history: {len(history)}")
        print(f"Message types: {[msg['role'] for msg in history]}")
        print()

        print("=" * 70)
        print("[SUCCESS] All agent tests completed!")
        print("=" * 70)

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
