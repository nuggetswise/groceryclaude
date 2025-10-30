# Smart Grocery List - Final Development & Deployment Plan

## Project Status
- **Phase:** Planning & Development
- **Current State:** Local Flask app (working)
- **Target:** Public iOS Shortcut integration + web UI
- **Deployment Strategy:** ngrok for iOS, local development machine

---

## 🎯 Final Approach

We're **NOT using Replit** due to paid plan requirements. Instead, we'll use:

1. **Local Development:** Keep Flask app running on your development machine
2. **Public URL for iOS:** Use ngrok (free) to expose the app publicly when needed
3. **Web UI:** Accessible via `http://localhost:5000` on your network or via ngrok URL
4. **Database:** Continue using `grocery_list.txt` (simple, reliable, no setup needed)

### Why This Approach?

✅ **Zero deployment cost** - No paid services required  
✅ **Zero setup complexity** - No Docker, no cloud infrastructure  
✅ **Full control** - Everything runs on your machine  
✅ **Perfect for personal use** - Your grocery list, your data, your machine  
✅ **iOS Shortcuts works great** - ngrok provides stable public HTTPS URLs  

---

## 📋 Development Tasks (In Order)

### Phase 1: Core Feature Development (BEFORE iOS Integration)

**Task 1.1: Intelligent Item Parsing**
- **File:** `app.py` → `/add-item` endpoint
- **Goal:** Parse natural language text into individual items
- **Input:** `{"text": "I need milk, eggs, and bread"}`
- **Output:** Add three separate items to `grocery_list.txt`
- **Details:** See `claude.md` for parsing strategy
- **Status:** ⏳ To Do
- **Owner:** Claude Code

**Task 1.2: De-duplication**
- **File:** `app.py` → `/add-item` endpoint
- **Goal:** Prevent duplicate items
- **Details:** Check if item exists before adding (case-insensitive)
- **Status:** ⏳ To Do
- **Owner:** Claude Code

**Task 1.3: Frontend Refactor (Optional but Nice)**
- **Files:** Extract CSS and JS from `index.html` into `static/` folder
- **Goal:** Better code organization
- **Status:** ⏳ To Do (lower priority)
- **Owner:** Claude Code

---

### Phase 2: iOS Shortcut Integration (AFTER Phase 1)

**Task 2.1: Test `/add-item` Endpoint**
- Verify parsing works with various message formats
- Verify de-duplication works
- Ensure JSON responses are correct

**Task 2.2: Create iOS Shortcut**
- Create a Shortcut that captures message text
- Send POST request to `http://<ngrok-url>/add-item`
- Test end-to-end with real messages

**Task 2.3: Deploy with ngrok**
- See deployment section below

---

## 🚀 Deployment Architecture

### Local Development (Day-to-Day)

```
Your Machine
├── Flask App (app.py) - localhost:5000
├── templates/index.html
├── static/ (CSS, JS)
└── grocery_list.txt
```

**Start the app:**
```bash
python app.py
```

**Access locally:**
- Web UI: `http://localhost:5000`
- API: `http://localhost:5000/get-items`

---

### Public Access (iOS Shortcuts)

When you need iOS Shortcuts to work:

```bash
# Terminal 1: Run your Flask app
python app.py

# Terminal 2: Expose publicly with ngrok
ngrok http 5000
```

**ngrok provides:**
- Public HTTPS URL: `https://abc123.ngrok.io` (changes each time)
- Automatic tunneling to `localhost:5000`
- Free tier is perfect for this

**Use in iOS Shortcut:**
```
POST https://abc123.ngrok.io/add-item
Body: {"text": "raw message text"}
```

---

## 📁 Final Project Structure

```
smart-grocery-list/
├── app.py                    # Flask backend (main file)
├── requirements.txt          # Python dependencies (just Flask)
├── claude.md                 # Development instructions for Claude Code
├── grocery_list.txt          # Database (auto-created on first run)
├── templates/
│   └── index.html            # Web UI (HTML + optional inline CSS/JS, or split)
├── static/                   # (Optional, if refactored)
│   ├── style.css             # CSS (optional)
│   └── script.js             # JavaScript (optional)
└── .gitignore                # Ignore grocery_list.txt (or not, your choice)
```

