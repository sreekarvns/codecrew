# CodeCrew - Multi-Agent Programming Assistant

A production-ready multi-agent system that automates software development through three specialized AI agents: Developer, QA Engineer, and Code Reviewer.

## 🎯 How It Works

```
User Query
    ↓
Developer Agent → Generates code
    ↓
QA Agent → Tests & debugs
    ↓
Reviewer Agent → Validates & approves
    ↓
Final Code (or iterate for improvements)
```
    
## ⚡ Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Setup API Keys
```bash
copy .env.example .env
# Edit .env and add OPENAI_API_KEY from https://platform.openai.com/api-keys
```

### 3. Run
```bash
python src/main.py
```

## 📝 Usage

### Python API
```python
from src.main import CodeCrewOrchestrator

orchestrator = CodeCrewOrchestrator()
result = orchestrator.process_request(
    "Write a Python function that calculates factorial"
)

print(result['final_code'])
```

### Command Line
```bash
python src/main.py
```

## 📦 Project Structure

```
src/
├── main.py           # Main orchestrator
├── config.py         # Configuration
├── agents/           # Three agents (developer, qa, reviewer)
├── tasks/            # Task definitions
└── tools/            # Helper utilities (code executor, error analyzer)
```

## 🔧 Configuration

Edit `src/config.py`:
```python
LLM_MODEL = "gpt-4"              # AI model
TEMPERATURE = 0.3                # 0 = deterministic, 1 = creative
MAX_ITERATIONS = 3               # Max correction cycles
```

## 🤖 Which LLM? (Using Ollama)

### **🥇 Recommended: Ollama**
- **Pros**: Free, runs locally, no API keys needed, privacy-focused
- **Cost**: Free (hardware dependent)
- **Speed**: Highly variable (depends on your machine)
- **Quality**: Good for code generation and testing
- **Ideal for**: Development, learning, privacy needs
- **Setup**: https://ollama.ai/

### **Available Models**
- `llama3.2` - Balanced, good for general use
- `mistral` - Fast and efficient
- `neural-chat` - Specialized for chat/coding
- `dolphin-mixtral` - Good code quality
- `llama2` - Stable and reliable

### **Recommendation**

Use **OpenAI GPT-4** for:
- Production environments
- Best code quality
- Critical applications
- When quality > cost

Use **Ollama** for:
- Learning and experimentation
- Development/testing
- Privacy-critical applications
- Cost-free local LLM inference
- Full control over the model

## 📊 Agent Responsibilities

| Agent | Role | Output |
|-------|------|--------|
| Developer | Generates clean code | Well-documented source code |
| QA Engineer | Tests & debugs | Bug fixes and improvements |
| Reviewer | Validates logic | Approval or feedback |

## 🔄 Workflow

```
Phase 1: Code Generation
├─ Analyze requirement
├─ Generate code
└─ Add documentation

Phase 2: QA & Testing  
├─ Test code
├─ Identify bugs
└─ Create fixes

Phase 3: Review & Approval
├─ Validate logic
├─ Check quality
└─ APPROVED or NEEDS_REVISION

Phase 4: Iteration (if needed)
└─ Repeat up to 3 times
```

## 🛠️ Customization

### Change LLM Model
```python
# In src/config.py
LLM_MODEL = "gpt-3.5-turbo"  # Faster, cheaper
```

### Adjust Agent Prompts
Edit `src/agents/developer.py`, `qa_debugger.py`, or `reviewer.py`

### Add Custom Tools
Create new tool in `src/tools/` and integrate into tasks

## 📄 Output

The system generates three files:
- `result.json` - Complete structured result
- `result.md` - Formatted markdown report
- Console output - Real-time execution logs

## 🎓 Key Features

✅ Automated code generation and debugging
✅ Iterative improvement loops
✅ Configurable LLM settings
✅ Multiple output formats
✅ Comprehensive error handling
✅ Production-ready architecture

## 📚 Files

- `src/main.py` - Main orchestrator (start here)s
- `src/config.py` - Configuration settings
- `requirements.txt` - Dependencies
- `.env.example` - API keys template
- `QUICKSTART.md` - Setup guide

---

**Status**: Production Ready | **Version**: 1.0 | **Created**: January 2026

