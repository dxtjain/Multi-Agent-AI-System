# 🤖 Multi-Agent AI System for Data & Research Intelligence

A sophisticated multi-agent AI system that seamlessly handles both structured data analysis and unstructured research document processing through intelligent query routing and specialized agents.

## 🎯 Overview

This system consists of three specialized AI agents:

- **📊 Data Intelligence Agent**: Processes CSV/Excel files, answers business queries, and generates automatic visualizations
- **📄 Research Assistant Agent**: Handles PDF documents, provides summaries, keyword extraction, and Q&A capabilities
- **🤖 Orchestrator Agent**: Intelligently routes user queries to the appropriate agent based on context and intent

## ✨ Key Features

### Data Intelligence Agent
- 📈 **Natural Language Queries**: Ask questions like "What was the total sales in Q2?"
- 📊 **Automatic Visualizations**: Generate charts and graphs with simple requests
- 🔍 **Advanced Analytics**: Aggregations, trends, rankings, and filtering
- 📋 **Multiple File Formats**: Support for CSV and Excel files
- 💡 **Smart Insights**: Automatic data profiling and recommendations

### Research Assistant Agent
- 📖 **Document Summarization**: Generate concise abstracts from research papers
- 🏷️ **Keyword Extraction**: Identify key terms and concepts
- ❓ **Intelligent Q&A**: Answer questions about document content
- 🔎 **Semantic Search**: Find relevant information across multiple documents
- 📚 **Multi-document Support**: Handle multiple research papers simultaneously

### Orchestrator Agent
- 🧠 **Smart Routing**: Automatically determines which agent should handle each query
- 🎯 **Context Awareness**: Considers loaded files and query history
- 💭 **Disambiguation**: Helps clarify ambiguous queries
- 📊 **System Monitoring**: Provides status and usage insights

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multi-agent-ai-system
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend (Streamlit): http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. **Prerequisites**
   - Python 3.9+
   - pip package manager

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run the frontend (in a new terminal)**
   ```bash
   cd frontend
   streamlit run app.py --server.port 8501
   ```

5. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

## 📖 Usage Guide

### 1. Upload Files

**Data Files (CSV/Excel):**
- Use the sidebar to upload CSV or Excel files
- Supported formats: `.csv`, `.xlsx`, `.xls`
- Files are automatically processed and profiled

**Research Documents (PDF):**
- Upload PDF research papers or documents
- Text is extracted and processed for semantic search
- Embeddings are generated for intelligent Q&A

### 2. Ask Questions

The system supports natural language queries. Here are some examples:

**Data Analysis Queries:**
```
"What was the total revenue in Q1?"
"Show me the top 5 products by sales"
"Plot revenue trends over time"
"Which region has the highest performance?"
"Create a bar chart of sales by category"
```

**Research Queries:**
```
"Summarize the uploaded research paper"
"What methodology was used in the study?"
"Extract key findings from the document"
"What are the main challenges discussed?"
"Find papers about machine learning"
```

**System Queries:**
```
"What files are currently loaded?"
"Show me system status"
"Help me understand what you can do"
```

### 3. Interpret Results

The system provides rich, interactive responses:
- **📊 Visualizations**: Interactive Plotly charts
- **📋 Tables**: Formatted data tables
- **💡 Insights**: Key findings and summaries
- **🏷️ Metadata**: Query analysis and routing information

## 🏗️ Architecture

### System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI       │    │   AI Agents     │
│   Frontend      │◄──►│    Backend       │◄──►│   Orchestrator  │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                        ┌────────────────┼────────────────┐
                                        │                │                │
                                        ▼                ▼                ▼
                                ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
                                │     Data     │ │   Research   │ │  Additional  │
                                │ Intelligence │ │  Assistant   │ │   Agents     │
                                │    Agent     │ │    Agent     │ │   (Future)   │
                                └──────────────┘ └──────────────┘ └──────────────┘
```

### Technology Stack

**Backend:**
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **PyMuPDF**: PDF text extraction
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **NLTK**: Natural language processing

**Frontend:**
- **Streamlit**: Interactive web application framework
- **Plotly**: Chart rendering
- **Requests**: API communication

**Deployment:**
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Uvicorn**: ASGI server

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
STREAMLIT_PORT=8501

# AI Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
MAX_CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Logging
LOG_LEVEL=INFO
```

