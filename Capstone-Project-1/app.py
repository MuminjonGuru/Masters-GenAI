"""
Northwind Data Insights Chat Application
Main Streamlit application file
"""

import streamlit as st
import os
import json
from dotenv import load_dotenv
import pandas as pd

# Import custom modules
from src.agent.llm_agent import NorthwindAgent
from src.database.db_manager import DatabaseManager
from src.utils.export import DataExporter
from src.utils.visualizations import ChartGenerator, DashboardMetrics

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Northwind Data Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'db_stats' not in st.session_state:
        st.session_state.db_stats = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False


def initialize_agent():
    """Initialize the Northwind agent."""
    if st.session_state.agent is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            st.stop()

        try:
            with st.spinner("Initializing Northwind Agent..."):
                st.session_state.agent = NorthwindAgent(api_key=api_key)
                st.session_state.db_stats = st.session_state.agent.get_database_stats()
                st.session_state.initialized = True
        except Exception as e:
            st.error(f"❌ Error initializing agent: {e}")
            st.stop()


def display_sidebar():
    """Display sidebar with database stats and controls."""
    with st.sidebar:
        st.markdown("### 📊 Database Information")

        if st.session_state.db_stats:
            stats = st.session_state.db_stats

            # Overall stats
            st.metric("Total Tables", stats['total_tables'])
            st.metric("Total Records", f"{stats['total_rows']:,}")

            st.markdown("---")

            # Top tables
            st.markdown("### 📋 Top Tables")
            sorted_tables = sorted(
                stats['tables'].items(),
                key=lambda x: x[1]['row_count'],
                reverse=True
            )[:5]

            for table, info in sorted_tables:
                st.markdown(f"**{table}**")
                st.caption(f"{info['row_count']:,} rows")

        st.markdown("---")

        # Sample queries
        st.markdown("### 💡 Sample Queries")
        sample_queries = [
            "How many customers do we have?",
            "Show top 5 products by sales",
            "List all employees",
            "What are the product categories?",
            "Show orders from last month"
        ]

        for query in sample_queries:
            if st.button(query, key=f"sample_{query}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()

        st.markdown("---")

        # Controls
        st.markdown("### ⚙️ Controls")

        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.reset_conversation()
            st.rerun()

        if st.button("📥 Export Chat", use_container_width=True):
            export_chat_history()


def export_chat_history():
    """Export chat history to a file."""
    if st.session_state.messages:
        exporter = DataExporter()
        chat_data = [
            {
                "role": msg["role"],
                "content": msg["content"][:500]  # Limit length
            }
            for msg in st.session_state.messages
        ]
        result = exporter.export_to_csv(chat_data, "chat_history", add_timestamp=True)
        if result['success']:
            st.sidebar.success(f"✅ Chat exported to {result['filepath']}")
        else:
            st.sidebar.error(f"❌ Export failed: {result['error']}")


def display_dashboard():
    """Display dashboard with key metrics."""
    st.markdown('<p class="main-header">📊 Northwind Data Insights</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Database Analytics Assistant</p>', unsafe_allow_html=True)

    if st.session_state.db_stats:
        stats = st.session_state.db_stats

        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="📋 Total Tables",
                value=stats['total_tables']
            )

        with col2:
            st.metric(
                label="📊 Total Records",
                value=f"{stats['total_rows']:,}"
            )

        with col3:
            # Count tables with data
            tables_with_data = sum(1 for t in stats['tables'].values() if t['row_count'] > 0)
            st.metric(
                label="✅ Active Tables",
                value=tables_with_data
            )

        with col4:
            # Largest table
            if stats['tables']:
                largest = max(stats['tables'].items(), key=lambda x: x[1]['row_count'])
                st.metric(
                    label="🔝 Largest Table",
                    value=largest[0],
                    delta=f"{largest[1]['row_count']:,} rows"
                )


def display_chat_interface():
    """Display chat interface."""
    st.markdown("---")
    st.markdown("### 💬 Chat with your Data")

    # Display chat messages
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                # Display tool calls if available
                if "tool_calls" in message and message["tool_calls"]:
                    with st.expander("🔧 Tool Calls", expanded=False):
                        for tool_call in message["tool_calls"]:
                            st.json(tool_call)

    # Chat input
    if prompt := st.chat_input("Ask me anything about the Northwind database..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.chat(prompt)

                if response['success']:
                    st.markdown(response['response'])

                    # Store assistant message with tool calls
                    assistant_message = {
                        "role": "assistant",
                        "content": response['response'],
                        "tool_calls": response.get('tool_calls', [])
                    }
                    st.session_state.messages.append(assistant_message)

                    # Display any charts or data
                    display_tool_results(response.get('tool_calls', []))

                else:
                    error_msg = f"❌ Error: {response.get('error', 'Unknown error')}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })


def display_tool_results(tool_calls):
    """Display results from tool calls (charts, data tables, etc.)."""
    if not tool_calls:
        return

    for tool_call in tool_calls:
        function_name = tool_call.get('function')
        result = tool_call.get('result', {})

        # Display query results as a table
        if function_name == 'execute_sql_query' and result.get('success'):
            data = result.get('data', [])
            if data:
                with st.expander(f"📊 Query Results ({result.get('row_count', 0)} rows)", expanded=True):
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)

        # Display chart
        if function_name == 'generate_chart' and result.get('success'):
            chart_data = result.get('chart_data', {})
            if chart_data:
                try:
                    from src.utils.visualizations import ChartGenerator
                    generator = ChartGenerator()

                    # Reconstruct data for chart
                    data = [
                        {chart_data['x_label']: x, chart_data['y_label']: y}
                        for x, y in zip(chart_data['x'], chart_data['y'])
                    ]

                    fig = generator.create_chart(
                        chart_data['type'],
                        data,
                        chart_data['x_label'],
                        chart_data['y_label'],
                        chart_data['title']
                    )

                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Chart display error: {e}")

        # Display export confirmation
        if function_name == 'export_data_to_file' and result.get('success'):
            st.success(f"✅ Data exported to: {result.get('filepath')}")
            st.info(f"📁 {result.get('row_count', 0)} rows exported")


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()

    # Initialize agent
    initialize_agent()

    # Display sidebar
    display_sidebar()

    # Main content
    display_dashboard()
    display_chat_interface()

    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Powered by OpenAI GPT • Built with Streamlit</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
