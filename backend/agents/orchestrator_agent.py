"""
Orchestrator Agent
Routes user queries to appropriate specialized agents (Data Intelligence or Research Assistant)
based on query analysis and context.
"""

import re
from typing import Dict, Any, Optional, Tuple
from enum import Enum
from .data_intelligence_agent import DataIntelligenceAgent
from .research_assistant_agent import ResearchAssistantAgent

class QueryType(Enum):
    DATA_ANALYSIS = "data_analysis"
    RESEARCH_QUERY = "research_query"
    GENERAL = "general"
    AMBIGUOUS = "ambiguous"

class OrchestratorAgent:
    def __init__(self):
        self.data_agent = DataIntelligenceAgent()
        self.research_agent = ResearchAssistantAgent()
        
        # Keywords for query classification
        self.data_keywords = {
            'analysis': ['total', 'sum', 'average', 'mean', 'count', 'maximum', 'minimum', 
                        'plot', 'chart', 'graph', 'visualize', 'trend', 'sales', 'revenue',
                        'profit', 'expense', 'customer', 'product', 'data', 'csv', 'excel',
                        'table', 'column', 'row', 'filter', 'sort', 'group', 'aggregate'],
            'operations': ['load', 'upload', 'import', 'export', 'save', 'delete'],
            'visualization': ['show', 'display', 'plot', 'chart', 'graph', 'visualize', 
                            'bar', 'line', 'pie', 'scatter', 'histogram']
        }
        
        self.research_keywords = {
            'document': ['paper', 'document', 'pdf', 'research', 'study', 'article', 
                        'publication', 'journal', 'abstract', 'summary'],
            'analysis': ['summarize', 'extract', 'keyword', 'topic', 'theme', 'content',
                        'methodology', 'conclusion', 'finding', 'result'],
            'search': ['find', 'search', 'locate', 'identify', 'discover', 'lookup'],
            'questions': ['what', 'how', 'why', 'when', 'where', 'who', 'explain', 'describe']
        }
    
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main entry point for processing user queries
        Determines the appropriate agent and routes the query
        """
        try:
            # Classify the query
            query_type, confidence, reasoning = self._classify_query(query, context)
            
            # Route to appropriate agent
            if query_type == QueryType.DATA_ANALYSIS:
                result = self._route_to_data_agent(query, context)
            elif query_type == QueryType.RESEARCH_QUERY:
                result = self._route_to_research_agent(query, context)
            elif query_type == QueryType.AMBIGUOUS:
                result = self._handle_ambiguous_query(query, context)
            else:
                result = self._handle_general_query(query, context)
            
            # Add orchestrator metadata
            result['orchestrator_info'] = {
                'query_type': query_type.value,
                'confidence': confidence,
                'reasoning': reasoning,
                'agent_used': self._get_agent_name(query_type)
            }
            
            return result
            
        except Exception as e:
            return {
                "error": f"Orchestrator failed to process query: {str(e)}",
                "query": query
            }
    
    def _classify_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Tuple[QueryType, float, str]:
        """
        Classify the user query to determine which agent should handle it
        Returns: (QueryType, confidence_score, reasoning)
        """
        query_lower = query.lower()
        
        # Check for explicit file type mentions
        if any(ext in query_lower for ext in ['.csv', '.xlsx', '.xls', 'spreadsheet', 'excel']):
            return QueryType.DATA_ANALYSIS, 0.9, "Query mentions data file formats"
        
        if any(ext in query_lower for ext in ['.pdf', 'paper', 'document', 'research']):
            return QueryType.RESEARCH_QUERY, 0.9, "Query mentions research documents"
        
        # Score based on keyword matching
        data_score = self._calculate_keyword_score(query_lower, self.data_keywords)
        research_score = self._calculate_keyword_score(query_lower, self.research_keywords)
        
        # Consider context (loaded files)
        context_bias = self._get_context_bias(context)
        data_score += context_bias.get('data', 0)
        research_score += context_bias.get('research', 0)
        
        # Decision logic
        if data_score > research_score and data_score > 0.3:
            confidence = min(0.8, data_score)
            return QueryType.DATA_ANALYSIS, confidence, f"Data keywords score: {data_score:.2f}"
        elif research_score > data_score and research_score > 0.3:
            confidence = min(0.8, research_score)
            return QueryType.RESEARCH_QUERY, confidence, f"Research keywords score: {research_score:.2f}"
        elif abs(data_score - research_score) < 0.1 and max(data_score, research_score) > 0.2:
            return QueryType.AMBIGUOUS, 0.5, "Similar scores for both agents"
        else:
            return QueryType.GENERAL, 0.3, "No clear category match"
    
    def _calculate_keyword_score(self, query: str, keyword_categories: Dict[str, list]) -> float:
        """Calculate relevance score based on keyword matching"""
        total_score = 0
        total_weight = 0
        
        for category, keywords in keyword_categories.items():
            category_score = 0
            for keyword in keywords:
                if keyword in query:
                    # Longer keywords get higher weight
                    weight = len(keyword.split())
                    category_score += weight
            
            # Normalize by category size
            if keywords:
                category_score = category_score / len(keywords)
                total_score += category_score
                total_weight += 1
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def _get_context_bias(self, context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Get bias based on loaded files and context"""
        bias = {'data': 0, 'research': 0}
        
        if not context:
            return bias
        
        # Check for loaded data files
        if context.get('loaded_datasets'):
            bias['data'] += 0.2
        
        # Check for loaded research documents
        if context.get('loaded_documents'):
            bias['research'] += 0.2
        
        return bias
    
    def _route_to_data_agent(self, query: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Route query to Data Intelligence Agent"""
        try:
            # Check if we need to load data first
            if not self.data_agent.data_storage and context and context.get('pending_data_file'):
                file_path = context['pending_data_file']['path']
                file_name = context['pending_data_file']['name']
                load_result = self.data_agent.load_data(file_path, file_name)
                if 'error' in load_result:
                    return load_result
            
            # Process the query
            result = self.data_agent.process_query(query)
            result['agent'] = 'data_intelligence'
            return result
            
        except Exception as e:
            return {"error": f"Data agent failed: {str(e)}"}
    
    def _route_to_research_agent(self, query: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Route query to Research Assistant Agent"""
        try:
            # Check if we need to load documents first
            if not self.research_agent.documents and context and context.get('pending_pdf_file'):
                file_path = context['pending_pdf_file']['path']
                file_name = context['pending_pdf_file']['name']
                load_result = self.research_agent.load_pdf(file_path, file_name)
                if 'error' in load_result:
                    return load_result
            
            # Determine the type of research query
            if any(word in query.lower() for word in ['summarize', 'summary', 'abstract']):
                # Get document name from context or use first available
                doc_names = list(self.research_agent.documents.keys())
                if doc_names:
                    result = self.research_agent.summarize_document(doc_names[0])
                else:
                    result = {"error": "No documents loaded for summarization"}
            elif any(word in query.lower() for word in ['search', 'find', 'locate']):
                result = self.research_agent.search_documents(query)
            else:
                # Default to Q&A
                result = self.research_agent.answer_question(query)
            
            result['agent'] = 'research_assistant'
            return result
            
        except Exception as e:
            return {"error": f"Research agent failed: {str(e)}"}
    
    def _handle_ambiguous_query(self, query: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle queries that could apply to either agent"""
        # Try to disambiguate based on available data
        has_data = bool(self.data_agent.data_storage)
        has_docs = bool(self.research_agent.documents)
        
        if has_data and not has_docs:
            return self._route_to_data_agent(query, context)
        elif has_docs and not has_data:
            return self._route_to_research_agent(query, context)
        elif has_data and has_docs:
            # Ask user to clarify
            return {
                "ambiguous": True,
                "message": "Your query could apply to both data analysis and research documents. Please specify which you're interested in.",
                "suggestions": [
                    "For data analysis: " + query + " (from data files)",
                    "For research: " + query + " (from documents)"
                ],
                "available_data": list(self.data_agent.data_storage.keys()),
                "available_documents": list(self.research_agent.documents.keys())
            }
        else:
            return {
                "error": "No data files or documents loaded. Please upload files first.",
                "suggestion": "Upload CSV/Excel files for data analysis or PDF files for research queries"
            }
    
    def _handle_general_query(self, query: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle general queries about the system"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['help', 'what can you do', 'capabilities']):
            return {
                "success": True,
                "message": "I'm a multi-agent AI system that can help with:",
                "capabilities": [
                    "📊 Data Analysis: Upload CSV/Excel files and ask questions like 'What was the total sales in Q2?' or 'Plot revenue trends'",
                    "📄 Research Assistant: Upload PDF documents for summarization, keyword extraction, and Q&A",
                    "🤖 Smart Routing: I automatically determine whether your query is about data or research and route it to the right agent"
                ],
                "examples": [
                    "Data: 'Show me the top 5 customers by revenue'",
                    "Research: 'Summarize the paper on machine learning'",
                    "Research: 'What methodology was used in the study?'"
                ]
            }
        elif any(word in query_lower for word in ['status', 'what is loaded', 'files']):
            return self._get_system_status()
        else:
            return {
                "message": "I'm not sure how to help with that. Try asking about data analysis, research documents, or type 'help' for more information.",
                "suggestions": [
                    "Upload a CSV/Excel file and ask data questions",
                    "Upload a PDF document and ask research questions",
                    "Type 'help' to see what I can do"
                ]
            }
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "success": True,
            "system_status": {
                "loaded_datasets": list(self.data_agent.data_storage.keys()),
                "loaded_documents": list(self.research_agent.documents.keys()),
                "data_agent_ready": len(self.data_agent.data_storage) > 0,
                "research_agent_ready": len(self.research_agent.documents) > 0
            }
        }
    
    def _get_agent_name(self, query_type: QueryType) -> str:
        """Get agent name for query type"""
        if query_type == QueryType.DATA_ANALYSIS:
            return "Data Intelligence Agent"
        elif query_type == QueryType.RESEARCH_QUERY:
            return "Research Assistant Agent"
        else:
            return "Orchestrator Agent"
    
    # File handling methods
    def load_data_file(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Load data file through data agent"""
        return self.data_agent.load_data(file_path, file_name)
    
    def load_pdf_file(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Load PDF file through research agent"""
        return self.research_agent.load_pdf(file_path, file_name)
    
    def get_loaded_files(self) -> Dict[str, Any]:
        """Get information about all loaded files"""
        return {
            "datasets": self.data_agent.list_datasets(),
            "documents": self.research_agent.list_documents()
        }
    
    def clear_all_data(self) -> Dict[str, Any]:
        """Clear all loaded data and documents"""
        self.data_agent.data_storage.clear()
        self.data_agent.dataset_info.clear()
        self.research_agent.documents.clear()
        self.research_agent.embeddings.clear()
        self.research_agent.faiss_indexes.clear()
        
        return {
            "success": True,
            "message": "All data and documents cleared"
        }
