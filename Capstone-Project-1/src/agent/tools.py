"""
Function Calling Tools for the Northwind Agent
Defines all tools available to the agent
"""

import json
from typing import Dict, List, Any, Optional
import pandas as pd
import os

from ..github_integration.issue_creator import GitHubIssueCreator

# Tool definitions for OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_sql_query",
            "description": "Execute a read-only SQL query on the Northwind database. Use this to retrieve data from the database based on user questions. The query must be a SELECT statement only - no INSERT, UPDATE, DELETE, or DROP operations are allowed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL SELECT query to execute. Must be read-only. Example: 'SELECT * FROM Customers WHERE Country = \"USA\" LIMIT 10'"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "A brief explanation of what this query does and why it answers the user's question"
                    }
                },
                "required": ["query", "explanation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_data_to_file",
            "description": "Export query results to a CSV or Excel file. Use this when the user wants to download or save data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "JSON string of the data to export (list of dictionaries)"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to create (without extension). Example: 'customer_report'"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["csv", "excel"],
                        "description": "File format to export - either 'csv' or 'excel'"
                    }
                },
                "required": ["data", "filename", "format"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_chart",
            "description": "Generate a chart visualization from data. Use this when the user wants to see a visual representation of data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "JSON string of the data to visualize (list of dictionaries)"
                    },
                    "chart_type": {
                        "type": "string",
                        "enum": ["bar", "line", "pie", "scatter"],
                        "description": "Type of chart to generate"
                    },
                    "x_column": {
                        "type": "string",
                        "description": "Name of the column to use for X-axis (or labels for pie chart)"
                    },
                    "y_column": {
                        "type": "string",
                        "description": "Name of the column to use for Y-axis (or values for pie chart)"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the chart"
                    }
                },
                "required": ["data", "chart_type", "x_column", "y_column", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "Create a GitHub issue as a support ticket. Use this when the user needs human assistance, reports a bug, has a complex request, or explicitly asks to create a support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Brief title for the support ticket"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue or request"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level of the ticket"
                    }
                },
                "required": ["title", "description", "priority"]
            }
        }
    }
]


