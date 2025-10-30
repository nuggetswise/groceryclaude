# Smart Grocery List - Claude Code Development Guide

## Project Overview

This is a personal grocery list web application built with Python (Flask) that integrates with iOS Shortcuts. Users can:
1. View their grocery list via a web UI
2. Add items by forwarding messages from iOS (via Shortcuts)
3. Delete items by clicking them in the web UI

**Tech Stack:** Python 3, Flask, HTML, CSS, JavaScript
**Database:** `grocery_list.txt` (line-delimited plain text)
**Deployment Target:** Replit (with public HTTPS URL for iOS Shortcuts)

---

## Current Architecture

### Backend (app.py)
- Flask server running on `0.0.0.0:5000`
- Serves static web UI at `/`
- Provides API endpoints for the frontend and iOS Shortcuts

### Frontend (templates/index.html)
- Single-page HTML application
- Fetches list from API
- Allows users to "strike" (delete) items by clicking
- Includes inline CSS and JavaScript

### Database (grocery_list.txt)
- Simple text file, one item per line
- Example:
  ```
  Milk
  Eggs
  Bread
  ```

---

## API Endpoints (Current)

### GET /
- Serves the main web interface (`templates/index.html`)

### GET /get-items
- Returns JSON array of current grocery items
- Response: `["Milk", "Eggs", "Bread"]`
- Used by the frontend to display the list

### POST /delete-item
- Deletes an item from the list
- Request body: `{"item": "Milk"}`
- Rewrites `grocery_list.txt` without the deleted item

### POST /add-item
- **Primary iOS Shortcut integration point**
- Accepts raw message text from iOS Shortcuts
- Request body: `{"text": "We need milk, eggs, and bread"}`
- **Current behavior:** Appends raw text as-is to `grocery_list.txt`
- **Needs improvement:** Should parse and add items individually

---

## Development Tasks (Priority Order)

### TASK 1: Intelligent Item Parsing (HIGH PRIORITY)

**Goal:** Modify `/add-item` endpoint to parse natural language text and extract individual grocery items.

**Current Behavior:**
- Input: `{"text": "We need milk, eggs, and bread"}`
- Current output: Appends entire string to file
- Problem: Stores "We need milk, eggs, and bread" as a single item instead of three items

**Desired Behavior:**
- Input: `{"text": "We need milk, eggs, and bread"}`
- Desired output: Adds three separate items to the file:
  ```
  Milk
  Eggs
  Bread
  ```

**Requirements:**
- Handle common delimiters: commas (,), "and", "or"
- Normalize items: strip whitespace, capitalize properly
- Extract only meaningful nouns/items (ignore filler words like "we", "need", "the")
- Handle quantities gracefully:
  - "2 gallons of milk" → "Milk" (or "Milk (2 gal)" if you want to keep quantity)
  - "1 dozen eggs" → "Eggs" (or "Eggs (1 dz)")
- Handle common variations:
  - "tomatos" vs "tomatoes" (normalize to standard spelling)
  - "carrots" vs "baby carrots" (treat as different items, or same?)

**Implementation Location:** Add a parsing function in `app.py`, call it from the `/add-item` route.

**Example parsing cases to handle:**
- "milk, eggs, bread" → ["Milk", "Eggs", "Bread"]
- "milk and eggs and bread" → ["Milk", "Eggs", "Bread"]
- "I need milk, eggs, or bread" → ["Milk", "Eggs", "Bread"]
- "2 gallons of milk and a dozen eggs" → ["Milk", "Eggs"] (or with quantities)
- "We're out of cheddar cheese and need more" → ["Cheddar Cheese"]

**Approach:**
- Use Python string manipulation (split, regex, common delimiters)
- No external API calls—keep it local
- Keep the logic simple and readable
- Add comments explaining the parsing logic

---

### TASK 2: De-duplication (HIGH PRIORITY)

**Goal:** Prevent duplicate items from being added to the list.

**Current Problem:**
- User can add "milk" multiple times
- List grows with duplicates: Milk, Eggs, Milk, Bread, Milk

**Desired Behavior:**
- Before adding new items (after parsing), check if they already exist in `grocery_list.txt`
- If an item already exists, don't add it again
- Provide feedback (optional): "Milk already in list" or just silently skip

**Requirements:**
- Case-insensitive comparison: "Milk", "milk", "MILK" should all be treated as the same
- Trim whitespace before comparing
- Handle variations (optional, nice-to-have):
  - Should "Carrots" and "Baby Carrots" be treated as duplicates? (Probably not—keep them separate)
  - Should "Milk (2 gal)" and "Milk" be treated as the same? (Yes, probably)

**Implementation Location:** Add logic in the `/add-item` route, after parsing but before writing to file.

**Pseudocode:**
```
1. Parse the input text → get list of new items
2. Load current items from grocery_list.txt
3. For each new item:
   - Check if it already exists (case-insensitive)
   - If not, add it to the file
4. Return success response
```

---

### TASK 3: Frontend Refactor (MEDIUM PRIORITY)

**Goal:** Split inline CSS and JavaScript from `index.html` into separate static files for better maintainability.

**Current Structure:**
- `templates/index.html` contains everything (HTML, CSS, JavaScript)
- Gets large and hard to maintain

**Desired Structure:**
```
templates/
  index.html          (HTML only)
static/
  style.css           (CSS styles)
  script.js           (JavaScript logic)
```

**Requirements:**
- Update `index.html` to link to external CSS and JS files
- Extract all `<style>` blocks to `static/style.css`
- Extract all `<script>` blocks to `static/script.js`
- Update `app.py` to serve static files correctly (Flask does this automatically with the `static/` folder)
- Ensure no functionality changes—everything should work the same as before

