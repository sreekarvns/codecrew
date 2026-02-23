"""Main orchestrator - runs the code generation pipeline"""
import json
import re
from datetime import datetime
from crewai import Crew, Process

from src.agents.developer import create_developer_agent
from src.agents.qa_debugger import create_qa_agent
from src.agents.reviewer import create_reviewer_agent
from src.agents.usecase_agent import create_usecase_agent
from src.agents.testing_agent import create_testing_agent
from src.tasks.code_generation import create_code_generation_task
from src.tasks.debugging import create_debugging_task
from src.tasks.validation import create_validation_task
from src.tasks.usecase_generation import create_usecase_task
from src.tasks.testing import create_testing_task
from src.config import MAX_ITERATIONS


class CodeCrewOrchestrator:
    """Runs the multi-agent code generation workflow"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.max_iterations = MAX_ITERATIONS
    
    def log(self, msg):
        if self.verbose:
            print(msg)
    
    def run_crew(self, agent, task):
        """Run a single agent with a task"""
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=self.verbose
        )
        return str(crew.kickoff())
    
    def extract_code(self, text):
        """Pull code out of markdown blocks"""
        match = re.search(r'```python\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
    
    def process_request(self, query):
        """Standard flow: generate -> debug -> validate"""
        self.log(f"\n{'='*50}\nProcessing: {query}\n{'='*50}")
        
        # Step 1: Generate code
        self.log("\n[1] Generating code...")
        dev = create_developer_agent(verbose=self.verbose)
        task = create_code_generation_task(query)
        code = self.extract_code(self.run_crew(dev, task))
        
        # Step 2: Debug/QA
        self.log("\n[2] Running QA...")
        qa = create_qa_agent(verbose=self.verbose)
        task = create_debugging_task(code, query)
        feedback = self.run_crew(qa, task)
        
        # Step 3: Review
        self.log("\n[3] Reviewing...")
        reviewer = create_reviewer_agent(verbose=self.verbose)
        task = create_validation_task(code, query, feedback)
        review = self.run_crew(reviewer, task)
        
        self.log("\n[DONE]")
        return {
            "query": query,
            "code": code,
            "feedback": feedback,
            "review": review,
            "status": "completed"
        }
    
    def process_request_verified(self, query):
        """Verified flow: generate -> use case agent -> testing agent"""
        self.log(f"\n{'='*50}\nVerified Processing: {query}\n{'='*50}")
        
        # Step 1: Generate code
        self.log("\n[1] Generating code...")
        dev = create_developer_agent(verbose=self.verbose)
        task = create_code_generation_task(query)
        code = self.extract_code(self.run_crew(dev, task))
        
        for i in range(self.max_iterations):
            self.log(f"\n--- Iteration {i+1} ---")
            
            # Step 2: Use Case Agent generates test scenarios
            self.log("\n[2] Generating test scenarios...")
            usecase = create_usecase_agent(verbose=self.verbose)
            task = create_usecase_task(code, query)
            scenarios = self.run_crew(usecase, task)
            
            # Step 3: Testing Agent runs the tests
            self.log("\n[3] Running tests...")
            tester = create_testing_agent(verbose=self.verbose)
            task = create_testing_task(code, scenarios)
            results = self.run_crew(tester, task)
            
            # Check results
            if "ALL_PASSED" in results.upper():
                self.log("\n[OK] All tests passed!")
                return {
                    "query": query,
                    "code": code,
                    "scenarios": scenarios,
                    "results": results,
                    "status": "VERIFIED_PASSED"
                }
            
            if i < self.max_iterations - 1:
                self.log("\n[WARN] Tests failed, regenerating...")
                task = create_code_generation_task(
                    f"{query}\n\nFix these issues:\n{results}"
                )
                code = self.extract_code(self.run_crew(dev, task))
        
        self.log("\n[DONE] Max iterations reached")
        return {
            "query": query,
            "code": code,
            "scenarios": scenarios,
            "results": results,
            "status": "TESTS_FAILED"
        }
    
    def process_request_fast(self, query):
        """Fast mode: just generate, no QA"""
        self.log(f"\n[FAST] Generating: {query}")
        
        dev = create_developer_agent(verbose=self.verbose)
        task = create_code_generation_task(query)
        code = self.extract_code(self.run_crew(dev, task))
        
        return {"query": query, "code": code, "status": "generated"}