class ToolExecutor:
    """
    Executes function calls from the OpenAI agent.
    """

    def __init__(self, db_manager, logger, safety_validator):
        """
        Initialize tool executor.

        Args:
            db_manager: DatabaseManager instance
            logger: AgentLogger instance
            safety_validator: SQLSafetyValidator instance
        """
        self.db = db_manager
        self.logger = logger
        self.validator = safety_validator

        # Initialize GitHub issue creator (lazy loading)
        self.github_creator = None
        self._init_github()

    def _init_github(self):
        """Initialize GitHub issue creator if credentials are available."""
        try:
            # Only initialize if env vars are set
            if os.getenv("GITHUB_TOKEN") and os.getenv("GITHUB_REPO"):
                self.github_creator = GitHubIssueCreator()
                self.logger.info("GitHub integration initialized successfully")
            else:
                self.logger.warning("GitHub integration not configured (GITHUB_TOKEN or GITHUB_REPO missing)")
        except Exception as e:
            self.logger.warning(f"GitHub integration initialization failed: {e}")
            self.github_creator = None

    def execute_sql_query(self, query: str, explanation: str) -> Dict[str, Any]:
        """
        Execute a SQL query on the database.

        Args:
            query: SQL query string
            explanation: Explanation of what the query does

        Returns:
            Dictionary with results and metadata
        """
        self.logger.log_function_call("execute_sql_query", {
            "query": query[:100],
            "explanation": explanation
        })

        # Validate query safety
        is_safe, error_msg = self.validator.validate_query(query)
        self.logger.log_safety_check(query, is_safe, error_msg)

        if not is_safe:
            return {
                "success": False,
                "error": f"Query blocked by safety validator: {error_msg}",
                "data": [],
                "row_count": 0
            }

        try:
            # Execute query
            results, columns = self.db.execute_query(query)
            row_count = len(results)

            self.logger.log_query(query, row_count)

            return {
                "success": True,
                "data": results,
                "columns": columns,
                "row_count": row_count,
                "explanation": explanation
            }

        except Exception as e:
            self.logger.log_error_with_context(e, "SQL query execution")
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "row_count": 0
            }

    def export_data_to_file(self, data: str, filename: str, format: str) -> Dict[str, Any]:
        """
        Export data to a file.

        Args:
            data: JSON string of data
            filename: Name of file (without extension)
            format: File format ('csv' or 'excel')

        Returns:
            Dictionary with export result
        """
        self.logger.log_function_call("export_data_to_file", {
            "filename": filename,
            "format": format
        })

        try:
            # Parse data
            data_list = json.loads(data) if isinstance(data, str) else data

            if not data_list:
                return {
                    "success": False,
                    "error": "No data to export",
                    "filepath": None
                }

            # Create exports directory if it doesn't exist
            os.makedirs("exports", exist_ok=True)

            # Convert to DataFrame
            df = pd.DataFrame(data_list)

            # Determine file path
            if format == "csv":
                filepath = f"exports/{filename}.csv"
                df.to_csv(filepath, index=False)
            elif format == "excel":
                filepath = f"exports/{filename}.xlsx"
                df.to_excel(filepath, index=False, engine='openpyxl')
            else:
                return {
                    "success": False,
                    "error": f"Unsupported format: {format}",
                    "filepath": None
                }

            self.logger.log_agent_action("data_export", f"Exported {len(df)} rows to {filepath}")

            return {
                "success": True,
                "filepath": filepath,
                "row_count": len(df),
                "format": format
            }

        except Exception as e:
            self.logger.log_error_with_context(e, "Data export")
            return {
                "success": False,
                "error": str(e),
                "filepath": None
            }

    def generate_chart(self, data: str, chart_type: str, x_column: str,
                      y_column: str, title: str) -> Dict[str, Any]:
        """
        Generate a chart from data.

        Args:
            data: JSON string of data
            chart_type: Type of chart ('bar', 'line', 'pie', 'scatter')
            x_column: Column for X-axis
            y_column: Column for Y-axis
            title: Chart title

        Returns:
            Dictionary with chart data for Plotly
        """
        self.logger.log_function_call("generate_chart", {
            "chart_type": chart_type,
            "title": title
        })

        try:
            # Parse data
            data_list = json.loads(data) if isinstance(data, str) else data

            if not data_list:
                return {
                    "success": False,
                    "error": "No data to visualize",
                    "chart_data": None
                }

            # Convert to DataFrame
            df = pd.DataFrame(data_list)

            # Validate columns
            if x_column not in df.columns:
                return {
                    "success": False,
                    "error": f"Column '{x_column}' not found in data",
                    "chart_data": None
                }

            if y_column not in df.columns:
                return {
                    "success": False,
                    "error": f"Column '{y_column}' not found in data",
                    "chart_data": None
                }

            # Prepare chart data
            chart_data = {
                "type": chart_type,
                "x": df[x_column].tolist(),
                "y": df[y_column].tolist(),
                "title": title,
                "x_label": x_column,
                "y_label": y_column
            }

            self.logger.log_agent_action("chart_generation",
                                        f"Generated {chart_type} chart with {len(df)} data points")

            return {
                "success": True,
                "chart_data": chart_data,
                "data_points": len(df)
            }

        except Exception as e:
            self.logger.log_error_with_context(e, "Chart generation")
            return {
                "success": False,
                "error": str(e),
                "chart_data": None
            }

    def create_support_ticket(self, title: str, description: str,
                             priority: str) -> Dict[str, Any]:
        """
        Create a support ticket (GitHub issue).

        Args:
            title: Ticket title
            description: Ticket description
            priority: Priority level (low, medium, high, critical)

        Returns:
            Dictionary with ticket creation result
        """
        self.logger.log_function_call("create_support_ticket", {
            "title": title,
            "priority": priority
        })

        # Check if GitHub integration is available
        if not self.github_creator:
            return {
                "success": False,
                "error": "GitHub integration not configured. Please set GITHUB_TOKEN and GITHUB_REPO in your .env file.",
                "ticket_url": None,
                "ticket_number": None
            }

        # Create the issue
        try:
            result = self.github_creator.create_issue(
                title=title,
                description=description,
                priority=priority
            )

            if result['success']:
                self.logger.info(f"Support ticket created: #{result['ticket_number']}")

            return result

        except Exception as e:
            self.logger.error(f"Error creating support ticket: {e}")
            return {
                "success": False,
                "error": f"Failed to create support ticket: {str(e)}",
                "ticket_url": None,
                "ticket_number": None
            }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments

        Returns:
            Dictionary with execution result
        """
        self.logger.log_agent_action("tool_execution", f"Executing {tool_name}")

        if tool_name == "execute_sql_query":
            return self.execute_sql_query(**arguments)
        elif tool_name == "export_data_to_file":
            return self.export_data_to_file(**arguments)
        elif tool_name == "generate_chart":
            return self.generate_chart(**arguments)
        elif tool_name == "create_support_ticket":
            return self.create_support_ticket(**arguments)
        else:
            self.logger.error(f"Unknown tool: {tool_name}")
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }


def get_tool_definitions() -> List[Dict]:
    """
    Get the list of tool definitions for OpenAI function calling.

    Returns:
        List of tool definition dictionaries
    """
    return TOOLS
