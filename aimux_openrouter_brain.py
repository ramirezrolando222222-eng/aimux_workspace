import os
from dotenv import load

# Load environment variables from .env if present
load_dotenv = lambda: __import__('dotenv').load_dotenv()
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
# (Rest of your OpenRouter logic here...)
