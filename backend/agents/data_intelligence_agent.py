"""
Data Intelligence Agent
Handles structured data analysis (CSV/Excel files) with natural language queries
and automatic visualization generation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple
import sqlite3
import io
import base64
from pathlib import Path
import json
import re
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataIntelligenceAgent:
    def __init__(self):
        self.data_storage = {}  # Store loaded datasets
        self.db_connection = None
        self.current_dataset = None
        self.dataset_info = {}
        
    def load_data(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Load CSV or Excel file into pandas DataFrame"""
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                return {"error": f"Unsupported file format: {file_extension}"}
            
            # Store the dataset
            self.data_storage[file_name] = df
            self.current_dataset = file_name
            
            # Generate dataset info
            info = self._generate_dataset_info(df, file_name)
            self.dataset_info[file_name] = info
            
            return {
                "success": True,
                "message": f"Successfully loaded {file_name}",
                "info": info
            }
            
        except Exception as e:
            return {"error": f"Failed to load file: {str(e)}"}
    
    def _generate_dataset_info(self, df: pd.DataFrame, file_name: str) -> Dict[str, Any]:
        """Generate comprehensive information about the dataset"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        datetime_columns = []
        
        # Try to identify datetime columns
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col].head(), errors='raise')
                    datetime_columns.append(col)
                    categorical_columns.remove(col)
                except:
                    pass
        
        return {
            "file_name": file_name,
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "datetime_columns": datetime_columns,
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(3).to_dict('records')
        }
    
    def process_query(self, query: str, dataset_name: Optional[str] = None) -> Dict[str, Any]:
        """Process natural language queries about the data"""
        if not dataset_name:
            dataset_name = self.current_dataset
            
        if not dataset_name or dataset_name not in self.data_storage:
            return {"error": "No dataset loaded. Please upload a file first."}
        
        df = self.data_storage[dataset_name]
        query_lower = query.lower()
        
        try:
            # Query classification and processing
            if any(word in query_lower for word in ['total', 'sum', 'add']):
                return self._handle_aggregation_query(df, query, 'sum')
            elif any(word in query_lower for word in ['average', 'mean', 'avg']):
                return self._handle_aggregation_query(df, query, 'mean')
            elif any(word in query_lower for word in ['maximum', 'max', 'highest']):
                return self._handle_aggregation_query(df, query, 'max')
            elif any(word in query_lower for word in ['minimum', 'min', 'lowest']):
                return self._handle_aggregation_query(df, query, 'min')
            elif any(word in query_lower for word in ['count', 'number of']):
                return self._handle_count_query(df, query)
            elif any(word in query_lower for word in ['plot', 'chart', 'graph', 'visualize', 'show']):
                return self._handle_visualization_query(df, query)
            elif any(word in query_lower for word in ['trend', 'over time', 'timeline']):
                return self._handle_trend_query(df, query)
            elif any(word in query_lower for word in ['top', 'bottom', 'rank']):
                return self._handle_ranking_query(df, query)
            elif any(word in query_lower for word in ['filter', 'where', 'condition']):
                return self._handle_filter_query(df, query)
            else:
                return self._handle_general_query(df, query)
                
        except Exception as e:
            return {"error": f"Failed to process query: {str(e)}"}
    
    def _handle_aggregation_query(self, df: pd.DataFrame, query: str, operation: str) -> Dict[str, Any]:
        """Handle aggregation queries (sum, mean, max, min)"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Try to identify the column from the query
        target_column = None
        for col in df.columns:
            if col.lower() in query.lower():
                target_column = col
                break
        
        if target_column and target_column in numeric_cols:
            if operation == 'sum':
                result = df[target_column].sum()
            elif operation == 'mean':
                result = df[target_column].mean()
            elif operation == 'max':
                result = df[target_column].max()
            elif operation == 'min':
                result = df[target_column].min()
            
            return {
                "success": True,
                "result": result,
                "message": f"The {operation} of {target_column} is {result:,.2f}",
                "query_type": "aggregation"
            }
        else:
            # If no specific column found, show aggregations for all numeric columns
            results = {}
            for col in numeric_cols:
                if operation == 'sum':
                    results[col] = df[col].sum()
                elif operation == 'mean':
                    results[col] = df[col].mean()
                elif operation == 'max':
                    results[col] = df[col].max()
                elif operation == 'min':
                    results[col] = df[col].min()
            
            return {
                "success": True,
                "results": results,
                "message": f"{operation.title()} values for all numeric columns",
                "query_type": "aggregation"
            }
    
    def _handle_count_query(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Handle counting queries"""
        return {
            "success": True,
            "result": len(df),
            "message": f"Total number of records: {len(df):,}",
            "query_type": "count"
        }
    
    def _handle_visualization_query(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Handle visualization requests"""
        query_lower = query.lower()
        
        # Determine chart type
        if 'bar' in query_lower or 'column' in query_lower:
            chart_type = 'bar'
        elif 'line' in query_lower or 'trend' in query_lower:
            chart_type = 'line'
        elif 'pie' in query_lower:
            chart_type = 'pie'
        elif 'scatter' in query_lower:
            chart_type = 'scatter'
        elif 'histogram' in query_lower or 'distribution' in query_lower:
            chart_type = 'histogram'
        else:
            chart_type = 'bar'  # default
        
        # Try to identify columns mentioned in the query
        mentioned_cols = [col for col in df.columns if col.lower() in query_lower]
        
        if not mentioned_cols:
            # Use first few columns as default
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            
            if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                x_col = categorical_cols[0]
                y_col = numeric_cols[0]
            elif len(numeric_cols) > 1:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
            else:
                return {"error": "Unable to determine appropriate columns for visualization"}
        else:
            if len(mentioned_cols) == 1:
                col = mentioned_cols[0]
                if df[col].dtype in ['object']:
                    x_col = col
                    y_col = None  # For count plots
                else:
                    x_col = None
                    y_col = col
            else:
                x_col = mentioned_cols[0]
                y_col = mentioned_cols[1]
        
        # Generate the visualization
        chart_data = self._create_chart(df, chart_type, x_col, y_col)
        
        return {
            "success": True,
            "chart_data": chart_data,
            "message": f"Generated {chart_type} chart",
            "query_type": "visualization"
        }
    
    def _handle_trend_query(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Handle trend analysis queries"""
        datetime_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col].head(), errors='raise')
                    datetime_cols.append(col)
                except:
                    pass
        
        if not datetime_cols:
            return {"error": "No datetime columns found for trend analysis"}
        
        date_col = datetime_cols[0]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return {"error": "No numeric columns found for trend analysis"}
        
        # Convert date column to datetime
        df_copy = df.copy()
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
        df_copy = df_copy.sort_values(date_col)
        
        # Create trend chart
        chart_data = self._create_trend_chart(df_copy, date_col, numeric_cols[0])
        
        return {
            "success": True,
            "chart_data": chart_data,
            "message": f"Generated trend analysis for {numeric_cols[0]} over time",
            "query_type": "trend"
        }
    
    def _handle_ranking_query(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Handle ranking queries (top/bottom N)"""
        query_lower = query.lower()
        
        # Extract number if mentioned
        import re
        numbers = re.findall(r'\d+', query)
        n = int(numbers[0]) if numbers else 5
        
        # Determine if top or bottom
        ascending = 'bottom' in query_lower or 'lowest' in query_lower
        
        # Try to identify the column
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        target_column = None
        
        for col in df.columns:
            if col.lower() in query_lower:
                target_column = col
                break
        
        if not target_column and len(numeric_cols) > 0:
            target_column = numeric_cols[0]
        
        if target_column:
            ranked_data = df.nlargest(n, target_column) if not ascending else df.nsmallest(n, target_column)
            
            return {
                "success": True,
                "result": ranked_data.to_dict('records'),
                "message": f"{'Bottom' if ascending else 'Top'} {n} records by {target_column}",
                "query_type": "ranking"
            }
        else:
            return {"error": "Could not identify column for ranking"}
    
    def _handle_filter_query(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Handle filtering queries"""
        # This is a simplified implementation
        # In a production system, you'd want more sophisticated NLP parsing
        return {
            "success": True,
            "message": "Filter functionality would require more specific query parsing",
            "suggestion": "Please specify exact filter conditions",
            "query_type": "filter"
        }
    
    def _handle_general_query(self, df: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Handle general queries about the dataset"""
        return {
            "success": True,
            "info": self.dataset_info.get(self.current_dataset, {}),
            "message": "Here's general information about your dataset",
            "query_type": "general"
        }
    
    def _create_chart(self, df: pd.DataFrame, chart_type: str, x_col: str, y_col: str) -> Dict[str, Any]:
        """Create chart using Plotly"""
        try:
            if chart_type == 'bar':
                if y_col is None:  # Count plot
                    value_counts = df[x_col].value_counts().head(10)
                    fig = px.bar(x=value_counts.index, y=value_counts.values,
                               title=f'Count of {x_col}',
                               labels={'x': x_col, 'y': 'Count'})
                else:
                    # Group by x_col and aggregate y_col
                    grouped = df.groupby(x_col)[y_col].sum().head(10)
                    fig = px.bar(x=grouped.index, y=grouped.values,
                               title=f'{y_col} by {x_col}',
                               labels={'x': x_col, 'y': y_col})
            
            elif chart_type == 'line':
                fig = px.line(df.head(100), x=x_col, y=y_col,
                            title=f'{y_col} over {x_col}')
            
            elif chart_type == 'pie':
                if y_col is None:
                    value_counts = df[x_col].value_counts().head(8)
                    fig = px.pie(values=value_counts.values, names=value_counts.index,
                               title=f'Distribution of {x_col}')
                else:
                    grouped = df.groupby(x_col)[y_col].sum().head(8)
                    fig = px.pie(values=grouped.values, names=grouped.index,
                               title=f'{y_col} distribution by {x_col}')
            
            elif chart_type == 'scatter':
                fig = px.scatter(df.head(1000), x=x_col, y=y_col,
                               title=f'{y_col} vs {x_col}')
            
            elif chart_type == 'histogram':
                fig = px.histogram(df, x=y_col if y_col else x_col,
                                 title=f'Distribution of {y_col if y_col else x_col}')
            
            # Convert to JSON for frontend
            chart_json = fig.to_json()
            
            return {
                "chart_json": chart_json,
                "chart_type": chart_type,
                "x_column": x_col,
                "y_column": y_col
            }
            
        except Exception as e:
            return {"error": f"Failed to create chart: {str(e)}"}
    
    def _create_trend_chart(self, df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, Any]:
        """Create trend chart for time series data"""
        try:
            fig = px.line(df, x=date_col, y=value_col,
                         title=f'{value_col} Trend Over Time')
            
            chart_json = fig.to_json()
            
            return {
                "chart_json": chart_json,
                "chart_type": "line",
                "x_column": date_col,
                "y_column": value_col
            }
            
        except Exception as e:
            return {"error": f"Failed to create trend chart: {str(e)}"}
    
    def get_dataset_summary(self, dataset_name: Optional[str] = None) -> Dict[str, Any]:
        """Get summary of the current or specified dataset"""
        if not dataset_name:
            dataset_name = self.current_dataset
            
        if not dataset_name or dataset_name not in self.data_storage:
            return {"error": "No dataset available"}
        
        return {
            "success": True,
            "summary": self.dataset_info[dataset_name]
        }
    
    def list_datasets(self) -> List[str]:
        """List all loaded datasets"""
        return list(self.data_storage.keys())
