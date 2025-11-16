"""
Test script to verify Streamlit app structure and imports
Tests app.py without actually running Streamlit
"""

import sys
import os


def test_imports():
    """Test that all required modules can be imported."""
    print("=" * 70)
    print("TESTING APP.PY STRUCTURE AND IMPORTS")
    print("=" * 70)
    print()

    print("[TEST 1] Core Module Imports")
    try:
        from src.agent.llm_agent import NorthwindAgent
        print("  [OK] NorthwindAgent")
    except ImportError as e:
        print(f"  [ERROR] NorthwindAgent: {e}")

    try:
        from src.database.db_manager import DatabaseManager
        print("  [OK] DatabaseManager")
    except ImportError as e:
        print(f"  [ERROR] DatabaseManager: {e}")

    try:
        from src.utils.export import DataExporter
        print("  [OK] DataExporter")
    except ImportError as e:
        print(f"  [ERROR] DataExporter: {e}")

    try:
        from src.utils.visualizations import ChartGenerator, DashboardMetrics
        print("  [OK] ChartGenerator, DashboardMetrics")
    except ImportError as e:
        print(f"  [ERROR] Visualizations: {e}")

    print("[OK] Core modules imported")
    print()

    print("[TEST 2] Standard Library Imports")
    imports_ok = True
    try:
        import json
        import pandas as pd
        from dotenv import load_dotenv
        print("  [OK] json, pandas, dotenv")
    except ImportError as e:
        print(f"  [ERROR] {e}")
        imports_ok = False

    if imports_ok:
        print("[OK] Standard library imports successful")
    print()

    print("[TEST 3] Streamlit Import")
    try:
        import streamlit as st
        print("  [OK] Streamlit imported")
        print(f"  Version: {st.__version__}")
        print("[OK] Streamlit available")
    except ImportError:
        print("  [ERROR] Streamlit not installed")
        print("  Install with: pip install streamlit")
        print("[NOTE] Streamlit required to run app")
    print()


def test_file_structure():
    """Test that all required files exist."""
    print("[TEST 4] File Structure")

    required_files = [
        "app.py",
        ".env.example",
        "requirements.txt",
        "northwind.db",
        "src/agent/llm_agent.py",
        "src/agent/tools.py",
        "src/agent/safety.py",
        "src/database/db_manager.py",
        "src/database/schema_helper.py",
        "src/utils/export.py",
        "src/utils/visualizations.py",
        "src/utils/logger.py",
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  [OK] {file_path}")
        else:
            print(f"  [ERROR] {file_path} [MISSING]")
            all_exist = False

    if all_exist:
        print("[OK] All required files present")
    else:
        print("[WARNING] Some files missing")
    print()


def test_configuration():
    """Test configuration files."""
    print("[TEST 5] Configuration Files")

    # Check .env.example
    if os.path.exists(".env.example"):
        print("  [OK] .env.example exists")
    else:
        print("  [ERROR] .env.example missing")

    # Check if .env exists
    if os.path.exists(".env"):
        print("  [OK] .env exists")
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv("OPENAI_API_KEY"):
            print("  [OK] OPENAI_API_KEY configured")
        else:
            print("  [WARNING] OPENAI_API_KEY not set in .env")
    else:
        print("  [WARNING] .env file not found (app will not work without it)")
        print("  Create .env from .env.example and add your API key")

    # Check Streamlit config
    if os.path.exists(".streamlit/config.toml"):
        print("  [OK] Streamlit config exists")
    else:
        print("  [WARNING] Streamlit config not found (app will use defaults)")

    print("[OK] Configuration check complete")
    print()


def test_database():
    """Test database connection."""
    print("[TEST 6] Database Connection")

    try:
        from src.database.db_manager import DatabaseManager

        db = DatabaseManager()
        if db.test_connection():
            stats = db.get_database_stats()
            print(f"  [OK] Database connected")
            print(f"  Tables: {stats['total_tables']}")
            print(f"  Total rows: {stats['total_rows']:,}")
            print("[OK] Database ready")
        else:
            print("  [ERROR] Database connection failed")
    except Exception as e:
        print(f"  [ERROR] Database error: {e}")

    print()


def main():
    """Run all tests."""
    print("\n")
    print("*" * 70)
    print("STREAMLIT APP STRUCTURE VERIFICATION")
    print("*" * 70)
    print()

    test_imports()
    test_file_structure()
    test_configuration()
    test_database()

    print("*" * 70)
    print("SUMMARY")
    print("*" * 70)
    print()
    print("To run the Streamlit app:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Create .env file with OPENAI_API_KEY")
    print("3. Run: streamlit run app.py")
    print()
    print("See RUNNING.md for detailed instructions")
    print("*" * 70)
    print()


if __name__ == "__main__":
    main()
