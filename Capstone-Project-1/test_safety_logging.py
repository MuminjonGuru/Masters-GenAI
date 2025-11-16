"""
Test script for safety validator and logging system
"""

from src.agent.safety import SQLSafetyValidator
from src.utils.logger import get_logger


def main():
    print("=" * 70)
    print("TESTING SAFETY VALIDATOR WITH LOGGING")
    print("=" * 70)
    print()

    # Initialize
    validator = SQLSafetyValidator()
    logger = get_logger(level="INFO")

    logger.info("Initializing safety validator and logging test")
    logger.info(f"Blocked keywords: {', '.join(validator.get_blocked_keywords())}")

    print()
    print("-" * 70)
    print("Test 1: Safe Queries")
    print("-" * 70)

    safe_queries = [
        "SELECT * FROM Customers",
        "SELECT COUNT(*) FROM Orders WHERE OrderDate > '2024-01-01'",
        "SELECT p.ProductName, c.CategoryName FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID",
    ]

    for query in safe_queries:
        is_valid, error = validator.validate_query(query)
        logger.log_safety_check(query, is_valid, error)
        if is_valid:
            logger.log_query(query)

    print()
    print("-" * 70)
    print("Test 2: Dangerous Queries (Should be blocked)")
    print("-" * 70)

    dangerous_queries = [
        ("DELETE FROM Customers WHERE CustomerID = 'ALFKI'", "DELETE attempt"),
        ("DROP TABLE Orders", "DROP TABLE attempt"),
        ("UPDATE Products SET UnitPrice = 0", "UPDATE attempt"),
        ("INSERT INTO Customers VALUES ('TEST')", "INSERT attempt"),
        ("TRUNCATE TABLE Orders", "TRUNCATE attempt"),
    ]

    for query, description in dangerous_queries:
        logger.log_agent_action("safety_check", description)
        is_valid, error = validator.validate_query(query)
        logger.log_safety_check(query, is_valid, error)

    print()
    print("-" * 70)
    print("Test 3: SQL Injection Attempts (Should be blocked)")
    print("-" * 70)

    injection_attempts = [
        "SELECT * FROM Users; DROP TABLE Users;",
        "SELECT * FROM Orders WHERE OrderID = '1' OR '1'='1'",
    ]

    for query in injection_attempts:
        logger.log_agent_action("injection_check", "Testing SQL injection detection")
        is_valid, error = validator.validate_query(query)
        logger.log_safety_check(query, is_valid, error)

    print()
    print("-" * 70)
    print("Test 4: Query Sanitization")
    print("-" * 70)

    messy_query = "  SELECT   *   FROM    Customers   WHERE   Country='USA'  ;  "
    logger.info(f"Original query: '{messy_query}'")
    sanitized = validator.sanitize_query(messy_query)
    logger.info(f"Sanitized query: '{sanitized}'")

    print()
    print("-" * 70)
    print("Test 5: Error Logging")
    print("-" * 70)

    try:
        # Simulate an error
        raise ValueError("Simulated database connection error")
    except Exception as e:
        logger.log_error_with_context(e, "Database operation")

    print()
    print("=" * 70)
    logger.info("All safety and logging tests completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
