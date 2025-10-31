# 🚀 Quick Start Guide

## Step 1: Start the Flask App

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Open your browser to `http://localhost:5000` to see the app!

## Step 2: Test the Web Interface

1. Type "milk, eggs, bread" in the input box
2. Click "Add"
3. Watch as Gemini AI extracts the items
4. Click any item to delete it

## Step 3: Set Up ngrok (for iOS)

Open a **new terminal** and run:

```bash
ngrok http 5000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

## Step 4: Create iOS Shortcut

1. Open **Shortcuts** app on iPhone
2. Tap **+** to create new shortcut
3. Name it: "Add to Grocery List"
4. Add these actions:

### Action 1: Receive Input
- Type: Text
- From: Share Sheet

### Action 2: Get Contents of URL
- URL: `https://YOUR_NGROK_URL.ngrok.io/add-item`
- Method: **POST**
- Request Body: **JSON**
- Add Header:
  - Key: `Content-Type`
  - Value: `application/json`
- JSON Body:
```json
{
  "text": "[Shortcut Input]"
}
```

### Action 3: Show Notification (optional)
- Title: "Added to Grocery List"
- Body: "Items processed"

5. Save the shortcut

## Step 5: Test iOS Integration

1. Open Messages or Notes on your iPhone
2. Find a message like "We need milk and eggs"
3. Tap **Share** → **Add to Grocery List**
4. Check your web UI - items should appear!

## Testing Examples

Try these natural language inputs:

- "milk, eggs, bread"
- "We need milk and eggs"
- "Can you grab 2 gallons of milk?"
- "I'm out of cheddar cheese"
- "Get stuff for tacos - ground beef, tortillas, cheese"

The AI will extract the grocery items automatically!

## Troubleshooting

### App won't start
- Check if port 5000 is already in use
- Make sure `.env` has `GEMINI_API_KEY`

### iOS Shortcut not working
- Make sure both Flask and ngrok are running
- Check the ngrok URL is correct in the shortcut
- Verify the JSON format is correct

### Items not appearing
- Check the browser console for errors
- Verify Gemini API key is valid
- Try the fallback parser by testing with simple text

## Next Steps

- Customize the UI colors in `static/style.css`
- Adjust the Gemini prompt in `app.py` for better parsing
- Add more features like categories or quantities

Enjoy your smart grocery list! 🛒
