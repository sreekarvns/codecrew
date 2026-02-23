"""
Code Generation Task - Developer agent task
"""
from crewai import Task

from src.agents.developer import create_developer_agent


def create_code_generation_task(user_query: str, context: str = ""):
    """
    Create a code generation task for the Developer agent
    
    Args:
        user_query: The user's programming requirement
        context: Optional context or previous attempts
    
    Returns:
        Task: A CrewAI Task for code generation
    """
    developer = create_developer_agent()
    
    context_section = f"CONTEXT FROM PREVIOUS ATTEMPTS:\n{context}" if context else ""
    
    task_description = f"""Generate production-ready Python code.

REQUIREMENT:
{user_query}

{context_section}

BEFORE WRITING CODE, VERIFY:
1. Enum values match how they're used (if .lower() is called, value must be string)
2. User input parsing matches expected types (can't pass string to Enum expecting int)
3. All method calls exist on the types used (.lower() only works on strings)
4. Validation logic makes sense (calculators need negative numbers!)

MUST INCLUDE:
1. Complete working code - mentally trace through it to verify it runs
2. Proper error handling (try/except for risky operations)
3. Input validation that makes sense for the use case
4. Docstrings for all functions/classes
5. Working usage example in if __name__ == "__main__" block

CONSTRAINTS:
- Use standard library ONLY
- Test your code mentally: trace through with sample inputs
- Verify all method calls are valid for their types

OUTPUT: Only the Python code, nothing else.
"""
    
    task = Task(
        description=task_description,
        expected_output="Production-ready Python code with error handling, validation, docstrings, and usage example",
        agent=developer,
    )
    
    return task
