"""
Research Assistant Agent
Handles unstructured document analysis (PDF files) with summarization,
keyword extraction, and Q&A capabilities.
"""

import fitz  # PyMuPDF
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import re
import json
from pathlib import Path
import hashlib
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pickle
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResearchAssistantAgent:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
        self.documents = {}  # Store document content and metadata
        self.embeddings = {}  # Store document embeddings
        self.faiss_indexes = {}  # Store FAISS indexes for each document
        self.stop_words = set(stopwords.words('english'))
        
    def load_pdf(self, file_path: str, file_name: str) -> Dict[str, Any]:
        """Load and process PDF document"""
        try:
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(file_path)
            
            if not text_content.strip():
                return {"error": "No text content found in PDF"}
            
            # Process the document
            processed_doc = self._process_document(text_content, file_name)
            
            # Store document
            self.documents[file_name] = processed_doc
            
            # Generate embeddings
            embeddings = self._generate_embeddings(processed_doc['chunks'])
            self.embeddings[file_name] = embeddings
            
            # Create FAISS index
            self._create_faiss_index(file_name, embeddings)
            
            return {
                "success": True,
                "message": f"Successfully processed {file_name}",
                "info": {
                    "file_name": file_name,
                    "total_pages": processed_doc['metadata']['total_pages'],
                    "total_chunks": len(processed_doc['chunks']),
                    "word_count": processed_doc['metadata']['word_count'],
                    "summary": processed_doc['summary'][:200] + "..." if len(processed_doc['summary']) > 200 else processed_doc['summary']
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to process PDF: {str(e)}"}
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""
        text = ""
        try:
            # Try with PyMuPDF first
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            doc.close()
        except Exception as e1:
            try:
                # Fallback to pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
            except Exception as e2:
                raise Exception(f"Failed to extract text with both methods: {str(e1)}, {str(e2)}")
        
        return text
    
    def _process_document(self, text: str, file_name: str) -> Dict[str, Any]:
        """Process document text into chunks and extract metadata"""
        # Clean text
        cleaned_text = self._clean_text(text)
        
        # Split into chunks
        chunks = self._split_into_chunks(cleaned_text)
        
        # Generate summary
        summary = self._generate_summary(cleaned_text)
        
        # Extract keywords
        keywords = self._extract_keywords(cleaned_text)
        
        # Calculate metadata
        word_count = len(cleaned_text.split())
        sentence_count = len(sent_tokenize(cleaned_text))
        
        # Try to extract title (first non-empty line)
        lines = text.split('\n')
        title = ""
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                title = line.strip()[:100]
                break
        
        return {
            "file_name": file_name,
            "title": title,
            "full_text": cleaned_text,
            "chunks": chunks,
            "summary": summary,
            "keywords": keywords,
            "metadata": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "total_pages": text.count('\f') + 1,  # Rough page count
                "chunk_count": len(chunks)
            }
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        # Remove very short lines that might be artifacts
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 3]
        return ' '.join(cleaned_lines)
    
    def _split_into_chunks(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks"""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        current_sentences = []
        
        for i, sentence in enumerate(sentences):
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += " " + sentence
                current_sentences.append(sentence)
            else:
                if current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "chunk_id": len(chunks),
                        "sentence_count": len(current_sentences)
                    })
                
                # Start new chunk with overlap
                overlap_sentences = current_sentences[-overlap//50:] if len(current_sentences) > overlap//50 else []
                current_chunk = " ".join(overlap_sentences) + " " + sentence
                current_sentences = overlap_sentences + [sentence]
        
        # Add the last chunk
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "chunk_id": len(chunks),
                "sentence_count": len(current_sentences)
            })
        
        return chunks
    
    def _generate_summary(self, text: str, max_sentences: int = 3) -> str:
        """Generate extractive summary"""
        sentences = sent_tokenize(text)
        if len(sentences) <= max_sentences:
            return text
        
        # Simple extractive summarization based on sentence position and length
        # In production, you'd use more sophisticated methods
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = 0
            # Prefer sentences from beginning and end
            if i < len(sentences) * 0.3:
                score += 2
            if i > len(sentences) * 0.7:
                score += 1
            # Prefer medium-length sentences
            if 50 < len(sentence) < 200:
                score += 1
            sentence_scores.append((score, i, sentence))
        
        # Select top sentences
        sentence_scores.sort(reverse=True)
        selected_sentences = sorted(sentence_scores[:max_sentences], key=lambda x: x[1])
        
        return " ".join([sent[2] for sent in selected_sentences])
    
    def _extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract keywords using frequency analysis"""
        words = word_tokenize(text.lower())
        # Filter out stopwords and short words
        filtered_words = [
            word for word in words 
            if word.isalpha() and len(word) > 3 and word not in self.stop_words
        ]
        
        # Count frequencies
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        return [word for word, freq in word_freq.most_common(top_k)]
    
    def _generate_embeddings(self, chunks: List[Dict[str, Any]]) -> np.ndarray:
        """Generate embeddings for document chunks"""
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)
        return embeddings
    
    def _create_faiss_index(self, file_name: str, embeddings: np.ndarray) -> None:
        """Create FAISS index for similarity search"""
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        
        self.faiss_indexes[file_name] = index
    
    def answer_question(self, question: str, document_name: Optional[str] = None, top_k: int = 3) -> Dict[str, Any]:
        """Answer questions about loaded documents"""
        if not self.documents:
            return {"error": "No documents loaded"}
        
        try:
            # If no specific document, search all documents
            if document_name and document_name in self.documents:
                documents_to_search = [document_name]
            else:
                documents_to_search = list(self.documents.keys())
            
            all_results = []
            
            for doc_name in documents_to_search:
                # Generate question embedding
                question_embedding = self.embedding_model.encode([question])
                faiss.normalize_L2(question_embedding)
                
                # Search similar chunks
                index = self.faiss_indexes[doc_name]
                scores, indices = index.search(question_embedding, top_k)
                
                # Get relevant chunks
                doc = self.documents[doc_name]
                relevant_chunks = []
                for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                    if idx < len(doc['chunks']):
                        chunk = doc['chunks'][idx]
                        relevant_chunks.append({
                            "text": chunk["text"],
                            "score": float(score),
                            "chunk_id": chunk["chunk_id"],
                            "document": doc_name
                        })
                
                all_results.extend(relevant_chunks)
            
            # Sort by score and take top results
            all_results.sort(key=lambda x: x["score"], reverse=True)
            top_results = all_results[:top_k]
            
            # Generate answer based on top results
            context = " ".join([result["text"] for result in top_results])
            answer = self._generate_answer(question, context)
            
            return {
                "success": True,
                "answer": answer,
                "relevant_chunks": top_results,
                "question": question,
                "documents_searched": documents_to_search
            }
            
        except Exception as e:
            return {"error": f"Failed to answer question: {str(e)}"}
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer based on context (simplified implementation)"""
        # This is a simplified implementation
        # In production, you'd use a language model for better answer generation
        
        question_lower = question.lower()
        context_lower = context.lower()
        
        # Simple pattern matching for common question types
        if any(word in question_lower for word in ['what is', 'define', 'definition']):
            # Look for definitions or explanations
            sentences = sent_tokenize(context)
            for sentence in sentences:
                if any(word in sentence.lower() for word in ['is', 'are', 'defined', 'refers']):
                    return sentence
        
        elif any(word in question_lower for word in ['how', 'method', 'approach']):
            # Look for methodology or process descriptions
            sentences = sent_tokenize(context)
            for sentence in sentences:
                if any(word in sentence.lower() for word in ['method', 'approach', 'technique', 'process']):
                    return sentence
        
        elif any(word in question_lower for word in ['result', 'conclusion', 'finding']):
            # Look for results or conclusions
            sentences = sent_tokenize(context)
            for sentence in sentences:
                if any(word in sentence.lower() for word in ['result', 'conclusion', 'found', 'showed']):
                    return sentence
        
        # Default: return first relevant sentence
        sentences = sent_tokenize(context)
        if sentences:
            return sentences[0]
        
        return "I couldn't find a specific answer to your question in the loaded documents."
    
    def summarize_document(self, document_name: str) -> Dict[str, Any]:
        """Get summary of a specific document"""
        if document_name not in self.documents:
            return {"error": f"Document {document_name} not found"}
        
        doc = self.documents[document_name]
        
        return {
            "success": True,
            "document_name": document_name,
            "title": doc["title"],
            "summary": doc["summary"],
            "keywords": doc["keywords"],
            "metadata": doc["metadata"]
        }
    
    def search_documents(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Search across all loaded documents"""
        if not self.documents:
            return {"error": "No documents loaded"}
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            all_results = []
            
            for doc_name in self.documents.keys():
                index = self.faiss_indexes[doc_name]
                scores, indices = index.search(query_embedding, top_k)
                
                doc = self.documents[doc_name]
                for score, idx in zip(scores[0], indices[0]):
                    if idx < len(doc['chunks']):
                        chunk = doc['chunks'][idx]
                        all_results.append({
                            "document": doc_name,
                            "title": doc["title"],
                            "text": chunk["text"][:200] + "...",
                            "score": float(score),
                            "chunk_id": chunk["chunk_id"]
                        })
            
            # Sort by relevance score
            all_results.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "success": True,
                "query": query,
                "results": all_results[:top_k],
                "total_results": len(all_results)
            }
            
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all loaded documents with metadata"""
        return [
            {
                "name": name,
                "title": doc["title"],
                "word_count": doc["metadata"]["word_count"],
                "chunk_count": doc["metadata"]["chunk_count"],
                "keywords": doc["keywords"][:5]  # Top 5 keywords
            }
            for name, doc in self.documents.items()
        ]
    
    def get_document_info(self, document_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific document"""
        if document_name not in self.documents:
            return {"error": f"Document {document_name} not found"}
        
        doc = self.documents[document_name]
        
        return {
            "success": True,
            "document_info": {
                "name": document_name,
                "title": doc["title"],
                "summary": doc["summary"],
                "keywords": doc["keywords"],
                "metadata": doc["metadata"],
                "sample_chunks": [chunk["text"][:100] + "..." for chunk in doc["chunks"][:3]]
            }
        }
