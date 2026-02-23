"""
Developer Agent - Code writer and generator
"""
from crewai import Agent
from langchain.llms import Ollama
from src.config import LLM_MODEL, OLLAMA_BASE_URL

def create_developer_agent(verbose: bool = False):
    """Create and return the Developer agent for code generation"""
    
    llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
    )
    
    agent = Agent(
        role="Senior Python Developer",
        goal="""Generate production-ready Python code that is:
1. CORRECT - bug-free, no syntax/logical errors
2. ROBUST - handles edge cases, invalid inputs, exceptions
3. OPTIMIZED - efficient algorithms, minimal overhead, fast runtime
4. SECURE - no injection risks, resource leaks, or unsafe practices
5. DOCUMENTED - clear docstrings, comments, usage examples
Use standard library only. Output ONLY working code.""",
        backstory="Expert Python developer focused on writing optimized, secure, production-ready code.",
        llm=llm,
        verbose=verbose
    )
    return agent
