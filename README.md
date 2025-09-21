# 🤖 Multi-Agent AI System

> **Intelligent Data Analysis & Research Assistant Platform**

A sophisticated multi-agent AI system that seamlessly processes both structured business data and unstructured research documents through natural language queries and intelligent agent orchestration.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 🎯 Overview

This system addresses the common business challenge of analyzing both structured data (CSV/Excel files) and unstructured research documents (PDFs) through a single, intuitive interface. Instead of switching between different tools, users can ask natural language questions and get intelligent responses with automatic visualizations and insights.

### Key Features

- **🧠 Intelligent Query Routing**: Automatically determines whether your question is about data or research
- **📊 Data Intelligence**: Analyzes business data with natural language queries and auto-generated charts
- **📄 Research Assistant**: Processes research papers with summarization, keyword extraction, and Q&A
- **💬 Unified Chat Interface**: Single interface for all types of queries
- **📈 Interactive Visualizations**: Real-time charts and graphs based on your questions
- **🚀 Multiple Deployment Options**: Local, Docker, and cloud deployment ready

## 🏗️ System Architecture

The system follows a **multi-agent architecture pattern** with three specialized AI agents coordinated by an intelligent orchestrator:

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)                   │
│                     Natural Language Queries                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                            │
│              • Query Classification                             │
│              • Intent Recognition                               │
│              • Agent Routing                                    │
│              • Context Management                               │
└─────────────┬─────────────────────────────────┬─────────────────┘
              │                                 │
┌─────────────▼─────────────┐     ┌─────────────▼─────────────────┐
│   DATA INTELLIGENCE       │     │   RESEARCH ASSISTANT          │
│        AGENT               │     │         AGENT                 │
│                           │     │                               │
│ • CSV/Excel Processing    │     │ • PDF Text Extraction         │
│ • Pandas Integration      │     │ • Document Chunking           │
│ • SQL Query Generation    │     │ • Semantic Embeddings         │
│ • Chart Generation        │     │ • Vector Search (FAISS)       │
│ • Statistical Analysis    │     │ • Summarization               │
│                           │     │ • Keyword Extraction          │
└───────────────────────────┘     └───────────────────────────────┘
              │                                 │
┌─────────────▼─────────────────────────────────▼─────────────────┐
│                    BACKEND API (FastAPI)                        │
│               RESTful endpoints with OpenAPI docs               │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Components

**🎯 Orchestrator Agent**
- **Purpose**: Central coordinator that analyzes user queries and routes them to appropriate specialists
- **Technology**: Custom classification algorithm with keyword analysis and context awareness
- **Intelligence**: Handles query disambiguation and maintains conversation context

**📊 Data Intelligence Agent**
- **Purpose**: Specializes in structured data analysis and business intelligence
- **Technology**: Pandas for data processing, Plotly for visualizations, SQLite for storage
- **Capabilities**: Aggregations, trend analysis, statistical computations, automatic chart generation

**📄 Research Assistant Agent**
- **Purpose**: Handles unstructured document analysis and research tasks
- **Technology**: PyMuPDF for PDF processing, Sentence Transformers for embeddings, FAISS for vector search
- **Capabilities**: Document summarization, semantic search, keyword extraction, Q&A

**🌐 Unified Interface**
- **Frontend**: Streamlit-based web application with chat interface
- **Backend**: FastAPI REST API with automatic OpenAPI documentation
- **Communication**: RESTful API endpoints with JSON data exchange

## 🚀 Quick Start

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/multi-agent-ai-system.git
   cd multi-agent-ai-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the system**
   ```bash
   python run.py
   ```

4. **Access the application**
   - Frontend: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the services**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

### Option 3: Streamlit Cloud

1. **Deploy to Streamlit Cloud**
   - Fork this repository
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Deploy using `streamlit_app.py`

## 📖 How to Use

### 1. Upload Your Data

**For Data Analysis:**
- Upload CSV or Excel files containing your business data
- Supported formats: `.csv`, `.xlsx`, `.xls`
- Examples: sales data, customer information, financial records

**For Research Analysis:**
- Upload PDF research papers or documents
- The system will automatically extract and process the text
- Creates searchable embeddings for intelligent Q&A

### 2. Ask Natural Language Questions

