"""
Visualization Utilities
Functions for creating charts and visualizations using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any, Optional


class ChartGenerator:
    """
    Generates various types of charts for data visualization.
    Uses Plotly for interactive charts that work well with Streamlit.
    """

    def __init__(self):
        """Initialize chart generator."""
        self.default_template = "plotly_white"
        self.color_palette = px.colors.qualitative.Set3

    def create_bar_chart(self, data: List[Dict[str, Any]], x_column: str,
                        y_column: str, title: str,
                        orientation: str = 'v') -> go.Figure:
        """
        Create a bar chart.

        Args:
            data: List of dictionaries containing data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            title: Chart title
            orientation: 'v' for vertical, 'h' for horizontal

        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame(data)

        fig = go.Figure(data=[
            go.Bar(
                x=df[x_column] if orientation == 'v' else df[y_column],
                y=df[y_column] if orientation == 'v' else df[x_column],
                orientation=orientation,
                marker_color=self.color_palette[0]
            )
        ])

        fig.update_layout(
            title=title,
            xaxis_title=x_column if orientation == 'v' else y_column,
            yaxis_title=y_column if orientation == 'v' else x_column,
            template=self.default_template,
            hovermode='x unified'
        )

        return fig

    def create_line_chart(self, data: List[Dict[str, Any]], x_column: str,
                         y_column: str, title: str,
                         group_by: Optional[str] = None) -> go.Figure:
        """
        Create a line chart.

        Args:
            data: List of dictionaries containing data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            title: Chart title
            group_by: Optional column to group lines by

        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame(data)

        if group_by and group_by in df.columns:
            fig = px.line(df, x=x_column, y=y_column, color=group_by,
                         title=title, template=self.default_template)
        else:
            fig = go.Figure(data=[
                go.Scatter(
                    x=df[x_column],
                    y=df[y_column],
                    mode='lines+markers',
                    line=dict(color=self.color_palette[1])
                )
            ])

            fig.update_layout(
                title=title,
                xaxis_title=x_column,
                yaxis_title=y_column,
                template=self.default_template,
                hovermode='x unified'
            )

        return fig

    def create_pie_chart(self, data: List[Dict[str, Any]], labels_column: str,
                        values_column: str, title: str) -> go.Figure:
        """
        Create a pie chart.

        Args:
            data: List of dictionaries containing data
            labels_column: Column name for labels
            values_column: Column name for values
            title: Chart title

        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame(data)

        fig = go.Figure(data=[
            go.Pie(
                labels=df[labels_column],
                values=df[values_column],
                marker=dict(colors=self.color_palette)
            )
        ])

        fig.update_layout(
            title=title,
            template=self.default_template
        )

        return fig

    def create_scatter_chart(self, data: List[Dict[str, Any]], x_column: str,
                           y_column: str, title: str,
                           size_column: Optional[str] = None,
                           color_column: Optional[str] = None) -> go.Figure:
        """
        Create a scatter plot.

        Args:
            data: List of dictionaries containing data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            title: Chart title
            size_column: Optional column for marker size
            color_column: Optional column for marker color

        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame(data)

        if color_column and color_column in df.columns:
            fig = px.scatter(df, x=x_column, y=y_column, color=color_column,
                           size=size_column if size_column in df.columns else None,
                           title=title, template=self.default_template)
        else:
            marker_size = df[size_column] if size_column and size_column in df.columns else 10

            fig = go.Figure(data=[
                go.Scatter(
                    x=df[x_column],
                    y=df[y_column],
                    mode='markers',
                    marker=dict(
                        size=marker_size,
                        color=self.color_palette[2]
                    )
                )
            ])

            fig.update_layout(
                title=title,
                xaxis_title=x_column,
                yaxis_title=y_column,
                template=self.default_template
            )

        return fig

    def create_grouped_bar_chart(self, data: List[Dict[str, Any]], x_column: str,
                                y_column: str, group_column: str,
                                title: str) -> go.Figure:
        """
        Create a grouped bar chart.

        Args:
            data: List of dictionaries containing data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            group_column: Column name to group bars by
            title: Chart title

        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame(data)

        fig = px.bar(df, x=x_column, y=y_column, color=group_column,
                    title=title, template=self.default_template,
                    barmode='group')

        return fig

    def create_histogram(self, data: List[Dict[str, Any]], column: str,
                        title: str, bins: int = 30) -> go.Figure:
        """
        Create a histogram.

        Args:
            data: List of dictionaries containing data
            column: Column name for histogram
            title: Chart title
            bins: Number of bins

        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame(data)

        fig = go.Figure(data=[
            go.Histogram(
                x=df[column],
                nbinsx=bins,
                marker_color=self.color_palette[3]
            )
        ])

        fig.update_layout(
            title=title,
            xaxis_title=column,
            yaxis_title="Count",
            template=self.default_template
        )

        return fig

    def create_chart(self, chart_type: str, data: List[Dict[str, Any]],
                    x_column: str, y_column: str, title: str,
                    **kwargs) -> go.Figure:
        """
        Create a chart of the specified type.

        Args:
            chart_type: Type of chart ('bar', 'line', 'pie', 'scatter')
            data: List of dictionaries containing data
            x_column: Column name for x-axis (or labels for pie)
            y_column: Column name for y-axis (or values for pie)
            title: Chart title
            **kwargs: Additional chart-specific arguments

        Returns:
            Plotly Figure object
        """
        if chart_type == 'bar':
            return self.create_bar_chart(data, x_column, y_column, title, **kwargs)
        elif chart_type == 'line':
            return self.create_line_chart(data, x_column, y_column, title, **kwargs)
        elif chart_type == 'pie':
            return self.create_pie_chart(data, x_column, y_column, title)
        elif chart_type == 'scatter':
            return self.create_scatter_chart(data, x_column, y_column, title, **kwargs)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")


class DashboardMetrics:
    """
    Helper class for creating dashboard metric cards and KPIs.
    """

    @staticmethod
    def calculate_kpis(data: List[Dict[str, Any]], metric_column: str) -> Dict[str, Any]:
        """
        Calculate basic KPIs for a metric.

        Args:
            data: List of dictionaries containing data
            metric_column: Column name for the metric

        Returns:
            Dictionary with KPI values
        """
        df = pd.DataFrame(data)

        if metric_column not in df.columns:
            return {}

        values = df[metric_column].dropna()

        return {
            'total': float(values.sum()),
            'average': float(values.mean()),
            'min': float(values.min()),
            'max': float(values.max()),
            'count': int(len(values))
        }

    @staticmethod
    def format_number(value: float, format_type: str = 'number') -> str:
        """
        Format a number for display.

        Args:
            value: Number to format
            format_type: Type of formatting ('number', 'currency', 'percent')

        Returns:
            Formatted string
        """
        if format_type == 'currency':
            return f"${value:,.2f}"
        elif format_type == 'percent':
            return f"{value:.1f}%"
        else:
            return f"{value:,.0f}"


if __name__ == "__main__":
    # Test the chart generator
    print("=" * 70)
    print("VISUALIZATION UTILITIES TEST")
    print("=" * 70)
    print()

    generator = ChartGenerator()

    # Test data
    test_data = [
        {"Month": "Jan", "Sales": 1200, "Category": "A"},
        {"Month": "Feb", "Sales": 1500, "Category": "A"},
        {"Month": "Mar", "Sales": 1800, "Category": "A"},
        {"Month": "Jan", "Sales": 900, "Category": "B"},
        {"Month": "Feb", "Sales": 1100, "Category": "B"},
        {"Month": "Mar", "Sales": 1300, "Category": "B"},
    ]

    # Test 1: Bar chart
    print("[TEST 1] Bar Chart")
    fig = generator.create_bar_chart(test_data[:3], "Month", "Sales", "Monthly Sales")
    print(f"Chart type: {type(fig).__name__}")
    print(f"Data points: {len(test_data[:3])}")
    print("[OK] Bar chart created")
    print()

    # Test 2: Line chart
    print("[TEST 2] Line Chart")
    fig = generator.create_line_chart(test_data[:3], "Month", "Sales", "Sales Trend")
    print(f"Chart type: {type(fig).__name__}")
    print("[OK] Line chart created")
    print()

    # Test 3: Pie chart
    print("[TEST 3] Pie Chart")
    pie_data = [
        {"Category": "Beverages", "Amount": 5000},
        {"Category": "Condiments", "Amount": 3000},
        {"Category": "Seafood", "Amount": 4000},
    ]
    fig = generator.create_pie_chart(pie_data, "Category", "Amount", "Sales by Category")
    print(f"Chart type: {type(fig).__name__}")
    print("[OK] Pie chart created")
    print()

    # Test 4: Scatter chart
    print("[TEST 4] Scatter Chart")
    scatter_data = [
        {"Price": 10, "Quantity": 100},
        {"Price": 15, "Quantity": 80},
        {"Price": 20, "Quantity": 60},
    ]
    fig = generator.create_scatter_chart(scatter_data, "Price", "Quantity", "Price vs Quantity")
    print(f"Chart type: {type(fig).__name__}")
    print("[OK] Scatter chart created")
    print()

    # Test 5: KPI calculation
    print("[TEST 5] KPI Calculation")
    metrics = DashboardMetrics()
    kpis = metrics.calculate_kpis(test_data, "Sales")
    print(f"Total: {metrics.format_number(kpis['total'], 'currency')}")
    print(f"Average: {metrics.format_number(kpis['average'], 'currency')}")
    print(f"Min: {metrics.format_number(kpis['min'], 'currency')}")
    print(f"Max: {metrics.format_number(kpis['max'], 'currency')}")
    print(f"Count: {kpis['count']}")
    print("[OK] KPIs calculated")
    print()

    print("=" * 70)
    print("[SUCCESS] Visualization utilities test complete!")
    print("=" * 70)
