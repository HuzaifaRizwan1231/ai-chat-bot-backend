import os
from dotenv import load_dotenv

# initialize
load_dotenv()

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
AES_SECRET_KEY = (os.getenv("AES_SECRET_KEY"))
AES_IV = (os.getenv("AES_IV"))

# Allowed Models
ALLOWED_OPENAI_MODELS = ["gpt-4o", "ft:gpt-4o-mini-2024-07-18:mergestack::AqhhvrOU"]
ALLOWED_GEMINI_MODELS = ["gemini-1.5-flash"]
ALLOWED_CLAUDE_MODELS = ["claude-3-5-sonnet-20241022"]

# OPEN AI model configs


# GEMINI model configs
MAX_OUTPUT_TOKENS = 500
TEMPERATURE = 0.7

#CLAUDE model configs
MAX_TOKEN = 1024