**Data Analysis Examples:**
```
"What was the total revenue in Q2?"
"Show me the top 5 customers by sales"
"Plot monthly revenue trends"
"Which product category performs best?"
"Create a bar chart of sales by region"
```

**Research Analysis Examples:**
```
"Summarize this research paper"
"What methodology was used in the study?"
"Extract the key findings"
"What are the main challenges discussed?"
"Find information about machine learning approaches"
```

### 3. Get Intelligent Responses

The system automatically:
- **Routes** your query to the appropriate agent
- **Processes** the request using specialized algorithms
- **Generates** visualizations, summaries, or answers
- **Presents** results in an easy-to-understand format

## 📊 Sample Data

The repository includes sample datasets for testing:

- **`sales_data.csv`**: 40 sales transactions with product, revenue, and regional data
- **`customer_data.csv`**: 30 customer profiles with demographics and purchasing behavior
- **`sample_research_paper.txt`**: Research paper on computer vision and deep learning

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **SQLite**: Lightweight database for data storage
- **Uvicorn**: ASGI server for FastAPI

### AI & Machine Learning
- **Sentence Transformers**: Text embeddings for semantic search
- **FAISS**: Vector similarity search for document retrieval
- **NLTK**: Natural language processing toolkit
- **PyMuPDF**: PDF text extraction and processing

### Visualization
- **Plotly**: Interactive charts and graphs
- **Matplotlib**: Statistical plotting library
- **Seaborn**: Statistical data visualization

### Frontend
- **Streamlit**: Interactive web application framework
- **HTML/CSS**: Custom styling and responsive design

### Deployment
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container orchestration

## 📁 Project Structure

```
multi-agent-ai-system/
├── backend/                 # FastAPI backend application
│   ├── agents/             # AI agent implementations
│   │   ├── data_intelligence_agent.py
│   │   ├── research_assistant_agent.py
│   │   └── orchestrator_agent.py
│   └── main.py            # FastAPI application entry point
│
├── frontend/              # Streamlit frontend application
│   ├── app.py            # Full-featured app (with backend)
│   └── app_standalone.py # Standalone app (for cloud deployment)
│
├── docker/               # Docker configuration
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
│
├── sample_data/         # Sample datasets for testing
│   ├── sales_data.csv
│   ├── customer_data.csv
│   └── sample_research_paper.txt
│
├── .streamlit/          # Streamlit configuration
│   └── config.toml
│
├── requirements.txt     # Python dependencies
├── streamlit_requirements.txt  # Streamlit Cloud dependencies
├── docker-compose.yml   # Container orchestration
├── streamlit_app.py    # Cloud deployment entry point
└── run.py              # Local development launcher
```

## 🎥 Demo Video Guide

Create a compelling 2-3 minute demonstration:

### Structure (2-3 minutes total)

**1. Introduction (20 seconds)**
- Show the main interface
- Explain the multi-agent concept briefly

**2. Data Analysis Demo (60 seconds)**
- Upload the sample sales data
- Ask: "What was the total revenue in Q1?"
- Ask: "Plot monthly sales trends"
- Show the automatic chart generation

**3. Research Analysis Demo (60 seconds)**
- Upload a research document
- Ask: "Summarize this research paper"
- Ask: "What methodology was used?"
- Show the intelligent responses

**4. Smart Orchestration (40 seconds)**
- Ask mixed queries to show intelligent routing
- Demonstrate the system's ability to handle different types of questions
- Show the agent badges indicating which specialist handled each query

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file for custom configuration:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501

# Development
DEBUG=False
LOG_LEVEL=INFO
```

### Customization

- **Agent Behavior**: Modify agent parameters in respective Python files
- **UI Styling**: Update CSS in the Streamlit app files
- **Data Processing**: Extend the data intelligence agent for custom analysis
- **Document Processing**: Enhance the research assistant for specific document types

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent modern web framework
- **Streamlit**: For making web app development incredibly simple
- **Sentence Transformers**: For powerful text embeddings
- **Plotly**: For beautiful interactive visualizations
- **The Open Source Community**: For the amazing tools and libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check the existing [Issues](https://github.com/your-username/multi-agent-ai-system/issues)
2. Create a new issue with detailed information
3. Include steps to reproduce any problems

---

**Built with ❤️ for intelligent data analysis and research assistance**

> Transform your data analysis workflow with the power of AI agents working together seamlessly.