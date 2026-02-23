"""Use Case Task - Generate test scenarios"""
from crewai import Task
from src.agents.usecase_agent import create_usecase_agent


def create_usecase_task(code, user_query):
    agent = create_usecase_agent()
    
    desc = f"""Analyze this code and generate comprehensive test scenarios.

## Original Requirement:
{user_query}

## Code to Test:
```python
{code}
```

## Instructions:
1. Identify ALL functions in the code
2. Read type hints and docstrings to understand expected behavior
3. For EACH function, create tests in these categories:

### NORMAL (typical valid inputs):
- Common use cases
- Expected input types and ranges

### EDGE (boundary conditions):
- Numbers: 0, 1, -1, large values (1000000), negative
- Strings: "", "a", "a"*1000
- Collections: [], [1], list with many items
- Booleans: True, False

### ERROR (should handle gracefully):
- None values
- Wrong types (pass string when int expected)
- Empty when not allowed
- Out of bounds

## Output Format (JSON only):
[
  {{"test_name": "test_funcname_normal_typical", "function": "funcname", "inputs": {{"param1": value}}, "expected": result, "category": "normal"}},
  {{"test_name": "test_funcname_edge_zero", "function": "funcname", "inputs": {{"param1": 0}}, "expected": result, "category": "edge"}},
  {{"test_name": "test_funcname_error_none", "function": "funcname", "inputs": {{"param1": null}}, "expected": "raises TypeError", "category": "error"}}
]

Generate 5-8 test scenarios total. Cover each function. Just output the JSON array, no explanation.
"""
    
    return Task(
        description=desc,
        expected_output="JSON array of test scenarios with test_name, function, inputs, expected, and category fields",
        agent=agent
    )
