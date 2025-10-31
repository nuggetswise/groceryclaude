# Smart Grocery List - Revised Implementation Plan
**Personal Project for iOS Integration**

**Created:** 2025-10-30
**Developer:** Solo (You)
**Timeline:** 4-6 hours (1-2 days)
**Deployment:** Local development only (no domain)

---

## Project Overview

Building a personal grocery list web app that:
- Runs locally on your machine
- Uses Gemini LLM for intelligent parsing
- Integrates with iOS Shortcuts via local network
- Stores data in simple text file

**Key Insight:** This is a personal productivity tool, not a production application. Keep it simple and functional.

---

## Tech Stack

**Backend:**
- Python 3.9+ with Flask
- Google Gemini API for natural language parsing
- Plain text file storage (`grocery_list.txt`)

**Frontend:**
- Simple HTML/CSS/JS (no framework needed)
- Mobile-friendly for iOS usage

**Integration:**
- iOS Shortcuts → POST to ngrok tunnel → local Flask server
- ngrok provides HTTPS URL for reliable iOS access

**Dependencies:**
```
Flask==2.3.0
google-generativeai==0.3.0
python-dotenv==1.0.0
```

**External Tools:**
- ngrok (for secure tunnel to localhost)

---

## Implementation Phases

### Phase 1: Basic Flask Foundation (45 minutes)

**Goal:** Get a working Flask app with basic functionality

**Tasks:**
1. Create `app.py` with Flask routes
2. Create basic HTML template
3. Implement file-based storage (read/write)
4. Test basic add/delete functionality

**Deliverables:**
- Working Flask server on `localhost:5000`
- Basic web UI that displays items
- Can manually add/delete items
- Data persists in `grocery_list.txt`

**Files to Create:**
```
app.py                    # Main Flask application
templates/index.html      # Web UI
grocery_list.txt         # Data storage (auto-created)
requirements.txt         # Dependencies
```

---

### Phase 2: Gemini LLM Integration (90 minutes)

**Goal:** Replace manual input with intelligent parsing using Gemini

**Tasks:**
1. Set up Gemini API client
2. Create parsing function that calls Gemini
3. Design effective prompt for grocery item extraction
4. Handle API errors gracefully
5. Test with various input formats

**Key Function:**
```python
def parse_grocery_items_with_gemini(raw_text: str) -> list[str]:
    """Use Gemini to extract grocery items from natural language."""
    # Call Gemini API with structured prompt
    # Return clean list of items
```

**Gemini Prompt Strategy:**
```
Extract grocery items from this text: "{raw_text}"

Rules:
- Return only the grocery items, one per line
- Remove filler words (I, we, need, etc.)
- Normalize to title case (Milk, not milk)
- Remove quantities (2 gallons of milk → Milk)
- If no items found, return empty

Examples:
Input: "We need milk, eggs, and bread"
Output:
Milk
Eggs
Bread

Input: "Can you grab 2 gallons of milk and a dozen eggs?"
Output:
Milk
Eggs

Now extract from: "{raw_text}"
```

**Error Handling:**
- API rate limits → fallback to simple parsing
- Network errors → graceful degradation
- Invalid responses → log and skip

---

### Phase 3: Deduplication & Polish (30 minutes)

**Goal:** Prevent duplicates and improve user experience

**Tasks:**
1. Add deduplication logic (case-insensitive)
2. Improve web UI styling
3. Add loading states
4. Test edge cases

**Deduplication Logic:**
```python
def add_items_with_deduplication(new_items: list[str]) -> dict:
    """Add items, preventing duplicates."""
    existing = read_grocery_list()
    existing_lower = [item.lower() for item in existing]
    
    added = []
    skipped = []
    
    for item in new_items:
        if item.lower() not in existing_lower:
            existing.append(item)
            added.append(item)
        else:
            skipped.append(item)
    
    write_grocery_list(existing)
    return {"added": added, "skipped": skipped}
```

---

### Phase 4: ngrok & iOS Integration (45 minutes)

**Goal:** Set up ngrok tunnel and iOS Shortcuts integration

