# Processing parameters
CHUNK_SIZE = 512
CHUNK_OVERLAP = 100
MAX_MEMORY_CHUNKS = 1000  # Keep only N chunks in memory

# Model paths
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
LLM_MODEL = "/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# Performance settings
LLM_THREADS = 6
LLM_CONTEXT_SIZE = 4096

# Caching
CACHE_EXPIRE_HOURS = 24
MIN_CACHE_ANSWER_LENGTH = 30

CONVERSATION_HISTORY_LENGTH = 5  # Number of exchanges to remember