---

## 🔧 Setup Instructions (For Dev)

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Terminal/Command line
- ngrok account (free, 1 minute signup)

### Step 1: Clone/Download Project

```bash
# Create project directory
mkdir smart-grocery-list
cd smart-grocery-list

# Copy all files here:
# - app.py
# - templates/index.html
# - claude.md
# - requirements.txt (create it)
```

### Step 2: Create `requirements.txt`

```
Flask==2.3.0
```

### Step 3: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Flask
pip install -r requirements.txt
```

### Step 4: Run Flask App

```bash
python app.py
```

Expected output:
```
WARNING in app.run_with_reloader
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

### Step 5: Access the App

- **Web UI:** Open browser to `http://localhost:5000`
- **API Test:** `http://localhost:5000/get-items`

### Step 6: Setup ngrok (For iOS Shortcuts)

1. **Sign up:** Go to https://ngrok.com, create free account
2. **Download:** Get ngrok for your OS
3. **Extract:** Put ngrok executable somewhere accessible
4. **Authenticate:**
   ```bash
   ngrok config add-authtoken <your-token>
   ```
5. **Expose your app:**
   ```bash
   ngrok http 5000
   ```
6. **Get public URL:** ngrok shows it in terminal, e.g., `https://abc123.ngrok.io`

---

## 📝 API Reference

### GET /
- **Purpose:** Serve web UI
- **Response:** HTML page (templates/index.html)

### GET /get-items
- **Purpose:** Fetch current grocery list
- **Response:** 
  ```json
  ["Milk", "Eggs", "Bread"]
  ```

### POST /add-item
- **Purpose:** Add items from iOS Shortcut
- **Request:**
  ```json
  {"text": "I need milk, eggs, and bread"}
  ```
- **Response:**
  ```json
  {"status": "success", "added": ["Milk", "Eggs", "Bread"]}
  ```
- **Error Handling:** Returns 400 if JSON invalid, 500 if file write fails

### POST /delete-item
- **Purpose:** Delete item via web UI
- **Request:**
  ```json
  {"item": "Milk"}
  ```
- **Response:**
  ```json
  {"status": "success"}
  ```

---

## 🧪 Testing Checklist

Before considering Phase 1 complete:

- [ ] Add simple item: "milk" → appears as "Milk"
- [ ] Add multiple items: "milk, eggs, bread" → all three separate
- [ ] Natural language: "I need milk and eggs" → extracts both
- [ ] De-duplicate: Add "milk" twice → only one "Milk" in list
- [ ] Delete item: Click in web UI, item removed
- [ ] Refresh page: Items persist
- [ ] API works: Test `/get-items` in browser

Before iOS integration:

- [ ] ngrok running and public URL working
- [ ] iOS Shortcut can POST to ngrok URL
- [ ] Message text extracts correctly
- [ ] Items appear in web UI
- [ ] No duplicates on repeated messages

---

## 🔄 Development Workflow

### For Claude Code Usage

```bash
# Terminal: Start your Flask app
python app.py

# Claude Code: Point it at your project
claude

# Ask Claude Code to:
# 1. "Add intelligent parsing to /add-item endpoint"
# 2. "Add de-duplication logic"
# 3. "Refactor frontend into separate CSS/JS files"
```

Claude Code will reference `claude.md` for context and make changes to your files.

### For Testing Changes

1. Make a change (or let Claude Code make it)
2. Save the file
3. Flask auto-reloads (if running in debug mode)
4. Test in browser or with API call
5. Fix any issues

---

## 💡 Important Notes

### On `grocery_list.txt`

- **Auto-created:** If it doesn't exist, Flask creates it on first `/add-item` call
- **Manual seeding:** Can pre-populate with items (one per line)
- **Backup:** It's just a text file—easy to backup or version control
- **Persistence:** Survives app restarts (data is in the file, not in memory)

### On ngrok URLs

