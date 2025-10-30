# Smart Grocery List - Implementation Plan with Gemini API
**Updated:** 2025-10-30
**Team:** 1 Lead/Manager + 4 Developers
**Deployment:** Local + ngrok (Zero Cost)
**Parsing:** Gemini API (LLM-based)

---

## 🎯 Executive Summary

Building a personal grocery list application with:
- **Gemini API** for intelligent natural language parsing
- **Local Flask app** + **ngrok** for iOS Shortcuts integration
- **Zero deployment costs** (free tier Gemini + free ngrok)
- **Plain text file** database for simplicity

### Key Changes from Original Plan
1. ✅ **Parsing:** Using Gemini API instead of regex
2. ✅ **Deployment:** Local + ngrok instead of Replit
3. ✅ **Cost:** $0 (was going to require paid Replit)

---

## 👥 Team Structure & Task Assignment

### 🎯 Lead Developer / Manager
**Name:** [TBD]
**Responsibilities:**
- Overall architecture and code review
- Gemini API integration oversight
- Team coordination and deployment
- Final QA and sign-off

**Time Commitment:** 6-8 hours across 3 weeks

---

### 👨‍💻 Developer 1: AI/LLM Integration Specialist
**Name:** [TBD]
**Primary Task:** Task 1 - Gemini API Integration for Parsing

**Deliverables:**
1. Gemini API setup and authentication
2. `parse_grocery_items_with_gemini()` function
3. Fallback parsing logic (if API fails)
4. Error handling and retry logic
5. Prompt engineering for optimal results
6. Cost tracking/monitoring
7. Unit tests (50+ scenarios)

**Estimated Time:** 8-10 hours

**Key Technologies:**
- Google Generative AI SDK (`google-generativeai`)
- Environment variable management (`python-dotenv`)
- API error handling and retries

---

### 👨‍💻 Developer 2: Data Management Specialist
**Name:** [TBD]
**Primary Task:** Task 2 - De-duplication Logic

**Deliverables:**
1. `add_items_with_deduplication()` function
2. Case-insensitive duplicate detection
3. File I/O operations (atomic writes)
4. Data persistence layer
5. Unit tests (20+ scenarios)

**Estimated Time:** 3-4 hours

---

### 👨‍💻 Developer 3: Frontend Specialist
**Name:** [TBD]
**Primary Tasks:**
- Task 0 - Initial UI/Backend Setup
- Task 3 - Frontend Refactor

**Deliverables:**
1. Basic Flask app structure
2. Web UI (HTML/CSS/JS)
3. Frontend refactor (separate CSS/JS files)
4. Responsive design
5. Manual UI testing

**Estimated Time:** 5-7 hours

---

### 👨‍💻 Developer 4: QA & Testing Lead
**Name:** [TBD]
**Primary Task:** Task 4 - Testing & Quality Assurance

**Deliverables:**
1. Test infrastructure setup (pytest)
2. Integration tests for API endpoints
3. E2E test scenarios
4. Regression test suite
5. Performance benchmarks
6. iOS Shortcut testing
7. Test documentation

**Estimated Time:** 8-10 hours

---

## 📋 Development Tasks (Updated for Gemini)

### Phase 0: Foundation Setup (Week 1, Days 1-2)
**Owner:** Dev 3 + Lead

**Tasks:**
1. Create project structure
2. Set up virtual environment
3. Create `.env` file for API keys
4. Create `requirements.txt` with Gemini dependencies
5. Basic Flask app with placeholder routes
6. Initial web UI
7. Test basic functionality

**Deliverables:**
- ✅ Project structure created
- ✅ Flask app running on localhost:5000
- ✅ Gemini API key configured
- ✅ Basic web UI functional

**Time:** 4-6 hours

---

### Phase 1: Gemini API Integration (Week 1, Days 3-5)
**Owner:** Dev 1 (AI/LLM Specialist)

**Task 1.1: Gemini API Setup**
- **File:** `app.py` and `.env`
- **Goal:** Configure Gemini API authentication
- **Steps:**
  1. Install `google-generativeai` package
  2. Set up `.env` file with `GEMINI_API_KEY`
  3. Initialize Gemini client in Flask app
  4. Test API connectivity

