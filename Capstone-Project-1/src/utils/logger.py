"""
Logging Configuration
Sets up console logging for the agent with color-coded output
"""

import logging
import sys
from typing import Optional
try:
    import colorlog
    HAS_COLORLOG = True
except ImportError:
    HAS_COLORLOG = False


class AgentLogger:
    """
    Custom logger for the Northwind Data Insights Agent.
    Provides structured, color-coded console logging.
    """

    def __init__(self, name: str = "NorthwindAgent", level: str = "INFO"):
        """
        Initialize the agent logger.

        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        # Create formatter
        if HAS_COLORLOG:
            formatter = colorlog.ColoredFormatter(
                '%(log_color)s[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
        else:
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)

    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)

    def log_query(self, query: str, row_count: Optional[int] = None):
        """
        Log a SQL query execution.

        Args:
            query: SQL query string
            row_count: Number of rows returned (optional)
        """
        if row_count is not None:
            self.info(f"Executed query (returned {row_count} rows): {query[:100]}...")
        else:
            self.info(f"Executing query: {query[:100]}...")

    def log_function_call(self, function_name: str, arguments: dict):
        """
        Log a function call.

        Args:
            function_name: Name of the function being called
            arguments: Dictionary of function arguments
        """
        args_str = ", ".join([f"{k}={v}" for k, v in arguments.items()])
        self.info(f"Function call: {function_name}({args_str[:100]}...)")

    def log_agent_action(self, action: str, details: str = ""):
        """
        Log an agent action.

        Args:
            action: Type of action (e.g., "query_generation", "data_export")
            details: Additional details about the action
        """
        if details:
            self.info(f"Agent action: {action} - {details}")
        else:
            self.info(f"Agent action: {action}")

    def log_safety_check(self, query: str, is_safe: bool, reason: str = ""):
        """
        Log a safety check result.

        Args:
            query: SQL query that was checked
            is_safe: Whether the query passed safety checks
            reason: Reason if query was blocked
        """
        if is_safe:
            self.info(f"Safety check PASSED: {query[:80]}...")
        else:
            self.warning(f"Safety check BLOCKED: {reason} - Query: {query[:80]}...")

    def log_error_with_context(self, error: Exception, context: str = ""):
        """
        Log an error with additional context.

        Args:
            error: Exception object
            context: Additional context about where the error occurred
        """
        if context:
            self.error(f"{context}: {type(error).__name__}: {str(error)}")
        else:
            self.error(f"{type(error).__name__}: {str(error)}")


# Global logger instance
_global_logger: Optional[AgentLogger] = None


def get_logger(name: str = "NorthwindAgent", level: str = "INFO") -> AgentLogger:
    """
    Get or create a global logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        AgentLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = AgentLogger(name, level)
    return _global_logger


def setup_logging(level: str = "INFO") -> AgentLogger:
    """
    Setup logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        AgentLogger instance
    """
    return get_logger(level=level)


if __name__ == "__main__":
    # Test the logger
    print("=" * 70)
    print("LOGGER TEST")
    print("=" * 70)
    print()

    logger = get_logger(level="DEBUG")

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    print()
    logger.log_query("SELECT * FROM Customers WHERE Country = 'USA'", row_count=13)

    print()
    logger.log_function_call("execute_sql_query", {
        "query": "SELECT * FROM Orders",
        "explanation": "Get all orders"
    })

    print()
    logger.log_agent_action("data_export", "Exporting results to CSV")

    print()
    logger.log_safety_check("SELECT * FROM Customers", is_safe=True)

    print()
    logger.log_safety_check(
        "DELETE FROM Customers",
        is_safe=False,
        reason="DELETE operations are not allowed"
    )

    print()
    try:
        raise ValueError("Test error message")
    except Exception as e:
        logger.log_error_with_context(e, "Testing error logging")

    print()
    print("=" * 70)
    print("[SUCCESS] Logger test complete!")
    print("=" * 70)