### Advanced Configuration

**Data Agent Settings:**
```python
# In backend/agents/data_intelligence_agent.py
DEFAULT_CHART_TYPE = "bar"
MAX_VISUALIZATION_POINTS = 1000
DEFAULT_TOP_N = 10
```

**Research Agent Settings:**
```python
# In backend/agents/research_assistant_agent.py
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MAX_CHUNK_SIZE = 500
SIMILARITY_THRESHOLD = 0.3
```

## 📊 API Documentation

### Core Endpoints

**File Upload:**
- `POST /upload/data` - Upload CSV/Excel files
- `POST /upload/pdf` - Upload PDF documents

**Query Processing:**
- `POST /query` - Process natural language queries

**System Management:**
- `GET /status` - Get system status
- `GET /files` - List loaded files
- `DELETE /files/clear` - Clear all data

**Data-Specific:**
- `GET /data/datasets` - List datasets
- `GET /data/summary/{name}` - Get dataset summary

**Research-Specific:**
- `GET /research/documents` - List documents
- `POST /research/search` - Search documents

### Example API Usage

```python
import requests

# Upload a data file
with open('sales_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload/data',
        files={'file': f}
    )

# Process a query
response = requests.post(
    'http://localhost:8000/query',
    json={
        'query': 'What was the total sales in Q1?',
        'context': {}
    }
)
```

## 🧪 Testing

### Sample Data

The `sample_data/` directory contains:
- `sales_data.csv`: Sample sales transactions
- `customer_data.csv`: Customer demographics
- `sample_research_paper.txt`: Research paper content

### Test Scenarios

1. **Data Analysis Test:**
   ```
   Upload: sales_data.csv
   Query: "Show me monthly revenue trends"
   Expected: Line chart with revenue over time
   ```

2. **Research Test:**
   ```
   Upload: research paper PDF
   Query: "Summarize the methodology section"
   Expected: Concise methodology summary
   ```

3. **Orchestrator Test:**
   ```
   Upload: Both data and research files
   Query: "What are the key findings?" (ambiguous)
   Expected: Disambiguation request
   ```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
python -m pytest tests/ -v
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup:**
   ```bash
   # Set production environment variables
   export NODE_ENV=production
   export API_HOST=0.0.0.0
   export API_PORT=8000
   ```

2. **Docker Production Build:**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Health Checks:**
   ```bash
   # Check backend health
   curl http://localhost:8000/health
   
   # Check frontend health
   curl http://localhost:8501/_stcore/health
   ```

### Scaling Considerations

- **Load Balancing**: Use nginx or similar for load balancing multiple backend instances
- **Database**: Consider PostgreSQL for persistent data storage
- **Caching**: Implement Redis for query result caching
- **Monitoring**: Use Prometheus and Grafana for system monitoring

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests:**
   ```bash
   python -m pytest tests/
   ```
5. **Submit a pull request**

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Write comprehensive tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain**: For multi-agent framework inspiration
- **Streamlit**: For the excellent web app framework
- **FastAPI**: For the modern API framework
- **Sentence Transformers**: For text embeddings
- **Plotly**: For interactive visualizations

## 📞 Support

For support, please:
1. Check the [FAQ](docs/FAQ.md)
2. Search existing [issues](https://github.com/your-repo/issues)
3. Create a new issue with detailed information

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] **Advanced NLP**: Integration with GPT-4 for better query understanding
- [ ] **Real-time Data**: Support for streaming data sources
- [ ] **Advanced Visualizations**: 3D charts and interactive dashboards
- [ ] **Multi-language Support**: Support for multiple languages
- [ ] **Cloud Integration**: AWS/Azure/GCP deployment options

### Version 2.1 (Future)
- [ ] **Voice Interface**: Voice-to-text query input
- [ ] **Mobile App**: React Native mobile application
- [ ] **Advanced Security**: OAuth2 and role-based access control
- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Custom Models**: Fine-tuned models for specific domains

---

**Built with ❤️ for intelligent data analysis and research assistance**
