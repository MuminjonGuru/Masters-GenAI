"""
SQL Safety Validator
Prevents dangerous SQL operations and ensures queries are read-only
"""

import re
from typing import Tuple, List


class SQLSafetyValidator:
    """
    Validates SQL queries to prevent dangerous operations.
    Implements safeguards against destructive commands.
    """

    # Dangerous SQL keywords that modify data or schema
    BLOCKED_KEYWORDS = [
        'DELETE',
        'DROP',
        'TRUNCATE',
        'ALTER',
        'INSERT',
        'UPDATE',
        'CREATE',
        'REPLACE',
        'GRANT',
        'REVOKE',
        'COMMIT',
        'ROLLBACK',
        'SAVEPOINT',
        'PRAGMA',  # Block PRAGMA except through controlled methods
    ]

    # Allowed PRAGMA commands (whitelist)
    ALLOWED_PRAGMAS = [
        'table_info',
        'foreign_key_list',
        'index_list',
        'table_list',
    ]

    def __init__(self):
        """Initialize the safety validator."""
        self.blocked_pattern = self._compile_blocked_pattern()

    def _compile_blocked_pattern(self) -> re.Pattern:
        """
        Compile regex pattern for blocked keywords.

        Returns:
            Compiled regex pattern
        """
        # Create pattern that matches blocked keywords as whole words
        # Use word boundaries to avoid false positives
        keywords = '|'.join(self.BLOCKED_KEYWORDS)
        pattern = rf'\b({keywords})\b'
        return re.compile(pattern, re.IGNORECASE)

    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        Validate a SQL query for safety.

        Args:
            query: SQL query string to validate

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if query is safe, False otherwise
            - error_message: Description of the issue if invalid, empty string if valid
        """
        if not query or not query.strip():
            return False, "Query cannot be empty"

        # Normalize query for checking
        normalized_query = query.strip()

        # Check for blocked keywords
        match = self.blocked_pattern.search(normalized_query)
        if match:
            blocked_keyword = match.group(1).upper()

            # Special case: PRAGMA - check if it's allowed
            if blocked_keyword == 'PRAGMA':
                if self._is_allowed_pragma(normalized_query):
                    return True, ""
                else:
                    return False, f"Blocked: PRAGMA command not allowed (only read-only PRAGMAs are permitted)"

            return False, f"Blocked: {blocked_keyword} operations are not allowed (read-only queries only)"

        # Check for SQL injection patterns
        if self._has_sql_injection_pattern(normalized_query):
            return False, "Potential SQL injection detected"

        # Check for multiple statements (prevents stacking attacks)
        if self._has_multiple_statements(normalized_query):
            return False, "Multiple SQL statements are not allowed"

        return True, ""

    def _is_allowed_pragma(self, query: str) -> bool:
        """
        Check if a PRAGMA command is in the allowed list.

        Args:
            query: SQL query string

        Returns:
            True if PRAGMA is allowed, False otherwise
        """
        for allowed_pragma in self.ALLOWED_PRAGMAS:
            if allowed_pragma.lower() in query.lower():
                return True
        return False

    def _has_sql_injection_pattern(self, query: str) -> bool:
        """
        Check for common SQL injection patterns.

        Args:
            query: SQL query string

        Returns:
            True if potential injection found, False otherwise
        """
        # Common SQL injection patterns
        injection_patterns = [
            r"['\"];\s*DROP",
            r"['\"];\s*DELETE",
            r"--\s*$",  # SQL comments at end (suspicious)
            r"/\*.*\*/",  # Block comments (often used in injection)
            r"UNION\s+SELECT.*FROM\s+information_schema",
            r"UNION\s+SELECT.*FROM\s+sqlite_master.*WHERE.*type\s*=\s*['\"]table['\"]",
        ]

        for pattern in injection_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True

        return False

    def _has_multiple_statements(self, query: str) -> bool:
        """
        Check if query contains multiple SQL statements.

        Args:
            query: SQL query string

        Returns:
            True if multiple statements found, False otherwise
        """
        # Simple check: look for semicolons not in quotes
        # Remove quoted strings first
        without_quotes = re.sub(r"'[^']*'", "", query)
        without_quotes = re.sub(r'"[^"]*"', "", without_quotes)

        # Count semicolons (allow one at the end)
        semicolons = without_quotes.count(';')

        # Allow 0 or 1 semicolon (1 if at the end)
        if semicolons > 1:
            return True

        # If there's exactly 1 semicolon, make sure it's at the end
        if semicolons == 1 and not without_quotes.rstrip().endswith(';'):
            return True

        return False

    def get_blocked_keywords(self) -> List[str]:
        """
        Get list of blocked SQL keywords.

        Returns:
            List of blocked keywords
        """
        return self.BLOCKED_KEYWORDS.copy()

    def sanitize_query(self, query: str) -> str:
        """
        Sanitize a query by removing extra whitespace and normalizing.

        Args:
            query: SQL query string

        Returns:
            Sanitized query string
        """
        # Remove extra whitespace
        sanitized = ' '.join(query.split())

        # Remove trailing semicolon if present
        sanitized = sanitized.rstrip(';')

        return sanitized


def validate_sql_safe(query: str) -> Tuple[bool, str]:
    """
    Convenience function to validate a SQL query.

    Args:
        query: SQL query string

    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = SQLSafetyValidator()
    return validator.validate_query(query)


if __name__ == "__main__":
    # Test the safety validator
    validator = SQLSafetyValidator()

    print("=" * 70)
    print("SQL SAFETY VALIDATOR TESTS")
    print("=" * 70)

    # Test cases
    test_queries = [
        ("SELECT * FROM Customers", True, "Valid SELECT query"),
        ("SELECT CustomerID, CompanyName FROM Customers WHERE Country = 'USA'", True, "Valid SELECT with WHERE"),
        ("DELETE FROM Customers WHERE CustomerID = 'ALFKI'", False, "DELETE operation"),
        ("DROP TABLE Customers", False, "DROP operation"),
        ("UPDATE Customers SET CompanyName = 'New Name'", False, "UPDATE operation"),
        ("INSERT INTO Customers VALUES ('TEST', 'Test Company')", False, "INSERT operation"),
        ("SELECT * FROM Orders; DROP TABLE Orders;", False, "SQL injection attempt"),
        ("SELECT * FROM Customers WHERE CustomerID = 'ALFKI' -- comment", False, "Suspicious comment"),
        ("PRAGMA table_info(Customers)", True, "Allowed PRAGMA"),
        ("PRAGMA foreign_keys = ON", False, "Blocked PRAGMA"),
        ("", False, "Empty query"),
        ("SELECT * FROM Customers LIMIT 10", True, "Valid with LIMIT"),
    ]

    print("\nRunning test cases...\n")

    passed = 0
    failed = 0

    for query, expected_valid, description in test_queries:
        is_valid, error_msg = validator.validate_query(query)

        status = "[PASS]" if is_valid == expected_valid else "[FAIL]"
        if is_valid == expected_valid:
            passed += 1
        else:
            failed += 1

        print(f"{status} {description}")
        print(f"  Query: {query[:60]}{'...' if len(query) > 60 else ''}")
        print(f"  Expected: {'VALID' if expected_valid else 'INVALID'}")
        print(f"  Result: {'VALID' if is_valid else 'INVALID'}")
        if error_msg:
            print(f"  Error: {error_msg}")
        print()

    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("[SUCCESS] All safety validator tests passed!")
    else:
        print(f"[WARNING] {failed} test(s) failed!")