**Tasks:**
1. Install and configure ngrok
2. Start ngrok tunnel to Flask server
3. Test API endpoints with curl using ngrok URL
4. Create iOS Shortcut with ngrok URL
5. Test end-to-end workflow

**ngrok Setup:**
```bash
# Install ngrok (if not already installed)
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Start Flask server
python app.py  # Runs on localhost:5000

# In another terminal, start ngrok tunnel
ngrok http 5000

# ngrok will provide URLs like:
# https://abc123.ngrok.io -> http://localhost:5000
```

**Flask Configuration:**
```python
# In app.py - no special network config needed with ngrok
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

**iOS Shortcut Configuration:**
- Action: "Get Contents of URL"
- URL: `https://YOUR_NGROK_URL.ngrok.io/add-item`
- Method: POST
- Headers: `Content-Type: application/json`
- Request Body: `{"text": "[Shortcut Input]"}`

**Testing Workflow:**
1. Start Flask server: `python app.py`
2. Start ngrok tunnel: `ngrok http 5000`
3. Copy ngrok HTTPS URL
4. Test with curl: `curl -X POST https://abc123.ngrok.io/add-item -H "Content-Type: application/json" -d '{"text":"test milk"}'`
5. Update iOS Shortcut with ngrok URL
6. Send test message from iOS
7. Check web UI for new items

---

## File Structure

```
groceryclaude/
├── app.py                    # Main Flask application
├── .env                      # Gemini API key (already exists)
├── requirements.txt          # Python dependencies
├── grocery_list.txt          # Data storage (auto-created)
├── templates/
│   └── index.html            # Web UI
├── static/                   # Optional: CSS/JS files
│   ├── style.css
│   └── script.js
└── README.md                 # Simple usage instructions
```

---

## Core Functions to Implement

### 1. Gemini Integration
```python
import google.generativeai as genai
from dotenv import load_dotenv

def setup_gemini():
    """Initialize Gemini API client."""
    load_dotenv()
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    return genai.GenerativeModel('gemini-pro')

def parse_grocery_items_with_gemini(raw_text: str) -> list[str]:
    """Extract grocery items using Gemini LLM."""
    model = setup_gemini()
    
    prompt = f"""Extract grocery items from this text: "{raw_text}"

Rules:
- Return only the grocery items, one per line
- Remove filler words (I, we, need, etc.)
- Normalize to title case (Milk, not milk)
- Remove quantities (2 gallons of milk → Milk)
- If no items found, return empty

Examples:
Input: "We need milk, eggs, and bread"
Output:
Milk
Eggs
Bread

Now extract from: "{raw_text}"
"""
    
    try:
        response = model.generate_content(prompt)
        items = [item.strip() for item in response.text.split('\n') if item.strip()]
        return items
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to simple parsing
        return simple_fallback_parse(raw_text)
```

### 2. File Operations
```python
def read_grocery_list() -> list[str]:
    """Read items from grocery_list.txt."""
    try:
        with open('grocery_list.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def write_grocery_list(items: list[str]) -> None:
    """Write items to grocery_list.txt."""
    with open('grocery_list.txt', 'w') as f:
        for item in items:
            f.write(f"{item}\n")
```

### 3. Flask Routes
```python
@app.route('/add-item', methods=['POST'])
def add_item():
    """Add items from natural language (iOS Shortcut endpoint)."""
    data = request.get_json()
    raw_text = data.get('text', '')
    
    if not raw_text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Parse with Gemini
    parsed_items = parse_grocery_items_with_gemini(raw_text)
    
    # Add with deduplication
    result = add_items_with_deduplication(parsed_items)
    
    return jsonify({
        'success': True,
        'added': result['added'],
        'skipped': result['skipped'],
        'total_items': len(read_grocery_list())
    })
```

---

## Testing Strategy (Minimal)

**Manual Testing Checklist:**
- [ ] Flask server starts without errors
- [ ] Web UI loads and displays items
- [ ] Can add items via web form
- [ ] Can delete items by clicking
- [ ] Gemini parsing works with test inputs
- [ ] Deduplication prevents duplicates
- [ ] iOS Shortcut successfully adds items
- [ ] Data persists after server restart

