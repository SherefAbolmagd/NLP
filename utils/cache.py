from typing import Optional
import diskcache as dc
from datetime import timedelta
import config

class AnswerCache:
    def __init__(self):
        self.cache = dc.Cache("answer_cache")
        self.ttl = timedelta(hours=config.CACHE_EXPIRE_HOURS)
    
    def get(self, question: str) -> Optional[str]:
        return self.cache.get(question.lower().strip())
    
    def set(self, question: str, answer: str):
        if len(answer) >= config.MIN_CACHE_ANSWER_LENGTH:
            self.cache.set(question.lower().strip(), answer, expire=self.ttl.total_seconds())
    
    def clear(self):
        self.cache.clear()