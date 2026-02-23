"""
CodeCrew Configuration - Minimal, Clean Settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
# Using Ollama
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")  # llama3.2 is faster, llama3.1 is more accurate
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
TEMPERATURE = 0.3  # Deterministic code generation
MAX_TOKENS = 2048

# Workflow Settings
MAX_ITERATIONS = 1  # 1 for speed, 2-3 for quality
VALIDATION_THRESHOLD = 0.85

# Agent Settings
DEVELOPER_AGENT_CONFIG = {
    "name": "Developer",
    "role": "Senior Software Engineer",
    "goal": "Write clean, efficient, production-ready code",
    "backstory": "Expert developer with years of best practices experience."
}

QA_AGENT_CONFIG = {
    "name": "QA Engineer",
    "role": "QA Engineer and Debugger",
    "goal": "Identify bugs and ensure code quality",
    "backstory": "Meticulous QA engineer who catches edge cases and ensures robustness."
}

REVIEWER_AGENT_CONFIG = {
    "name": "Reviewer",
    "role": "Senior Code Reviewer",
    "goal": "Validate code logic and quality",
    "backstory": "Senior reviewer with deep software architecture knowledge."
}
