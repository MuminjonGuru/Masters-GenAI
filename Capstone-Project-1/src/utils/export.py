"""
Data Export Utilities
Functions for exporting data to various formats (CSV, Excel)
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class DataExporter:
    """
    Handles data export to various file formats.
    """

    def __init__(self, export_dir: str = "exports"):
        """
        Initialize data exporter.

        Args:
            export_dir: Directory to save exported files
        """
        self.export_dir = export_dir
        self._ensure_export_dir()

    def _ensure_export_dir(self):
        """Create export directory if it doesn't exist."""
        os.makedirs(self.export_dir, exist_ok=True)

    def _generate_filename(self, base_name: str, extension: str, add_timestamp: bool = True) -> str:
        """
        Generate a filename with optional timestamp.

        Args:
            base_name: Base name for the file
            extension: File extension (without dot)
            add_timestamp: Whether to add timestamp to filename

        Returns:
            Generated filename
        """
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{base_name}_{timestamp}.{extension}"
        return f"{base_name}.{extension}"

    def export_to_csv(self, data: List[Dict[str, Any]], filename: str,
                     add_timestamp: bool = False) -> Dict[str, Any]:
        """
        Export data to CSV file.

        Args:
            data: List of dictionaries to export
            filename: Base filename (without extension)
            add_timestamp: Whether to add timestamp to filename

        Returns:
            Dictionary with export result
        """
        try:
            if not data:
                return {
                    "success": False,
                    "error": "No data to export",
                    "filepath": None
                }

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Generate filename
            full_filename = self._generate_filename(filename, "csv", add_timestamp)
            filepath = os.path.join(self.export_dir, full_filename)

            # Export to CSV
            df.to_csv(filepath, index=False, encoding='utf-8')

            return {
                "success": True,
                "filepath": filepath,
                "row_count": len(df),
                "column_count": len(df.columns),
                "file_size_kb": os.path.getsize(filepath) / 1024
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filepath": None
            }

    def export_to_excel(self, data: List[Dict[str, Any]], filename: str,
                       add_timestamp: bool = False, sheet_name: str = "Data") -> Dict[str, Any]:
        """
        Export data to Excel file.

        Args:
            data: List of dictionaries to export
            filename: Base filename (without extension)
            add_timestamp: Whether to add timestamp to filename
            sheet_name: Name of the Excel sheet

        Returns:
            Dictionary with export result
        """
        try:
            if not data:
                return {
                    "success": False,
                    "error": "No data to export",
                    "filepath": None
                }

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Generate filename
            full_filename = self._generate_filename(filename, "xlsx", add_timestamp)
            filepath = os.path.join(self.export_dir, full_filename)

            # Export to Excel with formatting
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Get the worksheet
                worksheet = writer.sheets[sheet_name]

                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

            return {
                "success": True,
                "filepath": filepath,
                "row_count": len(df),
                "column_count": len(df.columns),
                "file_size_kb": os.path.getsize(filepath) / 1024
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filepath": None
            }

    def export_multiple_sheets(self, data_dict: Dict[str, List[Dict[str, Any]]],
                              filename: str, add_timestamp: bool = False) -> Dict[str, Any]:
        """
        Export multiple datasets to different sheets in one Excel file.

        Args:
            data_dict: Dictionary mapping sheet names to data lists
            filename: Base filename (without extension)
            add_timestamp: Whether to add timestamp to filename

        Returns:
            Dictionary with export result
        """
        try:
            if not data_dict:
                return {
                    "success": False,
                    "error": "No data to export",
                    "filepath": None
                }

            # Generate filename
            full_filename = self._generate_filename(filename, "xlsx", add_timestamp)
            filepath = os.path.join(self.export_dir, full_filename)

            # Export to Excel with multiple sheets
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                total_rows = 0
                for sheet_name, data in data_dict.items():
                    if data:
                        df = pd.DataFrame(data)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        total_rows += len(df)

                        # Auto-adjust column widths
                        worksheet = writer.sheets[sheet_name]
                        for column in worksheet.columns:
                            max_length = 0
                            column_letter = column[0].column_letter
                            for cell in column:
                                try:
                                    if len(str(cell.value)) > max_length:
                                        max_length = len(str(cell.value))
                                except:
                                    pass
                            adjusted_width = min(max_length + 2, 50)
                            worksheet.column_dimensions[column_letter].width = adjusted_width

            return {
                "success": True,
                "filepath": filepath,
                "sheet_count": len(data_dict),
                "total_rows": total_rows,
                "file_size_kb": os.path.getsize(filepath) / 1024
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filepath": None
            }

    def get_export_files(self) -> List[str]:
        """
        Get list of all exported files.

        Returns:
            List of filenames in export directory
        """
        if not os.path.exists(self.export_dir):
            return []

        return [f for f in os.listdir(self.export_dir)
                if f.endswith(('.csv', '.xlsx'))]

    def delete_export_file(self, filename: str) -> bool:
        """
        Delete an exported file.

        Args:
            filename: Name of file to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            filepath = os.path.join(self.export_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except:
            return False


if __name__ == "__main__":
    # Test the exporter
    print("=" * 70)
    print("DATA EXPORT UTILITIES TEST")
    print("=" * 70)
    print()

    exporter = DataExporter()

    # Test data
    test_data = [
        {"CustomerID": "ALFKI", "CompanyName": "Alfreds Futterkiste", "Country": "Germany"},
        {"CustomerID": "ANATR", "CompanyName": "Ana Trujillo Emparedados", "Country": "Mexico"},
        {"CustomerID": "ANTON", "CompanyName": "Antonio Moreno Taquería", "Country": "Mexico"},
    ]

    # Test 1: CSV export
    print("[TEST 1] CSV Export")
    result = exporter.export_to_csv(test_data, "test_customers")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"File: {result['filepath']}")
        print(f"Rows: {result['row_count']}")
        print(f"Size: {result['file_size_kb']:.2f} KB")
    print()

    # Test 2: Excel export
    print("[TEST 2] Excel Export")
    result = exporter.export_to_excel(test_data, "test_customers_excel")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"File: {result['filepath']}")
        print(f"Rows: {result['row_count']}")
        print(f"Size: {result['file_size_kb']:.2f} KB")
    print()

    # Test 3: Multiple sheets
    print("[TEST 3] Multiple Sheets Export")
    multi_data = {
        "Customers": test_data,
        "Summary": [{"TotalCustomers": 3, "Countries": 2}]
    }
    result = exporter.export_multiple_sheets(multi_data, "test_multi_sheet")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"File: {result['filepath']}")
        print(f"Sheets: {result['sheet_count']}")
        print(f"Total rows: {result['total_rows']}")
    print()

    # Test 4: List exports
    print("[TEST 4] List Exported Files")
    files = exporter.get_export_files()
    print(f"Total files: {len(files)}")
    for f in files:
        print(f"  - {f}")
    print()

    print("=" * 70)
    print("[SUCCESS] Export utilities test complete!")
    print("=" * 70)
