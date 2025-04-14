import time
from typing import List, Dict
import hashlib
import diskcache as dc

from config import CONVERSATION_HISTORY_LENGTH

class ConversationMemory:
    def __init__(self, user_id: str = "default"):
        self.cache = dc.Cache(f"conversation_{hashlib.md5(user_id.encode()).hexdigest()}")
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        return list(self.cache.get("history", []))
    
    def add_exchange(self, question: str, answer: str):
        self.history.append({
            "question": question,
            "answer": answer,
            "timestamp": time.time()
        })
        # Keep only recent history
        self.history = self.history[-CONVERSATION_HISTORY_LENGTH:]
        self.cache.set("history", self.history)
    
    def get_context(self) -> str:
        return "\n".join(
            f"Q: {item['question']}\nA: {item['answer']}" 
            for item in self.history
        )
    
    def clear(self):
        self.history = []
        self.cache.clear()