**Task 1.2: Intelligent Parsing with Gemini**
- **File:** `app.py` → `parse_grocery_items_with_gemini()`
- **Goal:** Use LLM to parse natural language into grocery items
- **Input:** `{"text": "I need milk, eggs, and bread"}`
- **Output:** `["Milk", "Eggs", "Bread"]`
- **Implementation:**
  ```python
  import google.generativeai as genai
  import os
  from dotenv import load_dotenv

  load_dotenv()
  genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

  def parse_grocery_items_with_gemini(raw_text: str) -> list[str]:
      """
      Parse grocery items using Gemini API

      Args:
          raw_text: Natural language text (e.g., "We need milk and eggs")

      Returns:
          List of grocery items (e.g., ["Milk", "Eggs"])
      """
      try:
          model = genai.GenerativeModel('gemini-pro')

          prompt = f"""You are a grocery list assistant. Extract ONLY the grocery items from this text.

Text: "{raw_text}"

Rules:
1. Extract only actual grocery items (food, household products)
2. Remove filler words (we, need, the, a, I, you, etc.)
3. Remove quantities and units (2 gallons, 1 dozen, etc.)
4. Return items in Title Case (e.g., "Milk", "Cheddar Cheese")
5. Separate multiple items with commas
6. If no items found, return empty string

Examples:
Input: "We need milk and eggs"
Output: Milk, Eggs

Input: "Can you grab 2 gallons of milk and a dozen eggs?"
Output: Milk, Eggs

Input: "Pick up cheddar cheese from the store"
Output: Cheddar Cheese

Now extract items from the input text above. Return ONLY the comma-separated list, nothing else."""

          response = model.generate_content(prompt)
          result_text = response.text.strip()

          if not result_text:
              return []

          # Split by comma and clean up
          items = [item.strip() for item in result_text.split(',')]
          items = [item for item in items if item]  # Remove empty strings

          return items

      except Exception as e:
          print(f"Gemini API error: {e}")
          # Fallback to simple parsing
          return fallback_parse(raw_text)

  def fallback_parse(raw_text: str) -> list[str]:
      """
      Simple fallback parsing if Gemini API fails
      Uses basic regex and string manipulation
      """
      import re

      if not raw_text or not raw_text.strip():
          return []

      # Remove common filler words
      filler_words = r'\b(we|need|to|get|the|a|an|some|buy|grab|pick|up|from|store|I|you|they)\b'
      text = re.sub(filler_words, ' ', raw_text, flags=re.IGNORECASE)

      # Split by common delimiters
      items = re.split(r',|\sand\s|\sor\s', text)

      # Clean and capitalize
      cleaned = []
      for item in items:
          item = item.strip()
          if item:
              # Remove quantities
              item = re.sub(r'^\d+\s*(gallons?|lbs?|oz|dozen|bottles?|of)?\s*', '', item, flags=re.IGNORECASE)
              item = item.strip()
              if item:
                  cleaned.append(item.title())

      return cleaned
  ```

**Task 1.3: Error Handling & Retry Logic**
- Handle API failures gracefully
- Implement exponential backoff for retries
- Log API errors for debugging
- Monitor API usage/costs

**Task 1.4: Unit Testing**
- Test with 50+ scenarios (see TESTING_STRATEGY.md)
- Test API failure scenarios
- Test fallback parsing
- Ensure 100% code coverage

**Status:** ⏳ To Do
**Time:** 8-10 hours
**Priority:** 🔴 CRITICAL

---

### Phase 2: De-duplication (Week 2, Days 1-2)
**Owner:** Dev 2 (Data Management Specialist)

**Task 2.1: Duplicate Detection**
- **File:** `app.py` → `add_items_with_deduplication()`
- **Goal:** Prevent duplicate items (case-insensitive)
- **Implementation:** (Same as original plan)
- **Time:** 3-4 hours

---

### Phase 3: Frontend Refactor (Week 2, Days 3-4)
**Owner:** Dev 3 (Frontend Specialist)

**Task 3.1: Separate CSS/JS**
- **Files:** Extract to `static/style.css` and `static/script.js`
- **Time:** 1-2 hours

---

### Phase 4: Testing (Week 2-3)
**Owner:** Dev 4 (QA Lead)

**Task 4.1: Test Infrastructure**
- Set up pytest with fixtures
- **Time:** 1-2 hours

