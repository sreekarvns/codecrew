"""Testing Task - Run the tests"""
from crewai import Task
from src.agents.testing_agent import create_testing_agent


def create_testing_task(code, test_scenarios):
    agent = create_testing_agent()
    
    desc = f"""Run these tests against the code.

Code:
```python
{code}
```

Tests:
{test_scenarios}

For each test, run the function with inputs and check the result.

Output like this:
[PASS] test_name: expected 5, got 5
[FAIL] test_name: expected 10, got 8

End with:
SUMMARY: X/Y passed
STATUS: ALL_PASSED or SOME_FAILED
"""
    
    return Task(
        description=desc,
        expected_output="Test results with PASS/FAIL and final STATUS",
        agent=agent
    )