**Key Functions to Extract to script.js:**
- Fetch and display the grocery list
- Handle item deletion (strike through and remove)
- Update UI reactively

**Key Styles to Extract to style.css:**
- All layout, colors, typography
- Responsive design (if any)
- Animation/transitions

---

### TASK 4: iOS Shortcut Integration Testing (AFTER OTHER TASKS)

**Goal:** Ensure the `/add-item` endpoint works smoothly with iOS Shortcuts.

**What to Test:**
- Create a test iOS Shortcut that posts JSON to `/add-item`
- Send various message formats and verify parsing works
- Check that items appear in the web UI immediately
- Verify duplicates are not added on repeated messages

**Example iOS Shortcut Payload:**
```json
{
  "text": "Can you grab milk, eggs, and bread from the store?"
}
```

**Expected Result:**
- Three items added to list: Milk, Eggs, Bread
- No duplicates if the same message is sent twice
- Web UI updates automatically (user refreshes or auto-refresh)

---

## File Structure (Current & Target)

```
project-root/
├── app.py                    # Main Flask server
├── grocery_list.txt          # Database file (auto-created)
├── templates/
│   └── index.html            # Web UI (HTML + CSS + JS currently)
├── static/                   # Create this folder
│   ├── style.css             # Create: Extract CSS from index.html
│   └── script.js             # Create: Extract JS from index.html
└── claude.md                 # This file
```

---

## Implementation Notes

### When Modifying app.py

1. **Import statements needed:**
   - `Flask`, `request`, `jsonify` (already in Flask)
   - `os` (for file operations)
   - Possibly `re` (for regex, if needed for parsing)

2. **File I/O operations:**
   - Read: Open `grocery_list.txt`, split by `\n`, strip whitespace
   - Write: Join items with `\n`, write back to file
   - Handle edge cases: Empty file, file doesn't exist yet

3. **Error handling:**
   - What if `/add-item` receives malformed JSON? Return 400 error
   - What if parsing fails? Fall back gracefully (log error, skip item, or return error)
   - What if file write fails? Return 500 error

4. **Keep it simple:**
   - No database complexity—text file is fine
   - No authentication needed—it's for personal use
   - Focus on robustness (error handling) over features

### Parsing Strategy

**Recommended approach (no external APIs):**
- Split by common delimiters: `,`, ` and `, ` or `
- Remove filler words: "I", "we", "need", "the", "a", "is", "are", etc.
- Capitalize first letter of each word
- Strip extra whitespace
- Remove quantities if desired (or keep them)

**Example Python pseudocode:**
```python
def parse_grocery_text(raw_text):
    # Remove common filler words and split
    items = re.split(r',|\sand\s|\sor\s', raw_text)
    
    # Clean each item
    cleaned_items = []
    for item in items:
        item = item.strip()
        # Remove leading filler words
        item = re.sub(r'^(we|I|you|they|the|a|an|need|to|get|buy|grab|pick up)\s+', '', item, flags=re.IGNORECASE)
        item = item.strip()
        
        # Capitalize
        item = item.title()
        
        if item:  # Only add non-empty items
            cleaned_items.append(item)
    
    return cleaned_items
```

---

## Testing Checklist

Before considering the project "done," test these scenarios:

- [ ] Add a simple item: "milk" → appears as "Milk"
- [ ] Add multiple items: "milk, eggs, bread" → all three appear separately
- [ ] Delete an item: Click it in the web UI, it's removed
- [ ] De-duplication: Add "milk" twice → appears only once
- [ ] Case insensitivity: Add "Milk" then "milk" → still only one "Milk"
- [ ] Natural language: "I need milk and eggs" → extracts "Milk" and "Eggs"
- [ ] Quantities: "2 gallons of milk" → adds as "Milk" (or "Milk (2 gal)" if keeping qty)
- [ ] Refresh web UI: Items persist after page reload
- [ ] iOS Shortcut integration: Send a test message, verify it appears

---

## Deployment Notes (Replit)

When deploying to Replit:

1. Upload all files (app.py, templates/, static/, grocery_list.txt)
2. Create a `.replit` file:
   ```
   run = "python app.py"
   ```
3. Create a `requirements.txt`:
   ```
   Flask
   ```
4. Click "Run" → Replit gives you a public URL (e.g., `my-app.replit.dev`)
5. Use that URL in iOS Shortcut: `https://my-app.replit.dev/add-item`

---

## Questions for Claude Code

When working with Claude Code, you can ask:

1. "Parse the `/add-item` endpoint to intelligently extract grocery items from natural language text."
2. "Add de-duplication logic to prevent duplicate items in the grocery list."
3. "Refactor the frontend: extract CSS and JavaScript from index.html into separate static files."
4. "Review the error handling in app.py and suggest improvements."
5. "Optimize the file I/O operations in app.py for reliability."

---

## Future Enhancements (Out of Scope for Now)

These are nice-to-haves for later:

- Add categories (Produce, Dairy, Frozen, etc.)
- Add item quantities that persist (not just for display)
- Add timestamps (when items were added)
- Add estimated costs
- Add a "completed" status instead of deletion
- Multi-user support (if sharing with household members)
- Sync across devices
- Weekly/recurring item suggestions

---

## Summary

This is a simple but useful personal tool. Focus on getting **parsing** and **de-duplication** working well, then refactor the frontend. After that, it's ready to deploy to Replit and use with iOS Shortcuts for daily use.

Good luck! 🛒