# Smart Grocery List v2 - Specification Summary

## 📋 Overview

Complete redesign of the grocery list application with enhanced UX, shopping trip tracking, categorization, and purchase history.

---

## 🎯 Key Changes from v1

### What's New
1. **Prominent Input Field** - Immediately visible, can't miss it
2. **Auto-Categorization** - Items grouped by type (Produce, Dairy, etc.)
3. **Non-Destructive Checking** - Check items off without deleting them
4. **Shopping Trip Tracking** - Complete trips and maintain history
5. **Purchase History** - See when you last bought each item
6. **4-Week History** - Track multiple shopping trips per week
7. **Smart Insights** - "Last bought 7 days ago", frequency tracking
8. **Copy from Last Trip** - Quick add recurring items

### What's Changed
- **Data Storage:** Plain text → Structured JSON
- **Item Interaction:** Click to delete → Check to mark bought
- **List Structure:** Flat list → Categorized sections
- **Data Model:** Simple items → Items with metadata (dates, stats)

---

## 📁 Specification Files

### 1. requirements.md
**15 Requirements** covering:
- Enhanced input field visibility
- Item categorization (10 categories)
- Non-destructive checking (strike-through)
- Shopping trip management
- Purchase history tracking
- Item statistics and insights
- Data persistence (JSON)
- Enhanced AI parsing
- Mobile-first responsive design

### 2. design.md
**Technical Design** including:
- Architecture diagrams
- Data models (GroceryItem, ShoppingTrip, ItemStats)
- API endpoints (7 new/updated)
- Category system (10 categories with emojis)
- AI integration (enhanced Gemini prompt)
- Data flow diagrams
- Error handling strategies
- Performance optimization
- Migration plan (v1 → v2)
- UI/UX specifications

### 3. tasks.md
**9 Major Tasks** with **50+ Subtasks**:
1. Data Layer Foundation (4 subtasks)
2. Category System (4 subtasks)
3. Enhanced API Endpoints (8 subtasks)
4. Statistics and Insights (3 subtasks)
5. Frontend UI Redesign (9 subtasks)
6. Frontend JavaScript Logic (6 subtasks)
7. CSS Styling Updates (7 subtasks)
8. Testing and QA (7 subtasks)
9. Documentation and Polish (4 subtasks)

---

## 🏗️ Architecture Overview

```
Frontend (Browser)
    ↓ REST API
Flask Backend
    ↓ Gemini AI
Google Gemini 2.5 Flash
    ↓ JSON Storage
grocery_data.json
```

### Data Structure
```json
{
  "version": "2.0",
  "current": {
    "date": "2025-10-30",
    "items": [...]
  },
  "history": [
    {"date": "2025-10-23", "items": [...]},
    {"date": "2025-10-20", "items": [...]}
  ],
  "itemStats": {
    "Apples": {
      "lastBought": "2025-10-23",
      "totalPurchases": 15,
      "averageFrequency": 7
    }
  }
}
```

---

## 🎨 User Experience Flow

### Adding Items
```
1. User sees PROMINENT input field
2. Types: "milk, eggs, bread"
3. AI extracts and categorizes items
4. Items appear in categorized sections
5. Shows "Last bought: 7 days ago" if applicable
```

### Shopping
```
1. User goes to store with list
2. Taps checkbox as items are bought
3. Item strikes through (not deleted)
4. Can untap if mistake
5. Clicks "Complete Shopping Trip" when done
6. List moves to history, new list starts
```

### Viewing History
```
1. User expands History section
2. Sees last 4 weeks of trips
3. Each trip shows date and items
4. Can copy items from previous trip
```

---

## 📊 Key Features

### 1. Categories (10 Total)
- 🍎 Produce
- 🥛 Dairy
- 🥩 Meat & Seafood
- 🍞 Bakery
- 🥫 Pantry
- 🧊 Frozen
- 🧴 Household
- 🍫 Snacks
- 🥤 Beverages
- 📦 Other

### 2. Item Metadata
- Name (e.g., "Apples")
- Category (e.g., "Produce")
- Checked status (true/false)
- Added timestamp
- Checked timestamp
- Last bought date
- Purchase frequency

### 3. Shopping Trip Data
- Trip ID
- Completion date
- List of items (with checked status)
- Total items count
- Checked items count

### 4. Statistics
- Last bought date
- Total purchases
- Average frequency (days)
- Frequency label ("Weekly", "Every 3 days")

---

## 🔌 API Endpoints

### New/Updated Endpoints
1. **POST /add-item** - Enhanced with category detection
2. **GET /get-current-list** - Returns categorized items with metadata
3. **POST /toggle-item** - Check/uncheck items
4. **POST /complete-trip** - Archive current list, start fresh
5. **GET /get-history** - Return last 4 weeks of trips
6. **POST /copy-from-last-trip** - Copy items from previous trip
7. **DELETE /delete-item** - Updated for new data structure

---

## ⏱️ Implementation Timeline

