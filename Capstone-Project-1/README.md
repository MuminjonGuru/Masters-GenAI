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

## Tech Stack

- **Backend**: Python 3.9+
- **Frontend**: Streamlit
- **Database**: SQLite (Northwind sample database)
- **LLM**: OpenAI GPT-3.5-turbo/GPT-4 with function calling
- **Visualization**: Plotly, Matplotlib
- **Integration**: GitHub API for support tickets

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
- `OPENAI_API_KEY`: Your OpenAI API key
- `GITHUB_TOKEN`: Your GitHub personal access token
- `GITHUB_REPO`: Your GitHub repository (format: username/repo-name)

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

**Total Records**: 3000+ rows across all tables

## Usage Examples

(Screenshots and detailed usage instructions will be added here)

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

## Sample Queries

- "Show me the top 10 customers by total order value"
- "What are the most popular products?"
- "Export the list of all employees to Excel"
- "Create a chart showing sales by category"
- "I need help with a complex query, create a support ticket"

## Troubleshooting

### Common Issues

**Issue**: OpenAI API key error
- **Solution**: Make sure your `.env` file has the correct `OPENAI_API_KEY`

**Issue**: GitHub token error
- **Solution**: Verify your `GITHUB_TOKEN` has the necessary permissions (repo access)

**Issue**: Database locked
- **Solution**: Close any other applications that might be accessing northwind.db

## Architecture

(Architecture diagram and detailed explanation will be added here)

## Contributing

This is a capstone project. For issues or suggestions, please use the in-app support ticket feature or open a GitHub issue.

## License

MIT License

## Author

Masters in Generative AI - Capstone Project 1

---

**Note**: This application is for educational purposes and demonstrates the integration of LLMs with databases using function calling capabilities.
