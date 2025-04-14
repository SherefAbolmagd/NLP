from typing import List, Dict
from llama_cpp import Llama
from rouge_score import rouge_scorer
import time
import numpy as np

class PublicationSummarizer:
    def __init__(self, llm_path: str):
        self.llm = Llama(
            model_path=llm_path,
            n_ctx=4096,
            n_threads=4
        )
        self.scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
        self.performance_metrics = []
    
    def summarize(self, text: str, strategy: str = "key_points") -> Dict:
        """
        Summarize text using different strategies
        Returns: {
            'summary': str,
            'rouge_scores': dict,
            'metrics': {
                'time_sec': float,
                'tokens_per_sec': float,
                'compression_ratio': float
            }
        }
        """
        start_time = time.time()
        
        strategies = {
            "key_points": "Extract the 5 most important bullet points",
            "technical": "Write a technical abstract (1 paragraph)",
            "layman": "Explain to a non-expert in 3 sentences"
        }
        
        prompt = f"""Original Text:
{text}

Instruction: {strategies[strategy]}
Summary:"""
        
        response = self.llm.create_completion(
            prompt,
            temperature=0.2,
            max_tokens=500
        )
        
        summary = response['choices'][0]['text']
        exec_time = time.time() - start_time
        
        # Calculate ROUGE scores against first 500 chars as reference
        reference = text[:500]
        scores = self.scorer.score(reference, summary[:500])
        
        # Performance metrics
        tokens = len(self.llm.tokenize(summary.encode()))
        metrics = {
            'time_sec': exec_time,
            'tokens_per_sec': tokens / exec_time,
            'compression_ratio': len(summary) / len(text)
        }
        
        self.performance_metrics.append(metrics)
        
        return {
            'summary': summary,
            'rouge_scores': scores,
            'metrics': metrics
        }
    
    def evaluate_summary_quality(self):
        """Aggregate quality metrics across all summaries"""
        if not self.performance_metrics:
            return None
            
        avg_rouge1 = np.mean([m['rouge1'].fmeasure for m in self.performance_metrics])
        avg_rouge2 = np.mean([m['rouge2'].fmeasure for m in self.performance_metrics])
        avg_speed = np.mean([m['tokens_per_sec'] for m in self.performance_metrics])
        
        return {
            'avg_rouge1': avg_rouge1,
            'avg_rouge2': avg_rouge2,
            'avg_speed_tokens_per_sec': avg_speed
        }