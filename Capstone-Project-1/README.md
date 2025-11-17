# Northwind Data Insights Chat Application

A Streamlit-based AI-powered chat application that allows users to interact with the Northwind database using natural language queries. Built with OpenAI's GPT and function calling capabilities.

## Features

- **Natural Language Database Queries**: Ask questions in plain English and get SQL-powered answers
- **Intelligent Agent**: OpenAI-powered agent with function calling for:
  - SQL query execution with safety checks
  - Data export to CSV/Excel
  - Chart generation (bar, line, pie charts)
  - GitHub issue creation for support tickets
- **Business Dashboard**: View key metrics and database statistics at a glance
- **Safety Features**: Built-in SQL injection protection and query validation
- **Comprehensive Logging**: Console logging for all agent actions and queries

<details>
  <summary>📷 Click to expand screenshots (00 → 04)</summary>

  <!-- Center row of clickable thumbnails -->
  <p align="center">
    <a href="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/00.png" target="_blank">
      <img src="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/00.png" alt="screenshot-00" width="220" />
    </a>
    <a href="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/01.png" target="_blank">
      <img src="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/01.png" alt="screenshot-01" width="220" />
    </a>
    <a href="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/02.png" target="_blank">
      <img src="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/02.png" alt="screenshot-02" width="220" />
    </a>
    <a href="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/03.png" target="_blank">
      <img src="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/03.png" alt="screenshot-03" width="220" />
    </a>
    <a href="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/04.png" target="_blank">
      <img src="https://raw.githubusercontent.com/MuminjonGuru/Masters-GenAI/main/Capstone-Project-1/screenshots/04.png" alt="screenshot-04" width="220" />
    </a>
  </p>

  <sup>Click a thumbnail to open the full-size image in a new tab.</sup>
</details>


## Tech Stack

- **Backend**: Python 3.9+
- **Frontend**: Streamlit
- **Database**: SQLite (Northwind sample database)
- **LLM**: OpenAI GPT-4 Turbo with function calling
- **Visualization**: Plotly
- **Integration**: GitHub API (PyGithub) for support tickets

## Project Structure

```
Capstone-Project-1/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore file
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── northwind.db            # SQLite database
├── app.py                  # Main Streamlit application
│
├── src/
│   ├── agent/              # OpenAI agent and tools
│   ├── database/           # Database management
│   ├── utils/              # Utilities (export, charts, logging)
│   └── github_integration/ # GitHub issue creation
│
└── screenshots/            # Usage examples
```

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- GitHub personal access token (for support ticket creation)

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Capstone-Project-1
```

### 2. Create a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add:

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (default: `gpt-4-turbo`)

**Optional (for GitHub support tickets):**
- `GITHUB_TOKEN`: Your GitHub Personal Access Token (classic) with `repo` scope
  - Create at: https://github.com/settings/tokens
- `GITHUB_REPO`: Your GitHub repository (format: `username/repo-name`)
  - Example: `MuminjonGuru/Masters-GenAI`

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## About Northwind Database

The Northwind database is a sample database originally provided with Microsoft Access. It contains sales data for a fictional company called "Northwind Traders" which imports and exports specialty foods.

**Database Schema:**
- Customers
- Orders
- Order Details
- Products
- Categories
- Suppliers
- Employees
- Shippers

**Total Records**: 625,896+ rows across all tables (with 609,283 rows in Order Details alone)

## Usage Examples

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Sample Queries

The sidebar includes 7 pre-configured sample queries:
- "How many customers do we have?"
- "Show top 5 products by sales"
- "List all employees"
- "What are the product categories?"
- "Show orders from 2023"
- "Create a support ticket for testing the integration"
- "I need help with a complex query, please create a support ticket"

Click any sample query to populate the chat input, then press Enter or click "Send 🚀"

### Features Overview

1. **Natural Language Queries**: Ask questions in plain English
   - Example: "What are the top selling products in 2023?"

2. **Data Export**: Request exports in your queries
   - Example: "Export all customers to Excel"

3. **Visualizations**: Ask for charts and graphs
   - Example: "Create a bar chart of sales by category"

4. **Support Tickets**: Create GitHub issues for help
   - Example: "I need help analyzing customer trends, create a support ticket"

## Safety Features

- **SQL Query Validation**: Blocks dangerous operations (DELETE, DROP, TRUNCATE, ALTER, INSERT, UPDATE)
- **Read-Only Mode**: Database opened in read-only mode to prevent modifications
- **Query Sanitization**: Protection against SQL injection attacks
- **Result Limits**: Maximum 1000 rows per query to prevent memory issues

## Function Calling Tools

The agent has access to the following tools:

1. **execute_sql_query**: Execute read-only SQL queries on the database
2. **export_data_to_file**: Export query results to CSV or Excel
3. **generate_chart**: Create visualizations from data
4. **create_support_ticket**: Create GitHub issues for support requests

## Sample Queries (Available in Sidebar)

- "How many customers do we have?"
- "Show top 5 products by sales"
- "List all employees"
- "What are the product categories?"
- "Show orders from 2023"
- "Create a support ticket for testing the integration"
- "I need help with a complex query, please create a support ticket"

**Pro Tip**: Click any sample query to populate the input field, edit if needed, then send!

## Troubleshooting

### Common Issues

**Issue**: OpenAI API key error
- **Solution**: Make sure your `.env` file has the correct `OPENAI_API_KEY`

**Issue**: GitHub token error
- **Solution**: Verify your `GITHUB_TOKEN` has the necessary permissions (repo scope)
- Create token at: https://github.com/settings/tokens
- Select "repo" scope when creating the token

**Issue**: Context length exceeded error
- **Solution**: This has been optimized. If you still see this, you may be using an older model. Use `gpt-4-turbo` in your `.env` file.

**Issue**: Database locked
- **Solution**: Close any other applications that might be accessing northwind.db

## Architecture

### Data Flow

```
User Input (Streamlit UI)
    ↓
NorthwindAgent (OpenAI Function Calling)
    ↓
Tool Selection & Execution
    ├── execute_sql_query → SQLSafetyValidator → DatabaseManager → Results
    ├── export_data_to_file → DataExporter → CSV/Excel file
    ├── generate_chart → ChartGenerator → Plotly visualization
    └── create_support_ticket → GitHubIssueCreator → GitHub Issue
    ↓
Response to User (Streamlit UI)
```

### Key Components

- **app.py**: Streamlit UI with chat interface
- **src/agent/llm_agent.py**: OpenAI agent with GPT-4 Turbo
- **src/agent/tools.py**: Function calling tool definitions and executor
- **src/agent/safety.py**: SQL query safety validator
- **src/database/db_manager.py**: SQLite database operations (read-only)
- **src/database/schema_helper.py**: Optimized schema context for LLM
- **src/utils/export.py**: CSV/Excel data export
- **src/utils/visualizations.py**: Plotly chart generation
- **src/utils/logger.py**: Comprehensive logging system
- **src/github_integration/issue_creator.py**: GitHub API integration

See `CLAUDE.md` for detailed technical documentation.

## Contributing

This is a capstone project. For issues or suggestions, please use the in-app support ticket feature or open a GitHub issue.

## License

MIT License

## Author

Masters in Generative AI - Capstone Project 1

---

**Note**: This application is for educational purposes and demonstrates the integration of LLMs with databases using function calling capabilities.
