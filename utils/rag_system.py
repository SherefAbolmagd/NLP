from typing import List, Dict, Optional

from llama_cpp import Llama

import config
from utils.cache import AnswerCache
from utils.query_analyzer import QueryAnalyzer
from utils.vector_db import VectorDatabase

class EnhancedRAGSystem:
    def __init__(self, vector_db: VectorDatabase, llm_path: str):
        self.vector_db = vector_db
        self.llm = Llama(
            model_path=llm_path,
            n_ctx=4096,  # Larger context window
            n_threads=6   # More threads for better performance
        )
        self.query_analyzer = QueryAnalyzer()
        self.cache = AnswerCache()

    def ask(self, question: str, use_cache: bool = True) -> str:
        """Simplified RAG system"""
        
        # Cache check
        if use_cache:
            cached = self.cache.get(question)
            if cached:
                return f"[CACHED] {cached}"
        
        # Retrieve relevant chunks
        retrieved_chunks = self.vector_db.query(question, n_results=3)
        
        # Generate answer
        answer = self._generate_answer(question, retrieved_chunks)
        
        # Cache if answer is substantial
        if len(answer) >= config.MIN_CACHE_ANSWER_LENGTH:
            self.cache.set(question, answer)
            
        return answer
    
    def _generate_query_variations(self, question: str, query_type: str) -> List[str]:
        """Generate multiple query formulations"""
        variations = [question]
        
        if query_type == "fact":
            variations.append(f"What are the key facts about {question}")
        elif query_type == "comparison":
            variations.append(f"Compare and contrast {question}")
        
        return variations
    
    def _deduplicate_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Remove duplicate chunks based on their text content"""
        seen_texts = set()
        unique_chunks = []
        
        for chunk in chunks:
            if chunk['text'] not in seen_texts:
                seen_texts.add(chunk['text'])
                unique_chunks.append(chunk)
                
        return unique_chunks
    
    def _build_prompt(self, question: str, context: str) -> List[Dict]:
        """Build the LLM prompt with context"""
        return [
            {
                "role": "system",
                "content": "You are a research assistant analyzing scientific papers. "
                           "Answer questions accurately using the provided context. "
                           "If the answer isn't in the context, say 'I don't know'."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
            }
        ]
    
    def _generate_answer(self, question: str, chunks: List[Dict]) -> str:
        """Generate answer using retrieved chunks"""
        context = "\n\n".join([c['text'] for c in chunks])
        prompt = self._build_prompt(question, context)
        
        response = self.llm.create_chat_completion(
            messages=prompt,
            temperature=0.7,  # Balanced creativity/factuality
            max_tokens=1024
        )
        
        return response['choices'][0]['message']['content']