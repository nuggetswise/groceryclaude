# 🛒 Smart Grocery List v2

A modern, intelligent grocery list app with shopping trip tracking and AI-powered categorization. Uses Google Gemini AI to automatically organize your grocery items into categories.

## Features

- 🧠 **AI Categorization**: Automatically sorts items into 10 categories (🍎 Produce, 🥛 Dairy, etc.)
- ✅ **Shopping Trip Tracking**: Complete trips and maintain 4 weeks of history
- 📋 **Checkbox Toggle**: Check items off without deleting them
- 🔄 **Copy from Last Trip**: Quickly reuse items from previous shopping
- 📊 **Purchase Statistics**: Track when you last bought each item
- 🎨 **Modern UI**: Beautiful, mobile-friendly interface
- 💾 **JSON Storage**: Structured data with automatic backups

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Your `.env` file should contain:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. Run the App

```bash
python app.py
```

The app will start on `http://localhost:5000`

### 4. Set Up ngrok (for iOS)

In a separate terminal:
```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 5. Create iOS Shortcut

1. Open iOS Shortcuts app
2. Create new shortcut: "Add to Grocery List"
3. Add action: "Get Contents of URL"
   - URL: `https://YOUR_NGROK_URL.ngrok.io/add-item`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Request Body: `{"text": "[Shortcut Input]"}`
4. Share any text to this shortcut to add items!

## Usage

### Web Interface

- **Add items**: Type in the input box (e.g., "milk, eggs, bread")
- **Delete items**: Click on any item to remove it
- **Clear all**: Click the "Clear All" button

### iOS Shortcuts

Share any message containing grocery items:
- "We need milk and eggs"
- "Can you grab 2 gallons of milk?"
- "I'm out of cheddar cheese"

The AI will extract the items and add them to your list!

## How It Works

1. **Input**: Text from web UI or iOS Shortcut
2. **Parsing**: Gemini AI extracts grocery items
3. **Deduplication**: Checks for existing items (case-insensitive)
4. **Storage**: Saves to `grocery_list.txt`
5. **Display**: Updates web UI automatically

## Tech Stack

- **Backend**: Python 3.9+, Flask
- **AI**: Google Gemini API
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Storage**: Plain text file
- **Tunnel**: ngrok for iOS access

## Project Structure

```
groceryclaude/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env                   # API keys
├── grocery_list.txt       # Data storage (auto-created)
├── templates/
│   └── index.html         # Web UI
└── static/
    ├── style.css          # Styles
    └── script.js          # Frontend logic
```

## API Endpoints

- `GET /` - Web interface
- `GET /get-items` - Get all items (JSON)
- `POST /add-item` - Add items from text
- `POST /delete-item` - Delete an item
- `POST /clear-all` - Clear all items

## Tips

- The AI is smart! Try natural language like "get stuff for tacos"
- Items are automatically deduplicated (case-insensitive)
- The web UI auto-refreshes every 30 seconds
- Use ngrok for reliable iOS access from anywhere

## License

Personal use project - feel free to modify and adapt!
