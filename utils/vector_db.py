from typing import List, Dict, Optional
import chromadb
from chromadb.utils import embedding_functions

class VectorDatabase:
    def __init__(self, persist_dir: str = "chroma_db"):
        self.client = chromadb.Client()
        
        # Using Nomic embedding model
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="nomic-ai/nomic-embed-text-v1",
            trust_remote_code=True
        )
        
        self.collection = self.client.get_or_create_collection(
            name="dr_x_publications",
            embedding_function=self.embedding_fn
        )
    
    def add_documents(self, chunks: List[Dict]):
        """Add documents with robust metadata handling"""
        if not chunks:
            raise ValueError("No chunks provided")
        
        # Prepare data with defaults
        ids = []
        documents = []
        metadatas = []
        
        for chunk in chunks:
            ids.append(f"{chunk['source']}_{chunk['chunk_num']}")
            documents.append(chunk['text'])
            metadatas.append({
                'source': chunk.get('source', 'unknown'),
                'page': chunk.get('page', 1),  # Default to page 1
                'chunk_num': chunk.get('chunk_num', 0),
                'is_table': chunk.get('is_table', False),
                'token_count': chunk.get('token_count', 0)
            })
        
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            print("Sample problematic metadata:", metadatas[0] if metadatas else "None")
            raise
    
    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """Query the vector database"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return [{
            'text': doc,
            'metadata': meta,
            'distance': dist
        } for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )]