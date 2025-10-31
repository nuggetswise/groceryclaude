import os
import json
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
GROCERY_FILE = 'grocery_list.txt'  # v1 file (for migration)
GROCERY_DATA_FILE = 'grocery_data.json'  # v2 file

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# Use Gemini 2.5 Flash model
model = genai.GenerativeModel('gemini-2.5-flash')


# ==================== CATEGORY CONFIGURATION ====================

CATEGORIES = {
    "Produce": {
        "emoji": "🍎",
        "keywords": ["fruit", "vegetable", "apple", "banana", "lettuce", "tomato", "carrot", "onion", "potato", "orange", "grape", "berry", "melon", "pepper", "cucumber", "spinach", "broccoli", "celery"],
        "order": 1
    },
    "Dairy": {
        "emoji": "🥛",
        "keywords": ["milk", "cheese", "yogurt", "butter", "cream", "sour cream", "cottage cheese", "cheddar", "mozzarella", "parmesan"],
        "order": 2
    },
    "Meat & Seafood": {
        "emoji": "🥩",
        "keywords": ["beef", "chicken", "pork", "fish", "salmon", "shrimp", "turkey", "bacon", "sausage", "ham", "steak", "ground beef", "tuna", "cod"],
        "order": 3
    },
    "Bakery": {
        "emoji": "🍞",
        "keywords": ["bread", "bagel", "croissant", "muffin", "pastry", "bun", "roll", "tortilla", "pita", "baguette"],
        "order": 4
    },
    "Pantry": {
        "emoji": "🥫",
        "keywords": ["pasta", "rice", "beans", "sauce", "oil", "flour", "sugar", "salt", "pepper", "spice", "cereal", "oatmeal", "can", "jar"],
        "order": 5
    },
    "Frozen": {
        "emoji": "🧊",
        "keywords": ["frozen", "ice cream", "pizza", "frozen vegetables", "frozen fruit", "popsicle", "ice"],
        "order": 6
    },
    "Household": {
        "emoji": "🧴",
        "keywords": ["soap", "detergent", "paper towels", "cleaner", "shampoo", "toothpaste", "toilet paper", "tissue", "dish soap", "laundry"],
        "order": 7
    },
    "Snacks": {
        "emoji": "🍫",
        "keywords": ["chips", "cookies", "candy", "popcorn", "crackers", "nuts", "chocolate", "pretzels", "granola"],
        "order": 8
    },
    "Beverages": {
        "emoji": "🥤",
        "keywords": ["juice", "soda", "coffee", "tea", "water", "beer", "wine", "drink", "beverage"],
        "order": 9
    },
    "Other": {
        "emoji": "📦",
        "keywords": [],
        "order": 10
    }
}


# ==================== DATA MODELS ====================

@dataclass
class GroceryItem:
    """Represents a single grocery item."""
    id: str
    name: str
    category: str
    checked: bool = False
    addedAt: str = None
    checkedAt: Optional[str] = None
    
    def __post_init__(self):
        if self.addedAt is None:
            self.addedAt = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class CurrentList:
    """Represents the current shopping list."""
    date: str
    items: List[GroceryItem]
    
    def __post_init__(self):
        if isinstance(self.items, list) and len(self.items) > 0:
            if isinstance(self.items[0], dict):
                # Convert dicts to GroceryItem objects
                self.items = [GroceryItem(**item) for item in self.items]
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'date': self.date,
            'items': [item.to_dict() for item in self.items]
        }


@dataclass
class ShoppingTrip:
    """Represents a completed shopping trip."""
    id: str
    date: str
    completedAt: str
    items: List[GroceryItem]
    totalItems: int
    checkedItems: int
    
    def __post_init__(self):
        if isinstance(self.items, list) and len(self.items) > 0:
            if isinstance(self.items[0], dict):
                # Convert dicts to GroceryItem objects
                self.items = [GroceryItem(**item) for item in self.items]
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'date': self.date,
            'completedAt': self.completedAt,
            'items': [item.to_dict() for item in self.items],
            'totalItems': self.totalItems,
            'checkedItems': self.checkedItems
        }


@dataclass
class ItemStats:
    """Statistics for a specific item."""
    lastBought: Optional[str] = None
    totalPurchases: int = 0
    averageFrequency: Optional[int] = None  # days
    category: str = "Other"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class GroceryData:
    """Root data structure for the grocery list application."""
    version: str
    current: CurrentList
    history: List[ShoppingTrip]
    itemStats: Dict[str, ItemStats]
    
    def __post_init__(self):
        # Convert current to CurrentList if it's a dict
        if isinstance(self.current, dict):
            self.current = CurrentList(**self.current)
        
        # Convert history items to ShoppingTrip if they're dicts
        if isinstance(self.history, list) and len(self.history) > 0:
            if isinstance(self.history[0], dict):
                self.history = [ShoppingTrip(**trip) for trip in self.history]
        
        # Convert itemStats values to ItemStats if they're dicts
        if isinstance(self.itemStats, dict):
            for key, value in self.itemStats.items():
                if isinstance(value, dict):
                    self.itemStats[key] = ItemStats(**value)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'version': self.version,
            'current': self.current.to_dict(),
            'history': [trip.to_dict() for trip in self.history],
            'itemStats': {key: stats.to_dict() for key, stats in self.itemStats.items()}
        }


# ==================== FILE OPERATIONS (V1 - for migration) ====================

