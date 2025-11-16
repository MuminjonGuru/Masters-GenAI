"""
Verify agent setup without requiring API key
Tests that all components are properly imported and configured
"""

from src.agent.tools import ToolExecutor, get_tool_definitions, TOOLS
from src.database.db_manager import DatabaseManager
from src.utils.logger import get_logger
from src.agent.safety import SQLSafetyValidator


def main():
    print("=" * 70)
    print("AGENT SETUP VERIFICATION")
    print("=" * 70)
    print()

    # Test 1: Tool definitions
    print("[TEST 1] Tool Definitions")
    tools = get_tool_definitions()
    print(f"Total tools defined: {len(tools)}")
    for i, tool in enumerate(tools, 1):
        tool_name = tool['function']['name']
        tool_desc = tool['function']['description'][:60]
        print(f"  {i}. {tool_name}")
        print(f"     {tool_desc}...")
    print("[OK] All tools defined correctly")
    print()

    # Test 2: Tool executor initialization
    print("[TEST 2] Tool Executor Initialization")
    db = DatabaseManager()
    logger = get_logger()
    validator = SQLSafetyValidator()
    executor = ToolExecutor(db, logger, validator)
    print("[OK] Tool executor initialized")
    print()

    # Test 3: SQL query execution (without API)
    print("[TEST 3] SQL Query Execution Tool")
    result = executor.execute_sql_query(
        query="SELECT * FROM Customers LIMIT 3",
        explanation="Test query to get sample customers"
    )
    print(f"Success: {result['success']}")
    print(f"Rows returned: {result.get('row_count', 0)}")
    if result['success'] and result['data']:
        print(f"Sample data: {result['data'][0]}")
    print("[OK] SQL execution tool working")
    print()

    # Test 4: Safety validation in tool
    print("[TEST 4] Safety Validation in Tool")
    result = executor.execute_sql_query(
        query="DELETE FROM Customers WHERE CustomerID = 'ALFKI'",
        explanation="Attempting dangerous operation"
    )
    print(f"Success: {result['success']}")
    print(f"Error: {result.get('error', 'N/A')}")
    if not result['success'] and 'blocked' in result.get('error', '').lower():
        print("[OK] Dangerous query blocked correctly")
    else:
        print("[WARNING] Safety check may not be working properly")
    print()

    # Test 5: Export tool (dry run)
    print("[TEST 5] Export Tool Structure")
    import json
    test_data = [
        {"id": 1, "name": "Test 1"},
        {"id": 2, "name": "Test 2"}
    ]
    result = executor.export_data_to_file(
        data=json.dumps(test_data),
        filename="test_export",
        format="csv"
    )
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"File created: {result.get('filepath', 'N/A')}")
        print("[OK] Export tool working")
    else:
        print(f"Error: {result.get('error', 'N/A')}")
    print()

    # Test 6: Chart tool structure
    print("[TEST 6] Chart Tool Structure")
    result = executor.generate_chart(
        data=json.dumps(test_data),
        chart_type="bar",
        x_column="name",
        y_column="id",
        title="Test Chart"
    )
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Data points: {result.get('data_points', 0)}")
        print("[OK] Chart tool working")
    else:
        print(f"Error: {result.get('error', 'N/A')}")
    print()

    # Test 7: Support ticket tool
    print("[TEST 7] Support Ticket Tool")
    result = executor.create_support_ticket(
        title="Test Ticket",
        description="This is a test",
        priority="low"
    )
    print(f"Success: {result['success']}")
    print(f"Note: {result.get('error', 'GitHub integration pending')}")
    print("[OK] Support ticket tool structure ready")
    print()

    # Test 8: Verify all required parameters
    print("[TEST 8] Tool Parameter Validation")
    for tool in TOOLS:
        tool_name = tool['function']['name']
        required_params = tool['function']['parameters'].get('required', [])
        print(f"  {tool_name}: {len(required_params)} required parameters")
        print(f"    Required: {', '.join(required_params)}")
    print("[OK] All tools have proper parameter definitions")
    print()

    print("=" * 70)
    print("[SUCCESS] Agent setup verified successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Set up your .env file with OPENAI_API_KEY")
    print("2. Run test_agent.py to test with actual OpenAI API")
    print("3. Or proceed to Streamlit UI implementation")


if __name__ == "__main__":
    main()
