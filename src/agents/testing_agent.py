"""Testing Agent - Runs the tests"""
from crewai import Agent
from langchain.llms import Ollama
from src.config import LLM_MODEL, OLLAMA_BASE_URL


def create_testing_agent(verbose=False):
    llm = Ollama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    
    return Agent(
        role="Tester",
        goal="""Run the code against each test case.

For each test:
1. Run it with the inputs
2. Check if output matches expected
3. Report PASS or FAIL

Format:
[PASS] test_name: got expected result
[FAIL] test_name: expected X, got Y

End with: X/Y passed, STATUS: ALL_PASSED or SOME_FAILED""",
        backstory="Tester who validates code works correctly.",
        llm=llm,
        verbose=verbose
    )
