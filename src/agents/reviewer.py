"""
Reviewer/Validator Agent - Logic validation and code review
"""
from crewai import Agent
from langchain.llms import Ollama
from src.config import LLM_MODEL, OLLAMA_BASE_URL

def create_reviewer_agent(verbose: bool = False):
    """Create and return the Reviewer agent"""
    llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
    )
    
    agent = Agent(
        role="Code Reviewer",
        goal="""Validate code meets production standards:
- APPROVED: Code is correct, robust, secure, optimized, documented
- APPROVED_WITH_SUGGESTIONS: Good but minor improvements possible
- NEEDS_REVISION: Has bugs, security issues, or performance problems
Be strict. Only approve production-ready code.""",
        backstory="Senior architect who ensures only high-quality code passes review.",
        llm=llm,
        verbose=verbose
    )
    return agent