def read_grocery_list():
    """Read items from grocery_list.txt (v1 format)."""
    try:
        with open(GROCERY_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def write_grocery_list(items):
    """Write items to grocery_list.txt (v1 format)."""
    with open(GROCERY_FILE, 'w') as f:
        for item in items:
            f.write(f"{item}\n")


# ==================== FILE OPERATIONS (V2 - JSON) ====================

def read_grocery_data() -> GroceryData:
    """Read grocery data from JSON file."""
    try:
        with open(GROCERY_DATA_FILE, 'r') as f:
            data = json.load(f)
            return GroceryData(**data)
    except FileNotFoundError:
        # Initialize with empty data structure
        return _create_empty_grocery_data()
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        # Backup corrupted file and create new one
        if os.path.exists(GROCERY_DATA_FILE):
            backup_file = f"{GROCERY_DATA_FILE}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(GROCERY_DATA_FILE, backup_file)
            print(f"Corrupted file backed up to: {backup_file}")
        return _create_empty_grocery_data()


def write_grocery_data(data: GroceryData) -> None:
    """Write grocery data to JSON file with atomic write."""
    # Create backup before writing
    if os.path.exists(GROCERY_DATA_FILE):
        backup_file = f"{GROCERY_DATA_FILE}.backup"
        try:
            with open(GROCERY_DATA_FILE, 'r') as f:
                with open(backup_file, 'w') as bf:
                    bf.write(f.read())
        except Exception as e:
            print(f"Backup creation failed: {e}")
    
    # Write to temporary file first (atomic write)
    temp_file = f"{GROCERY_DATA_FILE}.tmp"
    try:
        with open(temp_file, 'w') as f:
            json.dump(data.to_dict(), f, indent=2)
        
        # Rename temp file to actual file (atomic operation)
        os.replace(temp_file, GROCERY_DATA_FILE)
    except Exception as e:
        print(f"Write failed: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise


def _create_empty_grocery_data() -> GroceryData:
    """Create an empty grocery data structure."""
    return GroceryData(
        version="2.0",
        current=CurrentList(
            date=datetime.now().strftime('%Y-%m-%d'),
            items=[]
        ),
        history=[],
        itemStats={}
    )


def migrate_v1_to_v2() -> GroceryData:
    """Migrate from grocery_list.txt (v1) to grocery_data.json (v2)."""
    print("Starting migration from v1 to v2...")
    
    # Read old format
    old_items = read_grocery_list()
    
    if not old_items:
        print("No v1 data found, creating empty v2 structure")
        return _create_empty_grocery_data()
    
    print(f"Found {len(old_items)} items in v1 format")
    
    # Create new structure
    new_data = _create_empty_grocery_data()
    
    # Convert items (we'll add category detection in next task)
    for item_name in old_items:
        new_item = GroceryItem(
            id=str(uuid.uuid4()),
            name=item_name,
            category="Other",  # Will be updated with category detection
            checked=False,
            addedAt=datetime.now().isoformat(),
            checkedAt=None
        )
        new_data.current.items.append(new_item)
    
    # Save new format
    write_grocery_data(new_data)
    print(f"Migration complete! {len(new_data.current.items)} items migrated")
    
    # Backup old file
    if os.path.exists(GROCERY_FILE):
        backup_file = f"{GROCERY_FILE}.v1_backup"
        os.rename(GROCERY_FILE, backup_file)
        print(f"Old file backed up to: {backup_file}")
    
    return new_data


def ensure_data_initialized():
    """Ensure grocery data is initialized, migrate if needed."""
    if not os.path.exists(GROCERY_DATA_FILE):
        # Check if v1 file exists
        if os.path.exists(GROCERY_FILE):
            print("V1 data detected, migrating to v2...")
            migrate_v1_to_v2()
        else:
            print("No existing data, creating new v2 structure...")
            write_grocery_data(_create_empty_grocery_data())


def validate_grocery_data(data: GroceryData) -> bool:
    """Validate grocery data structure."""
    try:
        # Check version
        if not data.version or data.version != "2.0":
            print(f"Invalid version: {data.version}")
            return False
        
        # Check current list
        if not isinstance(data.current, CurrentList):
            print("Invalid current list structure")
            return False
        
        # Check current list items
        if not isinstance(data.current.items, list):
            print("Invalid current items structure")
            return False
        
        for item in data.current.items:
            if not isinstance(item, GroceryItem):
                print(f"Invalid item structure: {item}")
                return False
            if not item.id or not item.name or not item.category:
                print(f"Missing required fields in item: {item}")
                return False
        
        # Check history
        if not isinstance(data.history, list):
            print("Invalid history structure")
            return False
        
        for trip in data.history:
            if not isinstance(trip, ShoppingTrip):
                print(f"Invalid trip structure: {trip}")
                return False
        
        # Check itemStats
        if not isinstance(data.itemStats, dict):
            print("Invalid itemStats structure")
            return False
        
        return True
    
    except Exception as e:
        print(f"Validation error: {e}")
        return False


# ==================== CATEGORY DETECTION ====================

def detect_category_fallback(item_name: str) -> str:
    """Detect category using keyword matching (fallback when AI fails)."""
    item_lower = item_name.lower()
    
    # Check each category's keywords
    for category, config in CATEGORIES.items():
        if category == "Other":
            continue  # Skip "Other" for now
        
        for keyword in config["keywords"]:
            if keyword in item_lower:
                return category
    
    # Default to "Other" if no match found
    return "Other"


def validate_category(category: str) -> str:
    """Validate category and return valid category or fallback to 'Other'."""
    if category in CATEGORIES:
        return category
    
    # Try case-insensitive match
    for valid_category in CATEGORIES.keys():
        if valid_category.lower() == category.lower():
            return valid_category
    
    # Invalid category, return "Other"
    print(f"Invalid category '{category}', defaulting to 'Other'")
    return "Other"


# ==================== GEMINI PARSING ====================

def parse_grocery_items_with_gemini(raw_text):
    """Use Gemini LLM to extract grocery items and assign categories."""
    
    categories_list = ", ".join([cat for cat in CATEGORIES.keys()])
    
    prompt = f"""Extract grocery items from this text and assign categories.

Text: "{raw_text}"

Categories: {categories_list}

Rules:
- Extract ONLY grocery item names
- Remove quantities, measurements, and numbers (2 gallons, a dozen, etc.)
- Remove filler words (I, we, need, get, buy, grab, pick up, for, etc.)
- Remove articles (a, an, the)
- Normalize to title case (Milk, not milk)
- Assign the most appropriate category
- Return as JSON array

Format:
[
  {{"name": "Milk", "category": "Dairy"}},
  {{"name": "Apples", "category": "Produce"}}
]

Examples:
Input: "We need milk, eggs, and bread"
Output: [
  {{"name": "Milk", "category": "Dairy"}},
  {{"name": "Eggs", "category": "Dairy"}},
  {{"name": "Bread", "category": "Bakery"}}
]

Input: "Get stuff for tacos - ground beef, tortillas, cheese, lettuce"
Output: [
  {{"name": "Ground Beef", "category": "Meat & Seafood"}},
  {{"name": "Tortillas", "category": "Bakery"}},
  {{"name": "Cheese", "category": "Dairy"}},
  {{"name": "Lettuce", "category": "Produce"}}
]

Now extract from: "{raw_text}"
"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
            text = text.strip()
        
        # Parse JSON response
        items = json.loads(text)
        
        if not items:
            return []
        
        # Validate and return items with categories
        result = []
        for item in items:
            if isinstance(item, dict) and 'name' in item and 'category' in item:
                result.append(item)
        
        return result
    
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to simple parsing without categories
        return simple_fallback_parse_with_categories(raw_text)


def simple_fallback_parse(raw_text):
    """Simple fallback parser if Gemini fails (v1 compatibility)."""
    import re
    
    # Remove common filler words
    filler_words = ['i', 'we', 'need', 'get', 'buy', 'grab', 'pick', 'up', 'the', 'a', 'an', 'some']
    
    # Split by common delimiters
    items = re.split(r',|\sand\s|\sor\s', raw_text.lower())
    
    cleaned_items = []
    for item in items:
        # Remove filler words
        words = item.split()
        words = [w for w in words if w not in filler_words]
        
        if words:
            cleaned_item = ' '.join(words).title()
            cleaned_items.append(cleaned_item)
    
    return cleaned_items


def simple_fallback_parse_with_categories(raw_text):
    """Simple fallback parser with category detection if Gemini fails."""
    import re
    
    # Remove common filler words
    filler_words = ['i', 'we', 'need', 'get', 'buy', 'grab', 'pick', 'up', 'the', 'a', 'an', 'some']
    
    # Split by common delimiters
    items = re.split(r',|\sand\s|\sor\s', raw_text.lower())
    
    cleaned_items = []
    for item in items:
        # Remove filler words
        words = item.split()
        words = [w for w in words if w not in filler_words]
        
        if words:
            cleaned_item = ' '.join(words).title()
            category = detect_category_fallback(cleaned_item)
            cleaned_items.append({
                'name': cleaned_item,
                'category': category
            })
    
    return cleaned_items


# ==================== V1 DEDUPLICATION (DEPRECATED - kept for reference) ====================
# This function is no longer used in v2. Deduplication is now handled in the /add-item endpoint.


# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    """Serve the web UI."""
    return render_template('index.html')


@app.route('/get-items', methods=['GET'])
def get_items():
    """Return all grocery items (v1 compatibility - deprecated, use /get-current-list instead)."""
    # Redirect to v2 endpoint
    return get_current_list()


@app.route('/get-current-list', methods=['GET'])
def get_current_list():
    """Return current list grouped by categories (v2)."""
    ensure_data_initialized()
    
    grocery_data = read_grocery_data()
    
    # Group items by category
    categories = {}
    for item in grocery_data.current.items:
        if item.category not in categories:
            categories[item.category] = []
        
        # Calculate "last bought" info
        last_bought_info = None
        days_since = None
        frequency_label = None
        
        if item.name in grocery_data.itemStats:
            stats = grocery_data.itemStats[item.name]
            if stats.lastBought:
                last_bought_date = datetime.fromisoformat(stats.lastBought)
                days_since = (datetime.now() - last_bought_date).days
                last_bought_info = stats.lastBought
            
            if stats.averageFrequency:
                if stats.averageFrequency <= 3:
                    frequency_label = "Every few days"
                elif stats.averageFrequency <= 7:
                    frequency_label = "Weekly"
                elif stats.averageFrequency <= 14:
                    frequency_label = "Every 2 weeks"
                else:
                    frequency_label = f"Every {stats.averageFrequency} days"
        
        categories[item.category].append({
            'id': item.id,
            'name': item.name,
            'checked': item.checked,
            'addedAt': item.addedAt,
            'checkedAt': item.checkedAt,
            'lastBought': last_bought_info,
            'daysSinceLastBought': days_since,
            'frequency': frequency_label
        })
    
    # Sort categories by order
    sorted_categories = {}
    for category in sorted(CATEGORIES.keys(), key=lambda c: CATEGORIES[c]['order']):
        if category in categories and len(categories[category]) > 0:
            sorted_categories[category] = categories[category]
    
    # Count totals
    total_items = len(grocery_data.current.items)
    checked_items = sum(1 for item in grocery_data.current.items if item.checked)
    
    return jsonify({
        'date': grocery_data.current.date,
        'categories': sorted_categories,
        'totalItems': total_items,
        'checkedItems': checked_items
    })


@app.route('/add-item', methods=['POST'])
def add_item():
    """Add items from natural language with categories (v2)."""
    ensure_data_initialized()
    
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    raw_text = data.get('text', '').strip()
    
    if not raw_text:
        return jsonify({'error': 'Empty text'}), 400
    
    # Parse with Gemini (returns items with categories)
    parsed_items = parse_grocery_items_with_gemini(raw_text)
    
    if not parsed_items:
        grocery_data = read_grocery_data()
        return jsonify({
            'success': True,
            'message': 'No grocery items found in text',
            'added': [],
            'skipped': [],
            'total': len(grocery_data.current.items)
        })
    
    # Load current data
    grocery_data = read_grocery_data()
    
    # Get existing item names (case-insensitive)
    existing_names = {item.name.lower(): item for item in grocery_data.current.items}
    
    added = []
    skipped = []
    
    for parsed_item in parsed_items:
        item_name = parsed_item['name']
        item_category = validate_category(parsed_item['category'])
        
        # Check for duplicates (case-insensitive)
        if item_name.lower() in existing_names:
            skipped.append({
                'name': item_name,
                'category': item_category,
                'reason': 'Already in list'
            })
            continue
        
        # Create new item
        new_item = GroceryItem(
            id=str(uuid.uuid4()),
            name=item_name,
            category=item_category,
            checked=False,
            addedAt=datetime.now().isoformat(),
            checkedAt=None
        )
        
        grocery_data.current.items.append(new_item)
        existing_names[item_name.lower()] = new_item
        
        # Get "last bought" info from stats
        last_bought_info = None
        days_since = None
        if item_name in grocery_data.itemStats:
            stats = grocery_data.itemStats[item_name]
            if stats.lastBought:
                last_bought_date = datetime.fromisoformat(stats.lastBought)
                days_since = (datetime.now() - last_bought_date).days
                last_bought_info = stats.lastBought
        
        added.append({
            'name': item_name,
            'category': item_category,
            'lastBought': last_bought_info,
            'daysSinceLastBought': days_since
        })
    
    # Save updated data
    write_grocery_data(grocery_data)
    
    return jsonify({
        'success': True,
        'added': added,
        'skipped': skipped,
        'total': len(grocery_data.current.items)
    })


@app.route('/toggle-item', methods=['POST'])
def toggle_item():
    """Toggle item checked status (v2)."""
    ensure_data_initialized()
    
    data = request.get_json()
    
    if not data or 'itemId' not in data:
        return jsonify({'error': 'No itemId provided'}), 400
    
    item_id = data.get('itemId')
    
    grocery_data = read_grocery_data()
    
    # Find item by ID
    item_found = None
    for item in grocery_data.current.items:
        if item.id == item_id:
            item_found = item
            break
    
    if not item_found:
        return jsonify({'error': 'Item not found'}), 404
    
    # Toggle checked status
    item_found.checked = not item_found.checked
    item_found.checkedAt = datetime.now().isoformat() if item_found.checked else None
    
    # Save updated data
    write_grocery_data(grocery_data)
    
    return jsonify({
        'success': True,
        'itemId': item_id,
        'checked': item_found.checked,
        'checkedAt': item_found.checkedAt
    })


@app.route('/delete-item', methods=['POST'])
def delete_item():
    """Delete an item from the list (v2)."""
    ensure_data_initialized()
    
    data = request.get_json()
    
    if not data or 'itemId' not in data:
        return jsonify({'error': 'No itemId provided'}), 400
    
    item_id = data.get('itemId')
    
    grocery_data = read_grocery_data()
    
    # Find and remove item by ID
    item_found = None
    for i, item in enumerate(grocery_data.current.items):
        if item.id == item_id:
            item_found = grocery_data.current.items.pop(i)
            break
    
    if not item_found:
        return jsonify({'error': 'Item not found'}), 404
    
    # Save updated data
    write_grocery_data(grocery_data)
    
    return jsonify({
        'success': True,
        'deleted': item_found.name,
        'total': len(grocery_data.current.items)
    })


@app.route('/complete-trip', methods=['POST'])
def complete_trip():
    """Complete current shopping trip and move to history (v2)."""
    ensure_data_initialized()
    
    grocery_data = read_grocery_data()
    
    # Check if there are items to complete
    if not grocery_data.current.items:
        return jsonify({'error': 'No items in current list'}), 400
    
    # Create shopping trip from current list
    trip_id = str(uuid.uuid4())
    completion_time = datetime.now().isoformat()
    
    # Count totals
    total_items = len(grocery_data.current.items)
    checked_items = sum(1 for item in grocery_data.current.items if item.checked)
    
    # Create trip object
    shopping_trip = ShoppingTrip(
        id=trip_id,
        date=grocery_data.current.date,
        completedAt=completion_time,
        items=grocery_data.current.items.copy(),  # Copy current items
        totalItems=total_items,
        checkedItems=checked_items
    )
    
    # Update item statistics for checked items
    for item in grocery_data.current.items:
        if item.checked:
            if item.name not in grocery_data.itemStats:
                grocery_data.itemStats[item.name] = ItemStats(
                    category=item.category
                )
            
            stats = grocery_data.itemStats[item.name]
            stats.lastBought = completion_time
            stats.totalPurchases += 1
            
            # Calculate average frequency if we have previous purchase
            if stats.totalPurchases > 1 and stats.lastBought:
                # Simple frequency calculation (can be improved)
                # For now, just estimate based on total purchases
                days_since_first = (datetime.now() - datetime.fromisoformat(stats.lastBought)).days
                if days_since_first > 0:
                    stats.averageFrequency = max(1, days_since_first // stats.totalPurchases)
    
    # Add trip to history
    grocery_data.history.append(shopping_trip)
    
    # Clean history - keep only last 4 weeks
    four_weeks_ago = datetime.now() - timedelta(weeks=4)
    grocery_data.history = [
        trip for trip in grocery_data.history
        if datetime.fromisoformat(trip.completedAt) > four_weeks_ago
    ]
    
    # Create new empty current list
    grocery_data.current = CurrentList(
        date=datetime.now().strftime('%Y-%m-%d'),
        items=[]
    )
    
    # Save updated data
    write_grocery_data(grocery_data)
    
    return jsonify({
        'success': True,
        'trip': shopping_trip.to_dict(),
        'message': f'Shopping trip completed! {checked_items} of {total_items} items checked off.'
    })


@app.route('/get-history', methods=['GET'])
def get_history():
    """Get shopping history (last 4 weeks) (v2)."""
    ensure_data_initialized()
    
    grocery_data = read_grocery_data()
    
    # Calculate days ago for each trip
    now = datetime.now()
    trips_with_metadata = []
    
    for trip in grocery_data.history:
        trip_date = datetime.fromisoformat(trip.completedAt)
        days_ago = (now - trip_date).days
        
        trip_dict = trip.to_dict()
        trip_dict['daysAgo'] = days_ago
        trips_with_metadata.append(trip_dict)
    
    # Sort by completion date (newest first)
    trips_with_metadata.sort(key=lambda x: x['completedAt'], reverse=True)
    
    return jsonify({
        'trips': trips_with_metadata,
        'totalTrips': len(trips_with_metadata)
    })


@app.route('/copy-from-last-trip', methods=['POST'])
def copy_from_last_trip():
    """Copy items from the most recent trip to current list (v2)."""
    ensure_data_initialized()
    
    grocery_data = read_grocery_data()
    
    # Check if there's any history
    if not grocery_data.history:
        return jsonify({'error': 'No previous trips found'}), 404
    
    # Get the most recent trip
    last_trip = max(grocery_data.history, key=lambda t: t.completedAt)
    
    # Get existing item names (case-insensitive) for duplicate checking
    existing_names = {item.name.lower(): item for item in grocery_data.current.items}
    
    copied = []
    skipped = []
    
    for trip_item in last_trip.items:
        # Check for duplicates (case-insensitive)
        if trip_item.name.lower() in existing_names:
            skipped.append({
                'name': trip_item.name,
                'category': trip_item.category,
                'reason': 'Already in current list'
            })
            continue
        
        # Create new item (with new ID and timestamp)
        new_item = GroceryItem(
            id=str(uuid.uuid4()),
            name=trip_item.name,
            category=trip_item.category,
            checked=False,  # Always start unchecked
            addedAt=datetime.now().isoformat(),
            checkedAt=None
        )
        
        grocery_data.current.items.append(new_item)
        existing_names[trip_item.name.lower()] = new_item
        
        copied.append({
            'name': trip_item.name,
            'category': trip_item.category
        })
    
    # Save updated data
    write_grocery_data(grocery_data)
    
    return jsonify({
        'success': True,
        'copied': copied,
        'skipped': skipped,
        'copiedCount': len(copied),
        'skippedCount': len(skipped),
        'totalItems': len(grocery_data.current.items)
    })


@app.route('/clear-all', methods=['POST'])
def clear_all():
    """Clear all items from the list (v2)."""
    ensure_data_initialized()
    
    grocery_data = read_grocery_data()
    grocery_data.current.items = []  # Clear all items
    write_grocery_data(grocery_data)
    
    return jsonify({
        'success': True,
        'message': 'All items cleared',
        'total': 0
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
