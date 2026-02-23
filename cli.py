"""
CodeCrew CLI - Simple command-line interface for code generation
Run: python cli.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import CodeCrewOrchestrator
import json

def main():
    print("=" * 60)
    print("🤖 CodeCrew - Multi-Agent Code Generation")
    print("=" * 60)
    
    # Check for modes
    fast_mode = "--fast" in sys.argv or "-f" in sys.argv
    verified_mode = "--verified" in sys.argv or "-v" in sys.argv
    
    if fast_mode:
        print("[FAST MODE] Developer only, no verification")
    elif verified_mode:
        print("[VERIFIED MODE] With automated testing")
    else:
        print("[STANDARD MODE] Developer → QA → Reviewer")
    
    # Get user input
    query = input("\nDescribe what code you need:\n> ")
    
    if not query.strip():
        query = "Write a Python function that calculates the factorial of a number with proper error handling"
        print(f"Using default: {query}")
    
    mode_label = "[FAST]" if fast_mode else "[VERIFIED]" if verified_mode else ""
    print("\n" + "=" * 60)
    print(f"Processing... {mode_label}")
    print("=" * 60 + "\n")
    
    # Create orchestrator and process
    orchestrator = CodeCrewOrchestrator(verbose=not fast_mode)
    orchestrator.max_iterations = 2
    
    try:
        if fast_mode:
            result = orchestrator.process_request_fast(query)
        elif verified_mode:
            result = orchestrator.process_request_verified(query)
        else:
            result = orchestrator.process_request(query)
        
        print("\n" + "=" * 60)
        print("✅ RESULT")
        print("=" * 60)
        print(f"\nStatus: {result.get('status', 'Unknown')}")
        
        # Show test results if in verified mode
        if verified_mode and result.get('results'):
            print("\n--- Test Results ---\n")
            print(result.get('results', 'No test results'))
        
        print("\n--- Generated Code ---\n")
        print(result.get('code', 'No code generated'))
        
        # Save result
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\n[Result saved to result.json]")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
