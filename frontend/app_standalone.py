"""
Standalone Streamlit App for Cloud Deployment
This version works without the FastAPI backend for demo purposes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import io
from pathlib import Path
import sys
import os

# Handle NLTK data download for Streamlit Cloud
try:
    import nltk
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        st.warning(f"NLTK data download failed: {e}. Some features may be limited.")
except ImportError:
    pass  # NLTK not available, continue without it

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
        margin-left: 0.5rem;
    }
    .data-agent {
        background-color: #28a745;
    }
    .research-agent {
        background-color: #17a2b8;
    }
    .orchestrator-agent {
        background-color: #6c757d;
    }
    .demo-note {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {'data': [], 'pdf': []}
if 'demo_data' not in st.session_state:
    st.session_state.demo_data = None

def load_sample_data():
    """Load sample data for demonstration"""
    # Create sample sales data
    sample_data = {
        'Date': ['2023-01-15', '2023-01-16', '2023-01-17', '2023-01-18', '2023-01-19'],
        'Product': ['Laptop Pro', 'Wireless Mouse', 'Office Chair', 'Laptop Pro', 'Desk Lamp'],
        'Category': ['Electronics', 'Electronics', 'Furniture', 'Electronics', 'Furniture'],
        'Sales': [1, 3, 2, 1, 1],
        'Revenue': [1200, 75, 400, 1200, 80],
        'Region': ['North', 'South', 'East', 'West', 'North']
    }
    return pd.DataFrame(sample_data)

def simulate_data_query(query: str, df: pd.DataFrame) -> Dict[str, Any]:
    """Simulate data intelligence agent responses"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['total', 'sum']) and 'revenue' in query_lower:
        total_revenue = df['Revenue'].sum()
        return {
            'agent': 'Data Intelligence Agent',
            'response': f"The total revenue is ${total_revenue:,}",
            'data': {'total_revenue': total_revenue}
        }
    
    elif any(word in query_lower for word in ['plot', 'chart', 'graph']) and 'revenue' in query_lower:
        fig = px.bar(df, x='Product', y='Revenue', title='Revenue by Product')
        return {
            'agent': 'Data Intelligence Agent',
            'response': 'Here\'s the revenue chart by product:',
            'chart': fig
        }
    
    elif 'top' in query_lower and 'product' in query_lower:
        top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(5)
        return {
            'agent': 'Data Intelligence Agent',
            'response': 'Top products by revenue:',
            'data': top_products.to_dict()
        }
    
    else:
        return {
            'agent': 'Data Intelligence Agent',
            'response': f"I can help you analyze data! Try asking about total revenue, plotting charts, or finding top products.",
            'suggestion': True
        }

def simulate_research_query(query: str) -> Dict[str, Any]:
    """Simulate research assistant agent responses"""
    query_lower = query.lower()
    
    if 'summarize' in query_lower or 'summary' in query_lower:
        return {
            'agent': 'Research Assistant Agent',
            'response': """**Research Paper Summary:**
            
This paper presents a comprehensive survey of deep learning approaches for computer vision. Key findings include:

• **Main Topic**: Deep learning architectures for image classification, object detection, and segmentation
• **Key Methods**: CNNs, ResNets, Vision Transformers, and attention mechanisms
• **Results**: Significant improvements in accuracy and efficiency across various vision tasks
• **Impact**: Revolutionary transformation of computer vision applications

The research demonstrates how modern deep learning has achieved human-level performance on many visual recognition tasks."""
        }
    
    elif any(word in query_lower for word in ['keyword', 'key terms', 'extract']):
        return {
            'agent': 'Research Assistant Agent',
            'response': """**Extracted Keywords:**
            
• Deep Learning
• Computer Vision
• Convolutional Neural Networks (CNNs)
• Vision Transformers
• Object Detection
• Image Classification
• Semantic Segmentation
• ResNet Architecture
• Transfer Learning
• Neural Architecture Search""",
            'keywords': ['Deep Learning', 'Computer Vision', 'CNNs', 'Vision Transformers', 'Object Detection']
        }
    
    elif any(word in query_lower for word in ['methodology', 'method', 'approach']):
        return {
            'agent': 'Research Assistant Agent',
            'response': """**Research Methodology:**

The study employs a systematic literature review approach:

1. **Literature Search**: Comprehensive search across IEEE, ACM, and arXiv databases
2. **Selection Criteria**: Focus on peer-reviewed papers from 2012-2023
3. **Analysis Framework**: Categorization by task type and architectural innovation
4. **Evaluation**: Quantitative comparison on standard benchmarks like ImageNet and COCO

The methodology ensures comprehensive coverage of recent advances in computer vision."""
        }
    
    else:
        return {
            'agent': 'Research Assistant Agent',
            'response': f"I can help analyze research documents! Try asking me to summarize papers, extract keywords, or explain methodologies.",
            'suggestion': True
        }

