"""
Streamlit Web Interface for CodeCrew Multi-Agent System
Provides a user-friendly dashboard to interact with the code generation pipeline
"""

import streamlit as st
import sys
import os
from datetime import datetime
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import CodeCrewOrchestrator

# Page configuration
st.set_page_config(
    page_title="CodeCrew - Multi-Agent Code Generation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding: 10px 20px;
    }
    .phase-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .phase-generation {
        background-color: #e3f2fd;
        border-left: 5px solid #1976d2;
    }
    .phase-debugging {
        background-color: #fff3e0;
        border-left: 5px solid #f57c00;
    }
    .phase-validation {
        background-color: #e8f5e9;
        border-left: 5px solid #388e3c;
    }
    .code-block {
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = CodeCrewOrchestrator(verbose=False)

if "result" not in st.session_state:
    st.session_state.result = None

if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("# 🤖 CodeCrew - Multi-Agent Code Generation System")
st.markdown("""
Automated code generation, debugging, and validation through AI agent collaboration.
Powered by CrewAI and Ollama (llama3.2).
""")

# Sidebar configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    max_iterations = st.slider(
        "Max Iterations",
        min_value=1,
        max_value=5,
        value=3,
        help="Maximum number of refinement iterations"
    )
    st.session_state.orchestrator.max_iterations = max_iterations
    
    verbose_mode = st.checkbox(
        "Verbose Mode",
        value=False,
        help="Show detailed agent logs"
    )
    st.session_state.orchestrator.verbose = verbose_mode
    
    st.markdown("---")
    st.markdown("## 📋 About This System")
    st.markdown("""
    **Three AI Agents Work Together:**
    
    1. 👨‍💻 **Developer Agent**
       - Generates clean, efficient code
       - Follows best practices
       - Adds documentation
    
    2. 🔍 **QA Agent**
       - Reviews for bugs
       - Checks edge cases
       - Suggests improvements
    
    3. ✅ **Reviewer Agent**
       - Validates against requirements
       - Ensures code quality
       - Approves or requests revisions
    """)

# Main content area
st.markdown("## 📝 Code Generation Request")

# User input
user_query = st.text_area(
    "Describe what code you need:",
    value="Write a Python function that calculates the factorial of a number with proper error handling",
    height=100,
    placeholder="Enter your programming requirement here..."
)

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    submit_button = st.button("🚀 Generate Code", use_container_width=True)

