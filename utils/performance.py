import time
from functools import wraps
import pandas as pd

def monitor_performance(func):
    """Decorator to track execution metrics"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start_time
        
        # Estimate tokens (adapt based on your LLM)
        input_tokens = len(str(args) + str(kwargs)) // 4  # Approximation
        output_tokens = len(str(result)) // 4
        
        metrics = {
            'function': func.__name__,
            'time_sec': exec_time,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'tokens_per_sec': (input_tokens + output_tokens) / exec_time
        }
        
        # Store or print metrics
        pd.DataFrame([metrics]).to_csv('performance_metrics.csv', mode='a', header=False)
        
        return result
    return wrapper