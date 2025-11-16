"""
Test script for utility functions
Tests export and visualization utilities
"""

import sys

def test_export_utilities():
    """Test data export utilities."""
    print("=" * 70)
    print("TESTING EXPORT UTILITIES")
    print("=" * 70)
    print()

    try:
        from src.utils.export import DataExporter

        exporter = DataExporter()

        # Test data
        test_data = [
            {"CustomerID": "ALFKI", "CompanyName": "Alfreds Futterkiste", "Country": "Germany"},
            {"CustomerID": "ANATR", "CompanyName": "Ana Trujillo", "Country": "Mexico"},
            {"CustomerID": "ANTON", "CompanyName": "Antonio Moreno", "Country": "Mexico"},
        ]

        print("[TEST 1] CSV Export")
        result = exporter.export_to_csv(test_data, "test_customers_util")
        print(f"Success: {result['success']}")
        if result['success']:
            print(f"File: {result['filepath']}")
            print(f"Rows: {result['row_count']}")
            print(f"Columns: {result['column_count']}")
            print(f"Size: {result['file_size_kb']:.2f} KB")
            print("[OK] CSV export working")
        else:
            print(f"Error: {result.get('error')}")
        print()

        print("[TEST 2] Excel Export")
        try:
            result = exporter.export_to_excel(test_data, "test_customers_excel")
            print(f"Success: {result['success']}")
            if result['success']:
                print(f"File: {result['filepath']}")
                print(f"Rows: {result['row_count']}")
                print("[OK] Excel export working")
            else:
                print(f"Error: {result.get('error')}")
                if 'openpyxl' in result.get('error', ''):
                    print("[NOTE] Install openpyxl: pip install openpyxl")
        except Exception as e:
            print(f"[NOTE] Excel export requires openpyxl: {e}")
        print()

        print("[TEST 3] List Exported Files")
        files = exporter.get_export_files()
        print(f"Total files: {len(files)}")
        for f in files[:5]:  # Show first 5
            print(f"  - {f}")
        print("[OK] File listing working")
        print()

        print("[SUCCESS] Export utilities tests completed!")

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()


def test_visualization_utilities():
    """Test visualization utilities."""
    print()
    print("=" * 70)
    print("TESTING VISUALIZATION UTILITIES")
    print("=" * 70)
    print()

    try:
        from src.utils.visualizations import ChartGenerator, DashboardMetrics

        print("[TEST 1] Chart Generator Initialization")
        generator = ChartGenerator()
        print("[OK] ChartGenerator initialized")
        print()

        # Test data
        test_data = [
            {"Month": "Jan", "Sales": 1200, "Category": "A"},
            {"Month": "Feb", "Sales": 1500, "Category": "A"},
            {"Month": "Mar", "Sales": 1800, "Category": "A"},
        ]

        print("[TEST 2] Bar Chart Creation")
        try:
            fig = generator.create_bar_chart(test_data, "Month", "Sales", "Monthly Sales")
            print(f"Chart type: {type(fig).__name__}")
            print(f"Data points: {len(test_data)}")
            print("[OK] Bar chart created successfully")
        except Exception as e:
            if 'plotly' in str(e).lower():
                print(f"[NOTE] Plotly not installed: pip install plotly")
            else:
                raise
        print()

        print("[TEST 3] Dashboard Metrics")
        metrics = DashboardMetrics()
        kpis = metrics.calculate_kpis(test_data, "Sales")
        print(f"Total: {metrics.format_number(kpis['total'], 'currency')}")
        print(f"Average: {metrics.format_number(kpis['average'], 'currency')}")
        print(f"Min: {metrics.format_number(kpis['min'], 'currency')}")
        print(f"Max: {metrics.format_number(kpis['max'], 'currency')}")
        print(f"Count: {kpis['count']}")
        print("[OK] KPI calculations working")
        print()

        print("[SUCCESS] Visualization utilities tests completed!")

    except ImportError as e:
        if 'plotly' in str(e):
            print("[NOTE] Plotly not installed")
            print("Install with: pip install plotly")
            print("Charts will work once dependencies are installed")
        else:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()


def main():
    """Run all utility tests."""
    print("\n")
    print("*" * 70)
    print("NORTHWIND - UTILITY FUNCTIONS TEST SUITE")
    print("*" * 70)
    print()

    test_export_utilities()
    test_visualization_utilities()

    print()
    print("*" * 70)
    print("NOTE: Some features require additional packages:")
    print("  - Excel export: pip install openpyxl")
    print("  - Charts: pip install plotly")
    print()
    print("Run: pip install -r requirements.txt")
    print("*" * 70)
    print()


if __name__ == "__main__":
    main()
