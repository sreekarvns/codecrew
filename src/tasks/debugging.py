"""
Debugging Task - QA Engineer agent task
"""
from crewai import Task

from src.agents.qa_debugger import create_qa_agent


def create_debugging_task(code: str, user_query: str):
    """
    Create a debugging task for the QA Engineer agent
    
    Args:
        code: The code to debug and analyze
        user_query: The original user query for context
    
    Returns:
        Task: A CrewAI Task for debugging
    """
    qa_agent = create_qa_agent()
    
    task_description = f"""Debug this code by mentally executing it line by line.

REQUIREMENT: {user_query}

CODE:
```python
{code}
```

CRITICAL CHECKS (trace through the code mentally):
1. TYPE MISMATCHES: Is .lower()/.upper() called on non-strings? Is int used where string expected?
2. ENUM BUGS: Does Enum(user_input) work? Are enum values the right type for how they're used?
3. LOGIC ERRORS: Does validation reject valid inputs? (e.g., rejecting negative numbers in a calculator)
4. RUNTIME ERRORS: Will this crash? Trace through with sample inputs.
5. UNREACHABLE CODE: Is there dead code or redundant checks?

FIND AND FIX:
- Syntax errors
- Type errors (calling string methods on ints, etc.)
- Logic that doesn't make sense
- Missing error handling

OUTPUT:
1. List each bug found with line number
2. Provide the COMPLETE FIXED code
"""
    
    task = Task(
        description=task_description,
        expected_output="List of issues with severity, and fixed optimized code",
        agent=qa_agent,
    )
    
    return task