### Estimated Effort: 24-33 hours

**Week 1 (8-10 hours):**
- Data layer and JSON storage
- Category system
- Core API endpoints

**Week 2 (8-10 hours):**
- Remaining API endpoints
- Statistics calculation
- Core UI redesign

**Week 3 (8-10 hours):**
- Advanced UI features
- Frontend logic
- CSS styling

**Week 4 (3-5 hours):**
- Testing and QA
- Documentation
- Final polish

---

## ✅ Success Criteria

### Must Work
1. ✅ Input field is prominent and obvious
2. ✅ Items auto-categorize correctly (95%+ accuracy)
3. ✅ Checking items applies strike-through (no deletion)
4. ✅ Can complete shopping trips
5. ✅ History shows last 4 weeks
6. ✅ "Last bought" displays correctly
7. ✅ Mobile experience is smooth
8. ✅ Data persists without loss
9. ✅ Migration from v1 works
10. ✅ Performance targets met

### Performance Targets
- Add item: < 2 seconds (including AI)
- Toggle item: < 100ms
- Complete trip: < 500ms
- Load current list: < 300ms
- Load history: < 500ms

---

## 🎯 User Requirements Alignment

### Your Specific Needs
✅ **Shop couple times a week** - Supported with trip tracking  
✅ **Track when items ordered** - "Last bought" feature  
✅ **4 weeks history** - Automatic pruning  
✅ **Manual complete trip** - Dedicated button  
✅ **Don't override previous days** - Each trip is separate  
✅ **Weekly apples tracking** - Shows frequency and last bought  

---

## 🚀 Next Steps

### To Start Implementation:

1. **Review Spec Files**
   - Read requirements.md
   - Review design.md
   - Understand tasks.md

2. **Begin with Task 1**
   - Start with data layer
   - Build foundation first
   - Test as you go

3. **Follow Task Order**
   - Complete tasks sequentially
   - Don't skip ahead
   - Mark tasks complete as you finish

4. **Test Continuously**
   - Test each feature as built
   - Don't wait until end
   - Fix bugs immediately

---

## 📚 Documentation Structure

```
.kiro/specs/grocery-list-v2/
├── requirements.md       ← 15 requirements with acceptance criteria
├── design.md            ← Technical design and architecture
├── tasks.md             ← 50+ implementation tasks
└── SPEC_SUMMARY.md      ← This file
```

---

## 🎨 Visual Preview

### Before (v1)
```
┌─────────────────────┐
│  Grocery List       │
│                     │
│  Milk               │
│  Eggs               │
│  Bread              │
│                     │
│  [input box]        │
└─────────────────────┘
```

### After (v2)
```
┌─────────────────────────────┐
│  🛒 Grocery List            │
│                             │
│  ┌───────────────────────┐ │
│  │ 🔍 Add items...  [Add]│ │  ← PROMINENT
│  └───────────────────────┘ │
│                             │
│  📅 Current List (Oct 30)  │
│  ─────────────────────────  │
│  🍎 Produce                 │
│  ☐ Apples                   │
│     💡 Last bought: 7 days  │
│                             │
│  🥛 Dairy                   │
│  ☑̶ M̶i̶l̶k̶  (checked)          │
│  ☐ Eggs                     │
│                             │
│  [✓ Complete Trip]         │
│                             │
│  📜 History ▼               │
│  📅 Oct 23 (7 days ago)    │
│  ☑̶ A̶p̶p̶l̶e̶s̶, ☑̶ M̶i̶l̶k̶            │
└─────────────────────────────┘
```

---

## 💡 Key Insights

### Why This Design?
1. **Prominent Input** - Users know where to start
2. **Categories** - Matches how stores are organized
3. **Strike-through** - Non-destructive, can undo
4. **Trip Tracking** - Matches real shopping behavior (2x/week)
5. **History** - Learn patterns, reorder easily
6. **4 Weeks** - Balance between useful history and clutter

### Design Decisions
- **JSON over Database** - Simpler, sufficient for personal use
- **Gemini for Categories** - More accurate than keyword matching
- **Manual Trip Completion** - User controls when trip ends
- **4 Week Limit** - Prevents data bloat, keeps relevant
- **Mobile-First** - Primary use case is in-store shopping

---

## 🎓 What You'll Learn

This project demonstrates:
- Advanced Flask API design
- AI integration (Gemini)
- Complex data modeling
- State management
- Mobile-first UX
- Performance optimization
- Data migration strategies

---

## ✨ Summary

**From:** Simple text list with AI parsing  
**To:** Full-featured shopping trip tracker with categories, history, and insights

**Effort:** 24-33 hours over 3-4 weeks  
**Complexity:** Medium (structured data, multiple features)  
**Value:** High (matches real shopping behavior)

---

**Ready to implement?** Start with Task 1.1 in tasks.md! 🚀

---

**Document Version:** 1.0  
**Created:** 2025-10-30  
**Status:** ✅ Complete and Ready
