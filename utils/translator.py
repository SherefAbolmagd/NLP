from typing import List, Dict
from llama_cpp import Llama
import re
import time

class PublicationTranslator:
    def __init__(self, llm_path: str):
        self.llm = Llama(
            model_path=llm_path,
            n_ctx=4096,
            n_threads=4
        )
        self.token_counts = []
        self.times = []
    
    def translate(self, text: str, target_lang: str = "English") -> Dict:
        """
        Translate text while preserving formatting
        Returns: {
            'translated_text': str,
            'source_tokens': int,
            'target_tokens': int,
            'time_sec': float,
            'tokens_per_sec': float
        }
        """
        start_time = time.time()
        
        # Detect language if not specified
        lang_prompt = f"Detect the language of this text:\n{text[:500]}\nLanguage:"
        lang_response = self.llm.create_completion(lang_prompt, max_tokens=10)
        source_lang = lang_response['choices'][0]['text'].strip()
        
        # Format-preserving translation
        prompt = f"""Translate this {source_lang} text to {target_lang} while preserving:
- All formatting (paragraphs, lists, tables)
- Technical terminology
- Numerical data

Text:
{text}

Translation ({target_lang}):"""
        
        response = self.llm.create_completion(
            prompt,
            temperature=0.3,
            max_tokens=len(text.split()) * 2  # Allow for expansion
        )
        
        translated_text = response['choices'][0]['text']
        
        # Performance metrics
        exec_time = time.time() - start_time
        source_tokens = len(self.llm.tokenize(text.encode()))
        target_tokens = len(self.llm.tokenize(translated_text.encode()))
        
        self.token_counts.append((source_tokens, target_tokens))
        self.times.append(exec_time)
        
        return {
            'translated_text': translated_text,
            'source_lang': source_lang,
            'source_tokens': source_tokens,
            'target_tokens': target_tokens,
            'time_sec': exec_time,
            'tokens_per_sec': target_tokens / exec_time
        }

    def batch_translate(self, chunks: List[Dict], target_lang: str) -> List[Dict]:
        """Translate multiple chunks with progress tracking"""
        results = []
        for chunk in chunks:
            result = self.translate(chunk['text'], target_lang)
            results.append({
                **chunk,
                'translated_text': result['translated_text'],
                'translation_metrics': {
                    k: v for k, v in result.items() 
                    if k != 'translated_text'
                }
            })
        return results