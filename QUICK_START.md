# Quick Start Guide - Smart Grocery List with Gemini API

## 🚀 For Team Members

### Prerequisites
1. Python 3.9 or higher installed
2. Git installed
3. Gemini API key (get from lead/manager)
4. ngrok account (for iOS testing later)

---

## Step 1: Clone and Setup (5 minutes)

```bash
# Clone repository
git clone <repository-url>
cd groceryclaude

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment (2 minutes)

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# Use your text editor (nano, vim, VS Code, etc.)
nano .env
```

In `.env`, replace `your_gemini_api_key_here` with your actual API key:
```
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

---

## Step 3: Verify Setup (1 minute)

```bash
# Test that Gemini API key works
python -c "import google.generativeai as genai; import os; from dotenv import load_dotenv; load_dotenv(); genai.configure(api_key=os.getenv('GEMINI_API_KEY')); print('✅ Gemini API configured successfully!')"
```

If you see "✅ Gemini API configured successfully!", you're ready!

---

## Step 4: Run the App (Once Phase 0 is complete)

```bash
# Terminal 1: Start Flask app
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

Open browser to: http://localhost:5000

---

## Step 5: Run Tests (Once Phase 1+ is complete)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

---

## Step 6: iOS Testing with ngrok (Phase 5)

```bash
# Install ngrok (one-time)
# macOS:
brew install ngrok

# Or download from: https://ngrok.com/download

# Authenticate (one-time)
ngrok config add-authtoken <your-token>

# Terminal 1: Flask app (should already be running)
python app.py

# Terminal 2: Start ngrok
ngrok http 5000
```

Copy the HTTPS URL from ngrok output (e.g., `https://abc123.ngrok-free.app`) and use it in your iOS Shortcut.

---

## 🛠️ Common Commands

### Development
```bash
# Start Flask app
python app.py

# Run in debug mode (auto-reload on changes)
export FLASK_DEBUG=1  # macOS/Linux
set FLASK_DEBUG=1     # Windows
python app.py

# Run tests continuously (auto-run on file changes)
ptw -- tests/ -v
```

### Testing
```bash
# Fast tests only (unit + integration)
pytest tests/ -v -m "not slow"

# Specific test file
pytest tests/test_parsing.py -v

# Specific test
pytest tests/test_parsing.py::test_gemini_success -v
```

### Git
```bash
# Create feature branch
git checkout -b feature/your-task-name

# Stage changes
git add .

# Commit
git commit -m "[Task X] Description of changes"

# Push to remote
git push -u origin feature/your-task-name
```

---

## 📋 Task Assignments

### Developer 1: AI/LLM Specialist
**Branch:** `feature/gemini-parsing`
**Files:** `app.py` (parsing functions)
**Tests:** `tests/test_parsing.py`, `tests/test_parsing_gemini.py`

### Developer 2: Data Management
**Branch:** `feature/deduplication`
**Files:** `app.py` (deduplication functions)
**Tests:** `tests/test_deduplication.py`

### Developer 3: Frontend
**Branch:** `feature/frontend`
**Files:** `templates/index.html`, `static/style.css`, `static/script.js`
**Tests:** Manual UI testing checklist

### Developer 4: QA/Testing
**Branch:** `feature/testing`
**Files:** All `tests/` files
**Focus:** Integration, E2E, regression, performance tests

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'google.generativeai'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key not found"
```bash
# Check .env file exists
ls -la .env

# Check .env contains GEMINI_API_KEY
cat .env

# Make sure python-dotenv loads it
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

### "Port 5000 already in use"
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
python app.py --port 5001
```

---

## 📞 Getting Help

1. **Check documentation:**
   - `IMPLEMENTATION_PLAN_GEMINI.md` - Full implementation plan
   - `TESTING_STRATEGY.md` - Testing guidelines
   - `plannew.md` - Deployment strategy

2. **Ask team lead:** For architecture or Gemini API questions

3. **Check resources:**
   - Gemini API docs: https://ai.google.dev/docs
   - Flask docs: https://flask.palletsprojects.com/
   - pytest docs: https://docs.pytest.org/

---

## ✅ Ready to Code!

You're all set! Start with your assigned task and refer to `IMPLEMENTATION_PLAN_GEMINI.md` for detailed implementation instructions.

**Happy coding! 🛒**
