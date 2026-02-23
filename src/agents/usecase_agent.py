"""Use Case Agent - Figures out what to test"""
from crewai import Agent
from langchain.llms import Ollama
from src.config import LLM_MODEL, OLLAMA_BASE_URL


def create_usecase_agent(verbose=False):
    llm = Ollama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    
    return Agent(
        role="Test Designer",
        goal="""Analyze code thoroughly and generate comprehensive test scenarios.

For EACH function in the code, create tests covering:

1. NORMAL CASES - Typical valid inputs
   - Common use cases the function was designed for
   - Valid inputs within expected ranges

2. EDGE CASES - Boundary conditions
   - For numbers: 0, 1, -1, very large values, very small values
   - For strings: empty string "", single char, very long string
   - For lists/arrays: empty [], single item, many items
   - For dicts: empty {}, nested structures

3. ERROR CASES - Invalid inputs that should fail gracefully
   - None/null values
   - Wrong types (string instead of int, etc.)
   - Missing required arguments
   - Out of range values

Read function signatures, type hints, and docstrings to understand expected behavior.

Output as JSON list:
[{"test_name": "...", "function": "...", "inputs": {...}, "expected": "...", "category": "normal|edge|error"}]

Just the JSON, nothing else.""",
        backstory="Senior QA engineer with 10+ years experience in test automation. Expert at finding edge cases and breaking code. Believes every function needs at least 3 test cases.",
        llm=llm,
        verbose=verbose
    )
