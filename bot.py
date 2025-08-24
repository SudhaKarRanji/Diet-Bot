"""
Chatbot implementation using Llama 2 via Ollama with RAG capabilities
"""
from typing import List, Dict
import requests
import json
import chromadb
from utils import create_embeddings_database, process_documents, create_nutrition_collection

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

class DietBot:
    def __init__(self):
        """Initialize the Diet Bot with ChromaDB and Ollama"""
        self.db = create_embeddings_database()
        self.collection = None
        self.base_url = "http://localhost:11434/api/generate"
        self.context_window = 4096
        
    def initialize_knowledge_base(self, documents: List[str], metadatas: List[Dict] = None):
        """Initialize the knowledge base with nutrition documents"""
        chunks = process_documents(documents)
        self.collection = create_nutrition_collection(self.db, chunks, metadatas)
    
    def query_knowledge_base(self, query: str, n_results: int = 3) -> List[str]:
        """Query the knowledge base for relevant context"""
        if not self.collection:
            raise ValueError("Knowledge base not initialized. Call initialize_knowledge_base first.")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results["documents"][0]
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate a response using Llama 2 via Ollama"""
        # Prepare the prompt with context
        prompt = self._prepare_prompt(query, context)
        
        # Generate response using Ollama
        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_gpu": 1,
                        "num_thread": 4
                    }
                }
            )
            
            if response.status_code == 200:
                return json.loads(response.text)["response"]
            else:
                error_msg = f"Error generating response: {response.text}"
                print(f"Server error: {error_msg}")
                return "I apologize, but I encountered an error processing your request. Please try again."
        except Exception as e:
            print(f"Error during API call: {str(e)}")
            return "I apologize, but I'm having trouble connecting to the language model. Please ensure Ollama is running and try again."
    
    def chat(self, query: str) -> str:
        """Main chat function that combines retrieval and generation"""
        # Retrieve relevant context
        context = self.query_knowledge_base(query)
        
        # Generate response
        response = self.generate_response(query, context)
        
        return response
    
    def _prepare_prompt(self, query: str, context: List[str]) -> str:
        """Prepare the prompt with context for the language model"""
        context_str = "\n".join(context)
        
        prompt = f"""As a knowledgeable nutritionist, use the following information to answer the question:

Context:
{context_str}

Question:
{query}

Answer:"""
        
        return prompt