**Test Inputs for Gemini:**
```
"milk, eggs, bread"
"We need milk and eggs"
"Can you grab 2 gallons of milk?"
"I'm out of cheddar cheese"
"Pick up some apples and bananas from the store"
"Get stuff for tacos - ground beef, tortillas, cheese, lettuce"
```

**No Unit Tests Needed:** This is a personal tool. Manual testing is sufficient.

---

## Environment Setup

### 1. Install Dependencies
```bash
pip install Flask google-generativeai python-dotenv
```

### 2. Update .env File
```bash
# Your .env already has:
GEMINI_API_KEY=AIzaSyBN35WR64ZNfeFFP-jnUPolQeJK_NhSW3A
```

### 3. Run Application
```bash
python app.py
# Server starts on http://0.0.0.0:5000
```

### 4. Start ngrok Tunnel
```bash
# Start Flask server
python app.py

# In another terminal, start ngrok
ngrok http 5000

# Copy the HTTPS URL for iOS Shortcut
# Example: https://abc123.ngrok.io/add-item
```

---

## iOS Shortcut Setup

**Shortcut Name:** "Add to Grocery List"

**Actions:**
1. **Get Text from Input** (receives shared text)
2. **Get Contents of URL**
   - URL: `https://YOUR_NGROK_URL.ngrok.io/add-item`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Request Body: `{"text": "[Text from Step 1]"}`
3. **Show Notification** (optional)
   - Title: "Added to Grocery List"
   - Body: "Items processed successfully"

**Usage:**
- Share any text message to this shortcut
- It extracts grocery items and adds them to your list
- Check the web UI to see results

---

## Advantages of This Approach

**Using Gemini LLM:**
- Much better natural language understanding than regex
- Handles complex sentences: "Get stuff for tacos"
- Learns from context and examples
- Robust quantity removal and normalization

**Local Development with ngrok:**
- No deployment complexity
- No domain/hosting costs
- Secure HTTPS tunnel for iOS
- Fast iteration and testing
- Complete control over data

**Simple Architecture:**
- Single Python file for backend
- Plain text storage (no database)
- Minimal dependencies
- Easy to modify and extend

---

## Future Enhancements (Optional)

**If you want to expand later:**
- Add categories (Produce, Dairy, etc.)
- Store quantities separately
- Add item suggestions based on history
- Export to other formats (Apple Notes, etc.)
- Add web UI for managing the list
- Multiple lists (Costco vs regular grocery)

**But for now:** Keep it simple and functional.

---

## Timeline Breakdown

| Phase | Time | Tasks |
|-------|------|-------|
| **Phase 1** | 45 min | Basic Flask app, file storage, web UI |
| **Phase 2** | 90 min | Gemini integration, parsing function |
| **Phase 3** | 30 min | Deduplication, UI polish |
| **Phase 4** | 45 min | iOS Shortcut setup, testing |
| **Total** | **3.5 hours** | Complete working system |

**Buffer:** Add 1-2 hours for debugging and refinement.

---

## Success Criteria

**Must Work:**
- [ ] iOS message → Gemini parsing → grocery list
- [ ] Web UI shows current list
- [ ] Can delete items by clicking
- [ ] No duplicate items added
- [ ] Data persists between sessions

**Example Success Test:**
1. Send iOS message: "We're out of milk and need eggs for breakfast"
2. Check web UI: "Milk" and "Eggs" appear
3. Send same message again: No duplicates added
4. Click "Milk" in UI: Item is removed
5. Restart Flask server: "Eggs" still there

---

## Getting Started

**Next Steps:**
1. Install ngrok: `brew install ngrok` (or download from ngrok.com)
2. Create `requirements.txt`
3. Build basic `app.py` with Flask routes
4. Create simple `templates/index.html`
5. Test basic functionality
6. Add Gemini integration
7. Set up ngrok tunnel
8. Create iOS Shortcut with ngrok URL

Want me to start implementing this step by step?

---

**This plan is realistic, achievable, and focused on your actual use case.**