def get_agent_badge(agent_name: str) -> str:
    """Get HTML badge for agent"""
    if "Data Intelligence" in agent_name:
        return '<span class="agent-badge data-agent">📊 Data Intelligence Agent</span>'
    elif "Research Assistant" in agent_name:
        return '<span class="agent-badge research-agent">📄 Research Assistant Agent</span>'
    else:
        return '<span class="agent-badge orchestrator-agent">🤖 Orchestrator Agent</span>'

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Multi-Agent AI System</h1>', unsafe_allow_html=True)
    st.markdown("**Intelligent Data Analysis & Research Assistant** - *Demo Version*")
    
    # Demo notice
    st.markdown("""
    <div class="demo-note">
        <strong>🌟 Demo Mode:</strong> This is a demonstration version running on Streamlit Cloud. 
        The full system includes a FastAPI backend for complete functionality. 
        Try the sample queries below to see the AI agents in action!
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 File Management")
        
        # Load sample data button
        if st.button("📊 Load Sample Data", type="primary"):
            st.session_state.demo_data = load_sample_data()
            st.session_state.uploaded_files['data'].append("sample_sales_data.csv")
            st.success("✅ Sample sales data loaded!")
        
        # File upload section
        st.subheader("Upload Files")
        
        # Data file upload
        data_file = st.file_uploader(
            "📊 Upload Data File (CSV/Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="Upload CSV or Excel files for data analysis"
        )
        
        if data_file is not None:
            try:
                if data_file.name.endswith('.csv'):
                    df = pd.read_csv(data_file)
                else:
                    df = pd.read_excel(data_file)
                
                st.session_state.demo_data = df
                st.session_state.uploaded_files['data'].append(data_file.name)
                st.success(f"✅ {data_file.name} uploaded successfully!")
                
                # Show data preview
                with st.expander("📋 Data Preview"):
                    st.dataframe(df.head())
                    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
                    
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        # PDF file upload (demo)
        pdf_file = st.file_uploader(
            "📄 Upload Research Document (PDF)",
            type=['pdf'],
            help="Upload PDF documents for research analysis"
        )
        
        if pdf_file is not None:
            st.session_state.uploaded_files['pdf'].append(pdf_file.name)
            st.success(f"✅ {pdf_file.name} uploaded for research analysis!")
        
        # System status
        st.subheader("📊 System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Data Files", len(st.session_state.uploaded_files['data']))
        with col2:
            st.metric("Documents", len(st.session_state.uploaded_files['pdf']))
        
        # Clear data
        if st.button("🗑️ Clear All Data"):
            st.session_state.demo_data = None
            st.session_state.uploaded_files = {'data': [], 'pdf': []}
            st.session_state.chat_history = []
            st.success("✅ All data cleared")
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Example queries
    with st.expander("💡 Try These Example Queries", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Data Analysis Examples:**")
            if st.button("What is the total revenue?"):
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': "What is the total revenue?"
                })
                st.rerun()
            
            if st.button("Plot revenue by product"):
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': "Plot revenue by product"
                })
                st.rerun()
            
            if st.button("Show top products"):
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': "Show top products by revenue"
                })
                st.rerun()
        
        with col2:
            st.markdown("**📄 Research Examples:**")
            if st.button("Summarize the research paper"):
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': "Summarize the research paper"
                })
                st.rerun()
            
            if st.button("Extract key terms"):
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': "Extract key terms from the document"
                })
                st.rerun()
            
            if st.button("What methodology was used?"):
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': "What methodology was used in the research?"
                })
                st.rerun()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['type'] == 'user':
                st.markdown(f'<div style="background-color: #e3f2fd; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #2196f3;">👤 <strong>You:</strong> {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #f3e5f5; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #9c27b0;">🤖 <strong>Assistant:</strong></div>', 
                           unsafe_allow_html=True)
                
                result = message['content']
                
                # Show agent badge
                if 'agent' in result:
                    agent_badge = get_agent_badge(result['agent'])
                    st.markdown(f"**Processed by:** {agent_badge}", unsafe_allow_html=True)
                
                # Show response
                if 'response' in result:
                    if result.get('suggestion'):
                        st.info(result['response'])
                    else:
                        st.success(result['response'])
                
                # Show chart
                if 'chart' in result:
                    st.plotly_chart(result['chart'], use_container_width=True)
                
                # Show data
                if 'data' in result and not result.get('suggestion'):
                    st.json(result['data'])
    
    # Query input
    st.subheader("Ask a Question")
    
    # Query input form
    with st.form("query_form"):
        user_query = st.text_input(
            "Enter your question:",
            placeholder="Ask about your data or research documents...",
            help="I can analyze data files (CSV/Excel) or research documents (PDF)"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("🚀 Ask", type="primary")
        with col2:
            clear_chat = st.form_submit_button("🗑️ Clear Chat")
    
    # Handle clear chat
    if clear_chat:
        st.session_state.chat_history = []
        st.rerun()
    
    # Handle query submission
    if submit_button and user_query.strip():
        # Add user message to chat
        st.session_state.chat_history.append({
            'type': 'user',
            'content': user_query
        })
        
        # Determine query type and simulate response
        query_lower = user_query.lower()
        
        # Route to appropriate agent
        if any(word in query_lower for word in ['revenue', 'sales', 'total', 'plot', 'chart', 'product', 'data']):
            # Data Intelligence Agent
            if st.session_state.demo_data is not None:
                result = simulate_data_query(user_query, st.session_state.demo_data)
            else:
                result = {
                    'agent': 'Data Intelligence Agent',
                    'response': 'Please load sample data or upload a CSV/Excel file first!',
                    'suggestion': True
                }
        elif any(word in query_lower for word in ['research', 'paper', 'summarize', 'keyword', 'methodology', 'document']):
            # Research Assistant Agent
            result = simulate_research_query(user_query)
        else:
            # Orchestrator Agent
            result = {
                'agent': 'Orchestrator Agent',
                'response': 'I can help you with data analysis or research document queries. Please specify what you\'d like to analyze!',
                'suggestion': True
            }
        
        # Add assistant response to chat
        st.session_state.chat_history.append({
            'type': 'assistant',
            'content': result
        })
        
        # Rerun to update the chat display
        st.rerun()
    
    # Footer with system info
    st.markdown("---")
    st.markdown("""
    ### 🎯 Multi-Agent AI System Features:
    
    - **📊 Data Intelligence Agent**: Analyzes CSV/Excel files with natural language queries
    - **📄 Research Assistant Agent**: Processes research documents with AI-powered insights  
    - **🤖 Orchestrator Agent**: Intelligently routes queries to the appropriate specialist
    - **🎨 Interactive Interface**: Modern web interface with real-time responses
    - **📈 Smart Visualizations**: Automatic chart generation based on your questions
    
    **🔗 Full Version**: The complete system includes a FastAPI backend with advanced AI capabilities including vector databases, semantic search, and multi-modal processing.
    """)

if __name__ == "__main__":
    main()