with col2:
    if st.session_state.result:
        st.download_button(
            label="📥 Download JSON",
            data=json.dumps(st.session_state.result, indent=2),
            file_name=f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

with col3:
    if st.session_state.result:
        # Generate markdown export
        result = st.session_state.result
        markdown_content = f"""# Code Generation Result

## Query
{result['user_query']}

## Status
{result['final_status']}

## Final Code
```python
{result['final_code']}
```

## Metadata
- Total Iterations: {result['metadata']['total_iterations']}
- Duration: {result['metadata']['duration']}
- Start Time: {result['metadata']['start_time']}
"""
        st.download_button(
            label="📋 Download Markdown",
            data=markdown_content,
            file_name=f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# Processing
if submit_button:
    st.session_state.processing = True

if st.session_state.processing and user_query:
    # Create progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("## 🔄 Processing Workflow")
        
        # Create placeholders for progress display
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        phase_placeholder = st.empty()
        
        # Overall progress bar
        max_steps = (1 + st.session_state.orchestrator.max_iterations * 3)  # 1 generation + (iterations * 3 phases)
        current_step = 0
        
        class StreamlitProgressTracker:
            """Custom tracker to update Streamlit progress"""
            def __init__(self, max_steps, progress_ph, status_ph, phase_ph):
                self.max_steps = max_steps
                self.current_step = 0
                self.progress_ph = progress_ph
                self.status_ph = status_ph
                self.phase_ph = phase_ph
                self.phase_icons = {
                    'generation': '👨‍💻',
                    'debugging': '🔍',
                    'validation': '✅',
                    'regeneration': '♻️'
                }
            
            def update(self, phase, iteration=None, message=""):
                self.current_step += 1
                progress = min(self.current_step / self.max_steps, 0.99)
                
                icon = self.phase_icons.get(phase, '⚙️')
                phase_display = {
                    'generation': 'Code Generation',
                    'debugging': 'QA & Debugging',
                    'validation': 'Review & Validation',
                    'regeneration': 'Code Regeneration'
                }.get(phase, phase.upper())
                
                # Update progress bar
                with self.progress_ph.container():
                    st.progress(progress)
                    st.caption(f"Progress: {int(progress * 100)}%")
                
                # Update status
                status_text = f"{icon} **Current Phase:** {phase_display}"
                if iteration:
                    status_text += f" (Iteration {iteration})"
                
                with self.status_ph.container():
                    st.info(status_text)
                
                # Update phase details
                if message:
                    with self.phase_ph.container():
                        st.write(f"📝 {message}")
        
        tracker = StreamlitProgressTracker(max_steps, progress_placeholder, status_placeholder, phase_placeholder)
        
        # Monkey-patch the orchestrator to report progress
        original_log = st.session_state.orchestrator._log
        iteration_counter = [0]
        
        def progress_log(message: str):
            original_log(message)
            
            # Track phases
            if "PHASE 1: CODE GENERATION" in message:
                tracker.update('generation', message="Generating initial code...")
            elif "PHASE 2: QA & DEBUGGING" in message:
                tracker.update('debugging', iteration=iteration_counter[0], message="Analyzing code for bugs and issues...")
            elif "PHASE 3: REVIEW & VALIDATION" in message:
                tracker.update('validation', iteration=iteration_counter[0], message="Validating against requirements...")
            elif "ITERATION" in message and "==" in message:
                iteration_num = message.split("ITERATION")[1].split("=")[0].strip()
                if iteration_num.isdigit():
                    iteration_counter[0] = int(iteration_num)
        
        st.session_state.orchestrator._log = progress_log
        
        try:
            # Run orchestrator
            st.session_state.result = st.session_state.orchestrator.process_request(user_query)
            
            # Final progress update
            tracker.current_step = tracker.max_steps
            with progress_placeholder.container():
                st.progress(1.0)
                st.caption("Progress: 100%")
            
            with status_placeholder.container():
                st.success("✅ **Pipeline Complete!**")
            
            # Display results
            st.markdown("## ✅ Results")
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "💻 Generated Code", "🔍 Details", "📈 Timeline"])
            
            with tab1:
                result = st.session_state.result
                
                # Status badge
                status_color = "green" if result['final_status'] == "APPROVED" else "orange"
                st.markdown(f"""
                ### Status: :{status_color}[{result['final_status']}]
                
                **Query:** {result['user_query']}
                
                **Iterations:** {result['metadata']['total_iterations']}
                
                **Duration:** {result['metadata']['duration']}
                
                **Start Time:** {result['metadata']['start_time']}
                """)
            
            with tab2:
                result = st.session_state.result
                st.markdown("### Generated Code")
                st.code(result['final_code'], language="python")
            
            with tab3:
                result = st.session_state.result
                st.markdown("### Detailed Iteration Log")
                
                for idx, iteration in enumerate(result['iterations']):
                    phase = iteration.get('phase', 'unknown')
                    phase_title = {
                        'generation': '👨‍💻 Code Generation',
                        'debugging': '🔍 QA Debugging',
                        'validation': '✅ Validation',
                        'regeneration': '♻️ Regeneration'
                    }.get(phase, phase.upper())
                    
                    with st.expander(f"{phase_title} - Iteration {iteration.get('iteration', idx + 1)}", expanded=False):
                        st.text(iteration['output'][:500] + "..." if len(iteration['output']) > 500 else iteration['output'])
            
            with tab4:
                result = st.session_state.result
                st.markdown("### Process Timeline")
                
                timeline_data = {
                    'Start': result['metadata']['start_time'],
                    'End': result['metadata']['end_time'],
                    'Duration': result['metadata']['duration'],
                    'Total Iterations': result['metadata']['total_iterations']
                }
                
                for key, value in timeline_data.items():
                    st.metric(key, value)
            
            st.session_state.processing = False
            
        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            st.session_state.processing = False

# Display execution history if in verbose mode
if st.session_state.orchestrator.execution_history and verbose_mode:
    with st.expander("📜 Execution History", expanded=False):
        history_text = "\n".join(st.session_state.orchestrator.execution_history)
        st.code(history_text, language="text")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🤖 CodeCrew Multi-Agent System | Powered by CrewAI & Ollama</p>
    <p style='font-size: 12px; color: #666;'>
        Three AI agents collaborate to generate, review, and validate code
    </p>
</div>
""", unsafe_allow_html=True)
