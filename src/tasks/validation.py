"""
Validation Task - Reviewer agent task
"""
from crewai import Task

from src.agents.reviewer import create_reviewer_agent


def create_validation_task(code: str, user_query: str, previous_feedback: str = ""):
    """
    Create a validation task for the Reviewer agent
    
    Args:
        code: The code to validate
        user_query: The original user query for context
        previous_feedback: Feedback from previous iterations
    
    Returns:
        Task: A CrewAI Task for validation
    """
    reviewer = create_reviewer_agent()
    
    feedback_section = f"PREVIOUS FEEDBACK:\n{previous_feedback}" if previous_feedback else ""
    
    task_description = f"""Final code review - TRACE THROUGH THE CODE MENTALLY.

REQUIREMENT: {user_query}

CODE:
```python
{code}
```

{feedback_section}

BEFORE APPROVING, MENTALLY RUN THE CODE:
1. Pick sample inputs and trace through each line
2. Check: Does Enum usage match? (string vs int values)
3. Check: Are all method calls valid? (.lower() on strings only)
4. Check: Does the validation logic make sense?
5. Check: Will user input parsing actually work?

REJECT IF:
- Code will crash with TypeError/AttributeError
- Logic is wrong (e.g., calculator rejects negative numbers)
- Enum values don't match how they're used
- Method called on wrong type

DECISION (pick one):
- APPROVED: Code actually works when traced through
- NEEDS_REVISION: Found bugs that will cause runtime errors

OUTPUT FORMAT:
Decision: [APPROVED/NEEDS_REVISION]
Issues: [list any problems]
"""
    
    task = Task(
        description=task_description,
        expected_output="Decision (APPROVED/NEEDS_REVISION) with brief justification",
        agent=reviewer,
    )
    
    return task