**Task 4.2: Integration Tests**
- Test all API endpoints with Gemini parsing
- **Time:** 3-4 hours

**Task 4.3: E2E & Performance Tests**
- Complete user journeys
- Performance benchmarks
- **Time:** 2-3 hours

**Task 4.4: iOS Integration Testing**
- Deploy with ngrok
- Test iOS Shortcut
- **Time:** 2-3 hours

---

### Phase 5: Deployment & iOS Setup (Week 3, Days 1-3)
**Owner:** Lead + All Devs

**Task 5.1: Local Deployment Setup**

**Terminal 1: Run Flask App**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run app
python app.py
```

**Terminal 2: Run ngrok**
```bash
# Install ngrok (one-time)
# macOS: brew install ngrok
# Or download from https://ngrok.com/download

# Authenticate (one-time)
ngrok config add-authtoken <your-token>

# Expose Flask app
ngrok http 5000
```

**Task 5.2: iOS Shortcut Configuration**
1. Copy ngrok HTTPS URL (e.g., `https://abc123.ngrok-free.app`)
2. Create iOS Shortcut:
   - Name: "Add to Grocery List"
   - Action: Get text from Share Sheet
   - Action: POST to `https://abc123.ngrok-free.app/add-item`
   - Body: `{"text": "[text]"}`
   - Headers: `Content-Type: application/json`

**Task 5.3: Testing**
1. Send test message to Shortcut
2. Verify items appear in web UI
3. Test duplicate prevention
4. Test various message formats

**Note:** ngrok URL changes each time you restart it. Update iOS Shortcut when needed.

**Time:** 2-3 hours

---

## 🔧 Setup Instructions

### Prerequisites
- Python 3.9+
- Gemini API key (free tier: 60 requests/minute)
- ngrok account (free tier sufficient)

### Step 1: Clone/Setup Project
```bash
mkdir groceryclaude
cd groceryclaude
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Step 3: Create `requirements.txt`
```
Flask==2.3.0
google-generativeai==0.3.0
python-dotenv==1.0.0
pytest==7.4.0
pytest-flask==1.2.0
pytest-cov==4.1.0
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables
Create `.env` file:
```bash
# Gemini API Key (get from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
```

Create `.env.example` (for version control):
```bash
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_APP=app.py
FLASK_ENV=development
```

### Step 6: Update `.gitignore`
```
# Environment variables
.env

# Database
grocery_list.txt

# Python
__pycache__/
*.pyc
*.pyo
venv/
.pytest_cache/
htmlcov/
.coverage

# IDE
.vscode/
.idea/
```

### Step 7: Create Initial Flask App
See Phase 0 deliverables

---

## 📁 Project Structure

```
groceryclaude/
├── app.py                          # Flask backend with Gemini integration
├── .env                            # API keys (NOT in git)
├── .env.example                    # Template for .env
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── grocery_list.txt                # Database (auto-created)
│
├── templates/
│   └── index.html                  # Web UI
│
├── static/
│   ├── style.css                   # CSS styles
│   └── script.js                   # JavaScript
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_parsing.py             # Parsing tests (Gemini + fallback)
│   ├── test_deduplication.py       # De-duplication tests
│   ├── test_api_endpoints.py       # API integration tests
│   ├── test_integration.py         # E2E tests
│   ├── test_regression.py          # Regression suite
│   ├── test_performance.py         # Performance tests
│   └── fixtures/
│       └── test_data.py            # Test data
│
└── docs/
    ├── IMPLEMENTATION_PLAN_GEMINI.md    # This file
    ├── TESTING_STRATEGY.md              # Test strategy (mostly unchanged)
    └── plannew.md                       # Original plan (reference)
```

---

## 🧪 Testing Strategy Updates

### Unit Tests for Gemini Parsing

**New Test File:** `tests/test_parsing_gemini.py`

