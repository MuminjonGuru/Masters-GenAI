"""
OpenAI LLM Agent with Function Calling
Main agent that interacts with users and executes functions
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI

from .tools import ToolExecutor, get_tool_definitions
from ..database.db_manager import DatabaseManager
from ..database.schema_helper import SchemaHelper
from ..utils.logger import get_logger
from .safety import SQLSafetyValidator


class NorthwindAgent:
    """
    AI Agent for interacting with the Northwind database.
    Uses OpenAI's function calling to execute tools.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Northwind agent.

        Args:
            api_key: OpenAI API key (if None, will use environment variable)
            model: OpenAI model to use (if None, will use OPENAI_MODEL env var or default to gpt-4-turbo)
        """
        # Initialize OpenAI client
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4-turbo")

        # Initialize components
        self.db = DatabaseManager()
        self.schema_helper = SchemaHelper(self.db)
        self.logger = get_logger()
        self.validator = SQLSafetyValidator()
        self.tool_executor = ToolExecutor(self.db, self.logger, self.validator)

        # Get database context
        self.schema_context = self.schema_helper.get_schema_for_llm()
        self.business_context = self.schema_helper.get_business_context()

        # Conversation history
        self.messages: List[Dict[str, Any]] = []

        # Initialize system prompt
        self._initialize_system_prompt()

        self.logger.info("Northwind Agent initialized successfully")
        self.logger.info(f"Using model: {self.model}")
        self.logger.info(f"Database tables: {len(self.db.get_all_tables())}")

    def _initialize_system_prompt(self):
        """Initialize the system prompt with database context."""
        system_prompt = f"""You are an AI assistant for the Northwind database (specialty food import/export company).

{self.schema_context}

**Capabilities**: Execute SQL queries, export data (CSV/Excel), generate charts, create support tickets.

**Guidelines**:
- Use double quotes for table names: "Order Details", "Orders"
- Only SELECT queries (read-only database)
- Be concise and helpful
- Offer visualizations for numerical data

All operations are logged."""

        self.messages = [{"role": "system", "content": system_prompt}]

    def chat(self, user_message: str, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Process a user message and return a response.

        Args:
            user_message: The user's message
            max_iterations: Maximum number of function calling iterations

        Returns:
            Dictionary containing response and metadata
        """
        self.logger.info(f"User message: {user_message}")

        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})

        iteration = 0
        tool_calls_made = []

        while iteration < max_iterations:
            iteration += 1
            self.logger.debug(f"Iteration {iteration}/{max_iterations}")

            try:
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=get_tool_definitions(),
                    tool_choice="auto"
                )

                assistant_message = response.choices[0].message

                # Check if we're done
                if assistant_message.content and not assistant_message.tool_calls:
                    # Add assistant response to history
                    self.messages.append({
                        "role": "assistant",
                        "content": assistant_message.content
                    })

                    self.logger.info(f"Agent response: {assistant_message.content[:100]}...")

                    return {
                        "success": True,
                        "response": assistant_message.content,
                        "tool_calls": tool_calls_made,
                        "iterations": iteration
                    }

                # Handle tool calls
                if assistant_message.tool_calls:
                    # Add assistant message with tool calls to history
                    self.messages.append({
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": tc.type,
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })

                    # Execute each tool call
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

                        self.logger.info(f"Executing function: {function_name}")

                        # Execute the tool
                        result = self.tool_executor.execute_tool(function_name, arguments)

                        # Track tool call
                        tool_calls_made.append({
                            "function": function_name,
                            "arguments": arguments,
                            "result": result
                        })

                        # Add tool result to messages
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })

                    # Continue to next iteration to get final response
                    continue

                # If we get here without content or tool calls, something's wrong
                self.logger.warning("Assistant message has no content or tool calls")
                break

            except Exception as e:
                self.logger.log_error_with_context(e, "Chat processing")
                return {
                    "success": False,
                    "error": str(e),
                    "tool_calls": tool_calls_made,
                    "iterations": iteration
                }

        # Max iterations reached
        self.logger.warning(f"Max iterations ({max_iterations}) reached")
        return {
            "success": False,
            "error": "Max iterations reached. The agent may be stuck in a loop.",
            "tool_calls": tool_calls_made,
            "iterations": iteration
        }

    def reset_conversation(self):
        """Reset the conversation history."""
        self.logger.info("Resetting conversation history")
        self._initialize_system_prompt()

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.

        Returns:
            List of message dictionaries
        """
        return self.messages.copy()

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with database statistics
        """
        return self.db.get_database_stats()


if __name__ == "__main__":
    # Test the agent
    print("=" * 70)
    print("NORTHWIND AGENT TEST")
    print("=" * 70)
    print()

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY environment variable not set")
        print("Please set it before running the agent test")
        exit(1)

    try:
        # Initialize agent
        agent = NorthwindAgent()

        print("[TEST 1] Database Statistics")
        stats = agent.get_database_stats()
        print(f"Total tables: {stats['total_tables']}")
        print(f"Total rows: {stats['total_rows']:,}")
        print()

        print("[TEST 2] Simple Query")
        response = agent.chat("How many customers do we have?")
        if response['success']:
            print(f"Response: {response['response']}")
            print(f"Tool calls made: {len(response['tool_calls'])}")
        else:
            print(f"Error: {response.get('error')}")
        print()

        print("[TEST 3] Reset Conversation")
        agent.reset_conversation()
        print("Conversation reset successfully")
        print()

        print("=" * 70)
        print("[SUCCESS] Agent test completed!")
        print("=" * 70)

    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)