- **Temporary:** Each time you run `ngrok http 5000`, you get a new URL
- **Not permanent:** Don't share the URL publicly (it's meant for testing)
- **Pro accounts:** Can get static URLs if you pay ($5+/month), but free is fine for this
- **iOS Shortcut:** Update the URL in the Shortcut whenever ngrok restarts

### On Security

- **Local only:** Your grocery list never leaves your machine (unless using ngrok URL)
- **No authentication:** App has no login (assumes personal use only)
- **HTTPS with ngrok:** Public URL is encrypted (ngrok handles this)

---

## 🛠️ Troubleshooting

### Flask app won't start
```bash
# Check if port 5000 is already in use
# On macOS/Linux:
lsof -i :5000

# Kill the process or use a different port:
python app.py --port 5001
```

### Changes aren't showing up
```bash
# Restart Flask (it auto-reloads in debug mode, but sometimes needs manual restart)
# Press CTRL+C in Flask terminal and run again:
python app.py
```

### ngrok URL not working in iOS Shortcut
- Check ngrok is running in terminal (you should see `https://xxx.ngrok.io`)
- Verify URL is correct in Shortcut
- Test URL in browser first
- Make sure your Flask app is running (Terminal 1)

### Items not persisting after restart
- Check `grocery_list.txt` exists in project directory
- If missing, Flask will create it on next `/add-item` call
- Look for error messages in Flask terminal

### Parse errors on `/add-item`
- Verify Shortcut is sending valid JSON
- Check Flask terminal for error messages
- Test with curl:
  ```bash
  curl -X POST http://localhost:5000/add-item \
    -H "Content-Type: application/json" \
    -d '{"text": "milk and eggs"}'
  ```

---

## 📊 Cost Summary

| Service | Cost | Used For |
|---------|------|----------|
| ngrok (free tier) | $0 | Public URL for iOS Shortcuts |
| Flask | $0 | Backend framework (open source) |
| Your machine | ??? | Running the app (you pay for electricity) |
| **Total** | **$0** | ✅ Completely free |

---

## 🎯 Success Criteria

When this project is "done":

1. ✅ Flask app runs locally without errors
2. ✅ Web UI shows grocery list
3. ✅ Can delete items from web UI
4. ✅ Intelligent parsing works (natural language → individual items)
5. ✅ De-duplication prevents duplicates
6. ✅ iOS Shortcut can send messages to `/add-item`
7. ✅ Items appear in list after iOS Shortcut sends them
8. ✅ No duplicates from repeated messages

---

## 📞 Next Steps

1. **Set up your local environment** (Python, Flask, virtual env)
2. **Create your `app.py`, `index.html`, and `requirements.txt`**
3. **Test locally** (make sure `/get-items` returns JSON)
4. **Use Claude Code to implement Phase 1 features** (parsing + de-duplication)
5. **Sign up for ngrok** (takes 1 minute)
6. **Create iOS Shortcut** (uses ngrok public URL)
7. **Test end-to-end**

---

## 📚 Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **ngrok Documentation:** https://ngrok.com/docs
- **iOS Shortcuts Guide:** https://support.apple.com/guide/shortcuts/
- **Claude Code:** Use `claude` command in your terminal after setup

---

## 👥 Team Notes

**For the Developer:**
- Use `claude.md` to guide Claude Code
- Follow the testing checklist before declaring tasks "done"
- Refer to this document for architecture and deployment info
- Ask questions in `claude.md` if unclear about requirements

**For the Product Owner (You):**
- This is a personal tool, so you get full control
- No ongoing costs (completely free)
- Your data stays on your machine
- iOS integration is simple (just a Shortcut forwarding messages)

---

## 🚀 Let's Build This!

You have everything you need:
- A clear architecture
- A development guide (`claude.md`)
- A deployment strategy (ngrok)
- A testing plan
- Zero costs

Get your dev to read this, set up their local environment, and start with Claude Code. Happy building! 🛒

---

**Last Updated:** October 30, 2025  
**Status:** Ready for Development  
**Deployment Target:** Local + ngrok for iOS Shortcuts
