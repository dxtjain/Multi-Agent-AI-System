"""
Streamlit Frontend for Multi-Agent AI System
Provides an intuitive chat interface for data analysis and research queries
"""

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import pandas as pd
from typing import Dict, Any, Optional
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
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
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
    .success-message {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {'data': [], 'pdf': []}

# Helper functions
def make_api_request(endpoint: str, method: str = "GET", data: dict = None, files: dict = None) -> dict:
    """Make API request to the backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            return {"error": "Unsupported method"}
        
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend API. Make sure the FastAPI server is running."}
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

def get_agent_badge(agent_name: str) -> str:
    """Get HTML badge for agent"""
    if "data" in agent_name.lower():
        return '<span class="agent-badge data-agent">📊 Data Agent</span>'
    elif "research" in agent_name.lower():
        return '<span class="agent-badge research-agent">📄 Research Agent</span>'
    else:
        return '<span class="agent-badge orchestrator-agent">🤖 Orchestrator</span>'

def display_chart(chart_data: dict):
    """Display Plotly chart"""
    try:
        if 'chart_json' in chart_data:
            fig_dict = json.loads(chart_data['chart_json'])
            fig = go.Figure(fig_dict)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No chart data available")
    except Exception as e:
        st.error(f"Failed to display chart: {str(e)}")

def display_query_result(result: dict):
    """Display query result based on type"""
    if result.get('success'):
        # Show agent information
        if 'orchestrator_info' in result:
            info = result['orchestrator_info']
            agent_badge = get_agent_badge(info.get('agent_used', ''))
            st.markdown(f"**Query processed by:** {agent_badge}", unsafe_allow_html=True)
            
            with st.expander("🔍 Query Analysis"):
                st.write(f"**Type:** {info.get('query_type', 'N/A')}")
                st.write(f"**Confidence:** {info.get('confidence', 0):.2f}")
                st.write(f"**Reasoning:** {info.get('reasoning', 'N/A')}")
        
        # Display main result
        main_result = result.get('result', result)
        
        if 'chart_data' in main_result:
            st.subheader("📈 Visualization")
            display_chart(main_result['chart_data'])
        
        if 'message' in main_result:
            st.success(main_result['message'])
        
        if 'answer' in main_result:
            st.subheader("💡 Answer")
            st.write(main_result['answer'])
        
        if 'summary' in main_result:
            st.subheader("📋 Summary")
            st.write(main_result['summary'])
        
        if 'keywords' in main_result:
            st.subheader("🏷️ Keywords")
            st.write(", ".join(main_result['keywords']))
        
        if 'results' in main_result and isinstance(main_result['results'], list):
            st.subheader("📊 Results")
            df = pd.DataFrame(main_result['results'])
            st.dataframe(df, use_container_width=True)
        
        if 'relevant_chunks' in main_result:
            st.subheader("📖 Relevant Content")
            for i, chunk in enumerate(main_result['relevant_chunks'][:3]):
                with st.expander(f"Relevant passage {i+1} (Score: {chunk['score']:.2f})"):
                    st.write(chunk['text'])
        
        if 'suggestions' in main_result:
            st.subheader("💭 Suggestions")
            for suggestion in main_result['suggestions']:
                st.info(suggestion)
    
    elif result.get('ambiguous'):
        st.warning("🤔 " + result.get('message', 'Ambiguous query'))
        if 'suggestions' in result:
            st.subheader("💭 Suggestions")
            for suggestion in result['suggestions']:
                st.info(suggestion)
    
    else:
        st.error("❌ " + result.get('error', 'Unknown error'))

# Main UI
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Multi-Agent AI System</h1>', unsafe_allow_html=True)
    st.markdown("**Intelligent Data Analysis & Research Assistant**")
    
    # Sidebar
    with st.sidebar:
        st.header("📁 File Management")
        
        # File upload section
        st.subheader("Upload Files")
        
        # Data file upload
        data_file = st.file_uploader(
            "📊 Upload Data File (CSV/Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="Upload CSV or Excel files for data analysis"
        )
        
        if data_file is not None:
            if st.button("Upload Data File", key="upload_data"):
                with st.spinner("Uploading data file..."):
                    files = {"file": (data_file.name, data_file.getvalue(), data_file.type)}
                    result = make_api_request("/upload/data", method="POST", files=files)
                    
                    if result.get('success'):
                        st.success(f"✅ {result['message']}")
                        st.session_state.uploaded_files['data'].append(data_file.name)
                    else:
                        st.error(f"❌ {result.get('error', 'Upload failed')}")
        
        # PDF file upload
        pdf_file = st.file_uploader(
            "📄 Upload Research Document (PDF)",
            type=['pdf'],
            help="Upload PDF documents for research analysis"
        )
        
        if pdf_file is not None:
            if st.button("Upload PDF File", key="upload_pdf"):
                with st.spinner("Processing PDF document..."):
                    files = {"file": (pdf_file.name, pdf_file.getvalue(), pdf_file.type)}
                    result = make_api_request("/upload/pdf", method="POST", files=files)
                    
                    if result.get('success'):
                        st.success(f"✅ {result['message']}")
                        st.session_state.uploaded_files['pdf'].append(pdf_file.name)
                    else:
                        st.error(f"❌ {result.get('error', 'Upload failed')}")
        
        # System status
        st.subheader("📊 System Status")
        if st.button("🔄 Refresh Status"):
            status = make_api_request("/status")
            if status.get('success'):
                system_status = status['system_status']
                st.write("**Loaded Datasets:**")
                if system_status['loaded_datasets']:
                    for dataset in system_status['loaded_datasets']:
                        st.write(f"• {dataset}")
                else:
                    st.write("None")
                
                st.write("**Loaded Documents:**")
                if system_status['loaded_documents']:
                    for doc in system_status['loaded_documents']:
                        st.write(f"• {doc['name']}")
                else:
                    st.write("None")
            else:
                st.error("Failed to get status")
        
        # Clear data
        if st.button("🗑️ Clear All Data", type="secondary"):
            result = make_api_request("/files/clear", method="DELETE")
            if result.get('success'):
                st.success("✅ All data cleared")
                st.session_state.uploaded_files = {'data': [], 'pdf': []}
            else:
                st.error("❌ Failed to clear data")
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['type'] == 'user':
                st.markdown(f'<div class="chat-message user-message">👤 <strong>You:</strong> {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">🤖 <strong>Assistant:</strong></div>', 
                           unsafe_allow_html=True)
                display_query_result(message['content'])
    
    # Query input
    st.subheader("Ask a Question")
    
    # Example queries
    with st.expander("💡 Example Queries"):
        st.markdown("""
        **Data Analysis Examples:**
        - "What was the total sales in Q2?"
        - "Show me the top 5 customers by revenue"
        - "Plot revenue trends over time"
        - "What's the average order value?"
        
        **Research Examples:**
        - "Summarize the uploaded research paper"
        - "What methodology was used in the study?"
        - "Extract key findings from the document"
        - "Find papers about machine learning"
        """)
    
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
            clear_chat = st.form_submit_button("🗑️ Clear Chat", type="secondary")
    
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
        
        # Process query
        with st.spinner("🤔 Processing your query..."):
            query_data = {
                "query": user_query,
                "context": {
                    "loaded_datasets": st.session_state.uploaded_files['data'],
                    "loaded_documents": st.session_state.uploaded_files['pdf']
                }
            }
            
            result = make_api_request("/query", method="POST", data=query_data)
            
            # Add assistant response to chat
            st.session_state.chat_history.append({
                'type': 'assistant',
                'content': result
            })
        
        # Rerun to update the chat display
        st.rerun()
    
    # Help section
    with st.expander("❓ Help & Features"):
        st.markdown("""
        ### 🎯 What I Can Do:
        
        **📊 Data Intelligence Agent:**
        - Analyze CSV and Excel files
        - Answer questions about your data
        - Generate automatic visualizations
        - Perform aggregations (sum, average, count, etc.)
        - Show trends and rankings
        
        **📄 Research Assistant Agent:**
        - Process PDF research documents
        - Generate summaries and abstracts
        - Extract keywords and key findings
        - Answer questions about document content
        - Search across multiple documents
        
        **🤖 Smart Orchestrator:**
        - Automatically routes your queries to the right agent
        - Understands context and intent
        - Provides intelligent suggestions
        
        ### 🚀 Getting Started:
        1. Upload your files using the sidebar
        2. Ask questions in natural language
        3. Get intelligent responses with visualizations
        4. Explore your data and documents interactively
        """)

if __name__ == "__main__":
    main()
