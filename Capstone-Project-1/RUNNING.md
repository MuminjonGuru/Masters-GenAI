# Running the Northwind Data Insights Application

## Quick Start Guide

### 1. Install Dependencies

First, install all required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

**Required:**
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo
```

**Optional (for GitHub support tickets):**
```
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=username/repository-name
```

### 3. Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Features

### 💬 Chat Interface
- Ask questions in natural language
- Get SQL-powered answers from the database
- View query results in interactive tables
- See conversation history

### 📊 Dashboard
- View database statistics
- See top tables by row count
- Monitor key metrics

### 🔧 Tools & Functions
- **SQL Query Execution**: Natural language to SQL
- **Data Export**: Download results as CSV or Excel
- **Chart Generation**: Create visualizations
- **Support Tickets**: Create GitHub issues (when configured)

### 💡 Sample Queries

The sidebar includes 7 pre-configured sample queries you can click to try:

- "How many customers do we have?"
- "Show top 5 products by sales"
- "List all employees"
- "What are the product categories?"
- "Show orders from 2023"
- "Create a support ticket for testing the integration"
- "I need help with a complex query, please create a support ticket"

**Tip**: Click any sample query to populate the input field, edit if needed, then send!

## Troubleshooting

### Issue: OpenAI API Key Error

**Error**: "OpenAI API key not found"

**Solution**: Make sure your `.env` file exists and contains:
```
OPENAI_API_KEY=sk-...your-key...
```

### Issue: Database Not Found

**Error**: "Database file not found: northwind.db"

**Solution**: Ensure `northwind.db` is in the project root directory.

### Issue: Module Not Found

**Error**: "No module named 'streamlit'" (or other modules)

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Charts Not Displaying

**Error**: Charts don't show up

**Solution**: Make sure Plotly is installed:
```bash
pip install plotly
```

## Testing Without API Key

You can test the database and utilities without an API key:

```bash
# Test database connection
python test_database.py

# Test safety and logging
python test_safety_logging.py

# Test utilities
python test_utilities.py

# Verify agent setup (no API needed)
python verify_agent_setup.py
```

## Project Structure

```
Capstone-Project-1/
├── app.py                  # Main Streamlit application
├── .env                    # Your environment variables (create this)
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
├── northwind.db          # SQLite database
│
├── src/
│   ├── agent/            # LLM agent and tools
│   ├── database/         # Database management
│   ├── utils/            # Utilities (export, charts, logging)
│   └── github_integration/  # Support tickets
│
└── exports/              # Exported files (created automatically)
```

## Tips for Best Experience

1. **Start Simple**: Try basic queries first to understand how the agent works
2. **Be Specific**: More specific questions get better results
3. **Use Sample Queries**: Click the sample queries in the sidebar
4. **Export Data**: Use the export feature to save interesting results
5. **Create Charts**: Ask for visualizations when appropriate
6. **Check Logs**: Watch the console for detailed operation logs

## Advanced Usage

### Custom Queries

You can ask complex questions like:

- "Show me customers from USA with more than 5 orders"
- "What's the average order value by country?"
- "List products that are low in stock"
- "Compare sales between Q1 and Q2"

### Data Export

Export results by asking:

- "Export this data to CSV"
- "Save the results as an Excel file"

### Visualizations

Request charts by asking:

- "Create a bar chart of this data"
- "Show me a pie chart of sales by category"
- "Make a line chart of monthly orders"

## Safety Features

The application includes built-in safety features:

- ✅ Read-only database access
- ✅ SQL injection prevention
- ✅ Query validation before execution
- ✅ No DELETE, UPDATE, or DROP operations allowed
- ✅ All operations logged to console

## Getting Help

- Check the sidebar for sample queries
- Review error messages in the chat
- Check console logs for detailed information
- Create a support ticket through the app (when configured)

---

**Enjoy exploring your data with AI! 🚀**