```python
import pytest
from unittest.mock import patch, MagicMock
from app import parse_grocery_items_with_gemini, fallback_parse

@pytest.mark.unit
class TestGeminiParsing:
    """Test Gemini API parsing"""

    @patch('google.generativeai.GenerativeModel')
    def test_gemini_success(self, mock_model):
        """Test successful Gemini API call"""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.text = "Milk, Eggs, Bread"
        mock_model.return_value.generate_content.return_value = mock_response

        result = parse_grocery_items_with_gemini("We need milk, eggs, and bread")
        assert result == ["Milk", "Eggs", "Bread"]

    @patch('google.generativeai.GenerativeModel')
    def test_gemini_api_failure_fallback(self, mock_model):
        """Test fallback when Gemini API fails"""
        # Mock API failure
        mock_model.return_value.generate_content.side_effect = Exception("API Error")

        result = parse_grocery_items_with_gemini("milk, eggs, bread")
        # Should fallback to simple parsing
        assert len(result) > 0
        assert "Milk" in result or "milk" in str(result).lower()

    def test_fallback_parsing(self):
        """Test fallback parser works independently"""
        result = fallback_parse("milk, eggs, bread")
        assert len(result) == 3

@pytest.mark.unit
class TestCostTracking:
    """Test API cost tracking"""

    def test_api_call_count(self):
        """Test we track API calls for cost monitoring"""
        # Implement API call counter
        pass
```

### Integration Tests
All existing integration tests remain the same - they test the API endpoints, not the implementation details.

---

## 💰 Cost Analysis

### Gemini API Pricing (as of Oct 2025)
- **Free Tier:** 60 requests/minute, 1,500 requests/day
- **For this use case:** Extremely low usage (~10-50 requests/day)
- **Estimated cost:** $0/month (well within free tier)

### ngrok Pricing
- **Free Tier:** 1 online agent, HTTPS tunneling
- **Limitation:** URL changes on each restart
- **Pro Tier:** $8/month for static URLs (optional)
- **Our choice:** Free tier is sufficient

### Total Monthly Cost: **$0** 🎉

---

## 🔐 Security Considerations

### API Key Management
1. **NEVER commit `.env` to git**
2. Use `.env.example` as template
3. Rotate API keys periodically
4. Monitor API usage for suspicious activity

