"""
QA Engineer/Debugger Agent - Error handling and debugging
"""
from crewai import Agent
from langchain.llms import Ollama
from src.config import LLM_MODEL, OLLAMA_BASE_URL

def create_qa_agent(verbose: bool = False):
    """Create and return the QA Engineer agent"""
    llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
    )
    
    agent = Agent(
        role="QA Engineer",
        goal="""Thoroughly debug and test code for:
1. BUGS - syntax errors, logical flaws, runtime exceptions
2. EDGE CASES - empty inputs, nulls, boundaries, overflow
3. SECURITY - injection, leaks, unsafe operations
4. PERFORMANCE - inefficient loops, redundant operations
Provide fixed code with improvements. Be concise.""",
        backstory="Expert QA engineer who catches every bug and optimizes performance.",
        llm=llm,
        verbose=verbose
    )
    return agent
