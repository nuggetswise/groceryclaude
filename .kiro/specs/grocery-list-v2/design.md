# Design Document - Smart Grocery List v2

## Overview

This document outlines the technical design for the enhanced Smart Grocery List application with shopping trip tracking, categorization, and purchase history features.

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  UI Components                                   │   │
│  │  - Input Field (Prominent)                       │   │
│  │  - Current List (Categorized)                    │   │
│  │  - History Section (Collapsible)                 │   │
│  │  - Complete Trip Button                          │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↕ REST API                       │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                   Flask Backend (Python)                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  API Routes                                      │   │
│  │  - /add-item (with category detection)          │   │
│  │  - /toggle-item (check/uncheck)                 │   │
│  │  - /delete-item                                  │   │
│  │  - /complete-trip                                │   │
│  │  - /get-current-list                             │   │
│  │  - /get-history                                  │   │
│  │  - /copy-from-last-trip                          │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↕                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Business Logic                                  │   │
│  │  - AI Parsing (Gemini)                           │   │
│  │  - Category Assignment                           │   │
│  │  - Statistics Calculation                        │   │
│  │  - History Management                            │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↕                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Data Layer                                      │   │
│  │  - JSON File Operations                          │   │
│  │  - Data Validation                               │   │
│  │  - Migration from v1                             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│              Data Storage (grocery_data.json)            │
│  {                                                       │
│    "current": {...},                                     │
│    "history": [...],                                     │
│    "itemStats": {...}                                    │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                  External Services                       │
│  - Google Gemini AI API (parsing + categorization)      │
└─────────────────────────────────────────────────────────┘
```

---

## Components and Interfaces

### 1. Data Models

#### GroceryItem
```python
{
    "id": "uuid-string",
    "name": "Apples",
    "category": "Produce",
    "checked": false,
    "addedAt": "2025-10-30T10:00:00Z",
    "checkedAt": null  # timestamp when checked
}
```

#### CurrentList
```python
{
    "date": "2025-10-30",
    "items": [GroceryItem, ...]
}
```

#### ShoppingTrip
```python
{
    "id": "uuid-string",
    "date": "2025-10-23",
    "completedAt": "2025-10-23T15:30:00Z",
    "items": [GroceryItem, ...],
    "totalItems": 5,
    "checkedItems": 5
}
```

#### ItemStats
```python
{
    "Apples": {
        "lastBought": "2025-10-23",
        "totalPurchases": 15,
        "averageFrequency": 7,  # days
        "category": "Produce"
    }
}
```

#### GroceryData (Root)
```python
{
    "version": "2.0",
    "current": CurrentList,
    "history": [ShoppingTrip, ...],  # max 4 weeks
    "itemStats": ItemStats
}
```

---

### 2. Category System

#### Predefined Categories
```python
CATEGORIES = {
    "Produce": {
        "emoji": "🍎",
        "keywords": ["fruit", "vegetable", "apple", "banana", "lettuce", "tomato"],
        "order": 1
    },
    "Dairy": {
        "emoji": "🥛",
        "keywords": ["milk", "cheese", "yogurt", "butter", "cream"],
        "order": 2
    },
    "Meat & Seafood": {
        "emoji": "🥩",
        "keywords": ["beef", "chicken", "pork", "fish", "salmon", "shrimp"],
        "order": 3
    },
    "Bakery": {
        "emoji": "🍞",
        "keywords": ["bread", "bagel", "croissant", "muffin", "pastry"],
        "order": 4
    },
    "Pantry": {
        "emoji": "🥫",
        "keywords": ["pasta", "rice", "beans", "sauce", "oil", "flour"],
        "order": 5
    },
    "Frozen": {
        "emoji": "🧊",
        "keywords": ["frozen", "ice cream", "pizza"],
        "order": 6
    },
    "Household": {
        "emoji": "🧴",
        "keywords": ["soap", "detergent", "paper towels", "cleaner"],
        "order": 7
    },
    "Snacks": {
        "emoji": "🍫",
        "keywords": ["chips", "cookies", "candy", "popcorn"],
        "order": 8
    },
    "Beverages": {
        "emoji": "🥤",
        "keywords": ["juice", "soda", "coffee", "tea", "water"],
        "order": 9
    },
    "Other": {
        "emoji": "📦",
        "keywords": [],
        "order": 10
    }
}
```

---

### 3. API Endpoints

#### POST /add-item
**Request:**
```json
{
    "text": "We need milk, eggs, and bread"
}
```

**Response:**
```json
{
    "success": true,
    "added": [
        {
            "name": "Milk",
            "category": "Dairy",
            "lastBought": "2025-10-23",
            "daysSinceLastBought": 7
        },
        {
            "name": "Eggs",
            "category": "Dairy",
            "lastBought": null,
            "daysSinceLastBought": null
        },
        {
            "name": "Bread",
            "category": "Bakery",
            "lastBought": "2025-10-20",
            "daysSinceLastBought": 10
        }
    ],
    "skipped": [],
    "total": 15
}
```

#### GET /get-current-list
**Response:**
```json
{
    "date": "2025-10-30",
    "categories": {
        "Produce": [
            {
                "id": "uuid-1",
                "name": "Apples",
                "checked": false,
                "addedAt": "2025-10-30T10:00:00Z",
                "lastBought": "2025-10-23",
                "daysSinceLastBought": 7,
                "frequency": "Weekly"
            }
        ],
        "Dairy": [...]
    },
    "totalItems": 15,
    "checkedItems": 3
}
```

#### POST /toggle-item
**Request:**
```json
{
    "itemId": "uuid-1"
}
```

**Response:**
```json
{
    "success": true,
    "itemId": "uuid-1",
    "checked": true,
    "checkedAt": "2025-10-30T14:30:00Z"
}
```

#### POST /complete-trip
**Request:**
```json
{}
```

**Response:**
```json
{
    "success": true,
    "trip": {
        "id": "trip-uuid",
        "date": "2025-10-30",
        "completedAt": "2025-10-30T15:00:00Z",
        "totalItems": 15,
        "checkedItems": 12
    },
    "message": "Shopping trip completed! 12 items archived."
}
```

#### GET /get-history
**Response:**
```json
{
    "trips": [
        {
            "id": "trip-uuid-1",
            "date": "2025-10-23",
            "completedAt": "2025-10-23T15:30:00Z",
            "daysAgo": 7,
            "totalItems": 10,
            "checkedItems": 10,
            "items": [...]
        },
        {
            "id": "trip-uuid-2",
            "date": "2025-10-20",
            "completedAt": "2025-10-20T16:00:00Z",
            "daysAgo": 10,
            "totalItems": 8,
            "checkedItems": 7,
            "items": [...]
        }
    ],
    "totalTrips": 2
}
```

#### POST /copy-from-last-trip
**Response:**
```json
{
    "success": true,
    "copied": 8,
    "skipped": 2,
    "items": [...]
}
```

---

## AI Integration Design

### Enhanced Gemini Prompt

```python
def parse_with_category(raw_text: str) -> list[dict]:
    """Parse text and assign categories using Gemini."""
    
    prompt = f"""Extract grocery items from this text and assign categories.

Text: "{raw_text}"

Categories: Produce, Dairy, Meat & Seafood, Bakery, Pantry, Frozen, Household, Snacks, Beverages, Other

Rules:
- Extract ONLY grocery item names
- Remove quantities, measurements, filler words
- Assign the most appropriate category
- Return as JSON array

Format:
[
  {{"name": "Milk", "category": "Dairy"}},
  {{"name": "Apples", "category": "Produce"}}
]

Examples:
Input: "We need 2 gallons of milk and a dozen eggs"
Output: [
  {{"name": "Milk", "category": "Dairy"}},
  {{"name": "Eggs", "category": "Dairy"}}
]

Input: "Get stuff for tacos - ground beef, tortillas, cheese"
Output: [
  {{"name": "Ground Beef", "category": "Meat & Seafood"}},
  {{"name": "Tortillas", "category": "Bakery"}},
  {{"name": "Cheese", "category": "Dairy"}}
]

Now extract from: "{raw_text}"
"""
    
    response = model.generate_content(prompt)
    return parse_json_response(response.text)
```

---

## Data Flow Diagrams

### Adding Items Flow
```
User Input
    ↓
"milk, eggs, bread"
    ↓
POST /add-item
    ↓
Gemini AI Parsing
    ↓
[{name: "Milk", category: "Dairy"}, ...]
    ↓
Check Item Stats (last bought)
    ↓
Check for Duplicates
    ↓
Add to Current List
    ↓
Save to grocery_data.json
    ↓
Return Response with Metadata
    ↓
Frontend Updates UI (Categorized)
```

### Completing Trip Flow
```
User Clicks "Complete Trip"
    ↓
POST /complete-trip
    ↓
Create ShoppingTrip object
    ↓
Move Current List to History
    ↓
Update Item Stats (last bought, frequency)
    ↓
Clean History (keep only 4 weeks)
    ↓
Create New Empty Current List
    ↓
Save to grocery_data.json
    ↓
Return Trip Summary
    ↓
Frontend Shows Confirmation
```

### Toggle Item Flow
```
User Clicks Checkbox
    ↓
POST /toggle-item
    ↓
Find Item by ID
    ↓
Toggle checked state
    ↓
Update checkedAt timestamp
    ↓
Save to grocery_data.json
    ↓
Return New State
    ↓
Frontend Updates UI (Strike-through)
```

---

## Error Handling

### API Errors
```python
ERROR_CODES = {
    400: "Bad Request - Invalid input",
    404: "Not Found - Item/Trip not found",
    500: "Internal Server Error - AI/Storage failure",
    503: "Service Unavailable - Gemini API down"
}
```

### Fallback Strategies
1. **Gemini API Failure:** Use simple regex parsing + keyword-based categorization
2. **JSON Corruption:** Restore from backup, or initialize fresh
3. **Category Detection Failure:** Default to "Other" category
4. **History Overflow:** Auto-prune trips older than 4 weeks

---

## Testing Strategy

### Unit Tests
- Data model validation
- Category assignment logic
- Statistics calculation
- Date/time utilities
- JSON serialization/deserialization

### Integration Tests
- API endpoint responses
- Gemini AI integration
- File I/O operations
- History management
- Migration from v1 to v2

### Manual Tests
- Add items with various inputs
- Check/uncheck items
- Complete shopping trips
- View history
- Copy from last trip
- Mobile responsiveness
- Category accuracy

---

## Performance Considerations

### Optimization Strategies
1. **Caching:** Cache item stats in memory, refresh on trip completion
2. **Lazy Loading:** Load history only when expanded
3. **Debouncing:** Debounce rapid checkbox toggles (300ms)
4. **Batch Operations:** Batch multiple item additions in single AI call
5. **Index Optimization:** Use item ID for O(1) lookups

### Performance Targets
- Add item: < 2s (including AI)
- Toggle item: < 100ms
- Complete trip: < 500ms
- Load current list: < 300ms
- Load history: < 500ms

---

## Security Considerations

1. **API Key Protection:** Store Gemini API key in .env, never expose to frontend
2. **Input Validation:** Sanitize all user inputs before processing
3. **XSS Prevention:** Escape HTML in item names
4. **Rate Limiting:** Limit API calls to prevent abuse (60/min for Gemini free tier)
5. **Data Backup:** Periodic backups of grocery_data.json

---

## Migration Strategy (v1 → v2)

### Migration Function
```python
def migrate_v1_to_v2():
    """Migrate from grocery_list.txt to grocery_data.json"""
    
    # Read old format
    old_items = read_grocery_list_txt()
    
    # Create new structure
    new_data = {
        "version": "2.0",
        "current": {
            "date": today(),
            "items": []
        },
        "history": [],
        "itemStats": {}
    }
    
    # Convert items
    for item_name in old_items:
        category = detect_category_fallback(item_name)
        new_item = {
            "id": generate_uuid(),
            "name": item_name,
            "category": category,
            "checked": False,
            "addedAt": now(),
            "checkedAt": None
        }
        new_data["current"]["items"].append(new_item)
    
    # Save new format
    save_grocery_data(new_data)
    
    # Backup old format
    backup_file("grocery_list.txt")
```

---

## UI/UX Design Specifications

### Visual Hierarchy
```
┌─────────────────────────────────────┐
│  🛒 Grocery List                    │  ← Header (fixed)
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 🔍 Add items...          [Add]│ │  ← Input (prominent, 60px)
│  └───────────────────────────────┘ │
│                                     │
│  📅 Current List (Oct 30)          │  ← Section header
│  ─────────────────────────────────  │
│                                     │
│  🍎 Produce                         │  ← Category (collapsible)
│  ☐ Apples                           │
│     💡 Last bought: 7 days ago      │  ← Metadata (subtle)
│  ☐ Bananas                          │
│                                     │
│  🥛 Dairy                           │
│  ☑̶ M̶i̶l̶k̶                             │  ← Checked (strike-through)
│  ☐ Eggs                             │
│                                     │
│  [✓ Complete Shopping Trip]        │  ← Action button
│                                     │
│  ─────────────────────────────────  │
│  📜 History ▼                       │  ← Collapsible section
│                                     │
│  📅 Oct 23 (7 days ago)            │
│  ☑̶ A̶p̶p̶l̶e̶s̶, ☑̶ M̶i̶l̶k̶, ☑̶ E̶g̶g̶s̶          │
│  [Copy to Current List]            │
│                                     │
│  📅 Oct 20 (10 days ago)           │
│  ☑̶ B̶a̶n̶a̶n̶a̶s̶, ☑̶ B̶r̶e̶a̶d̶                │
└─────────────────────────────────────┘
```

### Color Scheme
```css
--primary: #4f46e5;        /* Indigo */
--success: #10b981;        /* Green */
--danger: #ef4444;         /* Red */
--warning: #f59e0b;        /* Amber */
--bg: #f8fafc;             /* Light gray */
--surface: #ffffff;        /* White */
--text: #1e293b;           /* Dark gray */
--text-light: #64748b;     /* Medium gray */
--border: #e2e8f0;         /* Light border */
--checked: #94a3b8;        /* Muted for checked items */
```

### Typography
```css
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
--font-size-xl: 2rem;      /* Headers */
--font-size-lg: 1.25rem;   /* Category headers */
--font-size-base: 1rem;    /* Items */
--font-size-sm: 0.875rem;  /* Metadata */
```

---

## Implementation Phases

### Phase 1: Data Layer (2-3 hours)
- Create new data models
- Implement JSON storage
- Build migration from v1
- Add data validation

### Phase 2: Backend API (3-4 hours)
- Update existing endpoints
- Add new endpoints (toggle, complete-trip, history)
- Enhance Gemini prompt for categories
- Implement statistics calculation

### Phase 3: Frontend UI (4-5 hours)
- Redesign input field (prominent)
- Implement categorized list view
- Add checkbox toggle (strike-through)
- Build history section
- Add "Complete Trip" button

### Phase 4: Testing & Polish (2-3 hours)
- Test all user flows
- Mobile responsiveness
- Performance optimization
- Bug fixes

**Total Estimated Time:** 11-15 hours

---

## Success Criteria

1. ✅ Input field is immediately visible and prominent
2. ✅ Items are automatically categorized
3. ✅ Checking items applies strike-through (no deletion)
4. ✅ Shopping trips can be completed and archived
5. ✅ History shows last 4 weeks of trips
6. ✅ "Last bought" information displays correctly
7. ✅ All API endpoints respond within performance targets
8. ✅ Mobile experience is smooth and intuitive
9. ✅ Data persists correctly across sessions
10. ✅ Migration from v1 works without data loss

---

**Document Version:** 1.0  
**Created:** 2025-10-30  
**Status:** ✅ Ready for Implementation