### ngrok Security
1. URL is temporary and changes frequently
2. Only you know the URL (don't share publicly)
3. Consider adding basic authentication if needed

---

## 📊 Success Criteria

### Functional Requirements
1. ✅ Gemini API successfully parses natural language
2. ✅ Fallback parsing works if API fails
3. ✅ De-duplication prevents duplicate items
4. ✅ Items persist in `grocery_list.txt`
5. ✅ Web UI displays and deletes items
6. ✅ iOS Shortcut integration works via ngrok
7. ✅ Response time < 3 seconds (including API call)

### Technical Requirements
1. ✅ 90%+ test coverage for critical code
2. ✅ All tests passing
3. ✅ Gemini API error handling robust
4. ✅ Fallback parsing tested
5. ✅ API cost stays within free tier

---

## 🚀 Development Workflow

### Daily Workflow
1. **Start Flask app:** `python app.py` (Terminal 1)
2. **Start ngrok:** `ngrok http 5000` (Terminal 2)
3. **Develop and test locally**
4. **Run tests:** `pytest tests/ -v`

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/gemini-parsing

# Make changes
git add .
git commit -m "[Task 1] Implement Gemini API parsing"

# Push and create PR
git push -u origin feature/gemini-parsing
```

### Testing Workflow
```bash
# Unit tests (fast)
pytest tests/test_parsing.py -v

# Integration tests
pytest tests/test_api_endpoints.py -v

# All tests with coverage
pytest tests/ -v --cov=app --cov-report=html
```

---

## 📅 Timeline

### Week 1: Foundation + Gemini Integration
- **Day 1-2:** Phase 0 - Setup (Dev 3 + Lead)
- **Day 3-5:** Phase 1 - Gemini API (Dev 1)
- **Milestone:** Parsing works with Gemini

### Week 2: Core Features + Testing
- **Day 1-2:** Phase 2 - De-duplication (Dev 2)
- **Day 3-4:** Phase 3 - Frontend refactor (Dev 3)
- **Day 1-5:** Phase 4 - Testing (Dev 4, ongoing)
- **Milestone:** All features implemented, 80% tested

### Week 3: Deployment + iOS + QA
- **Day 1-3:** Phase 5 - Deployment & iOS (Lead + All)
- **Day 4-5:** Final QA and bug fixes
- **Milestone:** Production ready, iOS working

---

## 🎓 Documentation Updates Needed

### Files to Update
1. ✅ **This file** - New implementation plan
2. ⏳ **claude.md** - Update parsing section to reference Gemini
3. ⏳ **TESTING_STRATEGY.md** - Add Gemini-specific tests
4. ⏳ **README.md** - Create project overview

---

## 🛠️ Troubleshooting

### Gemini API Issues

**Issue:** API key not working
```bash
# Verify API key is set
echo $GEMINI_API_KEY  # macOS/Linux
echo %GEMINI_API_KEY%  # Windows

# Test API key
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('Success')"
```

**Issue:** Rate limit exceeded
- Free tier: 60 requests/minute
- Solution: Implement caching or upgrade tier

**Issue:** API timeout
- Add timeout to API calls
- Use fallback parsing

### ngrok Issues

**Issue:** ngrok URL not accessible
```bash
# Check ngrok is running
curl http://localhost:4040/api/tunnels

# Restart ngrok
ngrok http 5000
```

**Issue:** URL changed and iOS Shortcut doesn't work
- Update Shortcut with new ngrok URL
- Consider ngrok Pro for static URL

---

## 📋 Acceptance Criteria Checklist

All criteria from original plan, plus:

### Additional Gemini-Specific Criteria

✅ **10. Gemini parsing accuracy**
- Test: Send 20 different messages, verify parsing accuracy > 95%
- Command: Run test suite in `test_parsing_gemini.py`

✅ **11. Fallback parsing works**
- Test: Disconnect internet, verify fallback parsing kicks in
- Manual test: Set invalid API key, send request

✅ **12. API costs stay within free tier**
- Monitor: Check API usage in Google Cloud Console
- Verify: < 1,500 requests/day

✅ **13. Response time acceptable**
- Test: Send message via iOS Shortcut
- Verify: Items appear in < 3 seconds (including API latency)

---

## 🎉 Next Steps

### For Lead/Manager (You):
1. ✅ Review this plan
2. ⏳ Assign developers to tasks
3. ⏳ Set up Gemini API key (get from Google AI Studio)
4. ⏳ Schedule Week 1 kickoff meeting
5. ⏳ Create GitHub repository

### For Developer 1 (AI/LLM Specialist):
1. ⏳ Get familiar with Gemini API documentation
2. ⏳ Set up development environment
3. ⏳ Start Phase 1 - Gemini integration

### For Developer 2-4:
1. ⏳ Review this plan
2. ⏳ Set up development environment
3. ⏳ Review TESTING_STRATEGY.md
4. ⏳ Wait for Phase 0 completion

---

## 📞 Resources

### Gemini API
- **Documentation:** https://ai.google.dev/docs
- **API Key:** https://makersuite.google.com/app/apikey
- **Python SDK:** https://github.com/google/generative-ai-python
- **Pricing:** https://ai.google.dev/pricing

### ngrok
- **Documentation:** https://ngrok.com/docs
- **Download:** https://ngrok.com/download
- **Pricing:** https://ngrok.com/pricing

### Original Documentation
- **claude.md** - Original requirements
- **TESTING_STRATEGY.md** - Comprehensive testing guide
- **plannew.md** - Deployment strategy reference

---

**Document Version:** 2.0 (Gemini Edition)
**Last Updated:** 2025-10-30
**Status:** ✅ Ready for Development
**Key Changes:** Gemini API integration, local + ngrok deployment

---

## Summary of Changes from Original Plan

| Aspect | Original Plan | New Plan (Gemini) |
|--------|---------------|-------------------|
| **Parsing** | Regex + string manipulation | Gemini API + fallback |
| **Deployment** | Replit (paid) | Local + ngrok (free) |
| **Dependencies** | Flask only | Flask + google-generativeai + python-dotenv |
| **Cost** | ~$5-10/month | $0/month |
| **Setup** | Deploy to cloud | Run locally |
| **API Keys** | None | Gemini API key required |
| **Complexity** | Lower (local parsing) | Medium (API integration) |
| **Accuracy** | Good (regex) | Excellent (LLM) |

**Trade-off:** Slightly more complex setup (API keys, environment variables) for significantly better parsing accuracy and zero ongoing costs.

**Recommendation:** ✅ Proceed with Gemini approach - better user experience, free, and more scalable.
