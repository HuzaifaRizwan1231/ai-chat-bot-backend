import os
from dotenv import load_dotenv

# initialize
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Allowed Models
ALLOWED_OPENAI_MODELS = ["gpt-4o"]
ALLOWED_GEMINI_MODELS = ["gemini-1.5-flash"]
ALLOWED_CLAUDE_MODELS = ["claude-3-5-sonnet-20241022"]

# OPEN AI model configs


# GEMINI model configs
MAX_OUTPUT_TOKENS = 500
TEMPERATURE = 0.7

#CLAUDE model configs
MAX_TOKEN = 1024