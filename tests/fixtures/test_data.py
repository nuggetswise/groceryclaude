"""
Test data fixtures for comprehensive testing
Contains all test cases, expected results, and sample data
"""

# =============================================================================
# PARSING TEST DATA
# =============================================================================

# Basic delimiter tests
BASIC_PARSING_TESTS = [
    # (input, expected_output)
    ("milk", ["Milk"]),
    ("milk, eggs", ["Milk", "Eggs"]),
    ("milk and eggs", ["Milk", "Eggs"]),
    ("milk or eggs", ["Milk", "Eggs"]),
    ("milk, eggs, and bread", ["Milk", "Eggs", "Bread"]),
    ("milk, eggs and bread", ["Milk", "Eggs", "Bread"]),
]

# Natural language tests
NATURAL_LANGUAGE_TESTS = [
    ("We need milk", ["Milk"]),
    ("I need eggs and bread", ["Eggs", "Bread"]),
    ("Can you grab milk, eggs, and bread?", ["Milk", "Eggs", "Bread"]),
    ("Pick up some cheese from the store", ["Cheese"]),
    ("We're out of butter", ["Butter"]),
    ("Get yogurt and sour cream", ["Yogurt", "Sour Cream"]),
    ("Please buy apples", ["Apples"]),
    ("Don't forget the oranges", ["Oranges"]),
]

# Filler word removal tests
FILLER_WORD_TESTS = [
    ("we need milk", ["Milk"]),
    ("I need eggs", ["Eggs"]),
    ("you need bread", ["Bread"]),
    ("they need butter", ["Butter"]),
    ("the milk", ["Milk"]),
    ("a loaf of bread", ["Loaf", "Bread"]),  # May need adjustment based on implementation
    ("an apple", ["Apple"]),
    ("some cheese", ["Cheese"]),
    ("get milk", ["Milk"]),
    ("buy eggs", ["Eggs"]),
    ("grab bread", ["Bread"]),
    ("pick up butter", ["Butter"]),
]

# Quantity handling tests
QUANTITY_TESTS = [
    # Basic quantities
    ("2 gallons of milk", ["Milk"]),
    ("1 dozen eggs", ["Eggs"]),
    ("3 lbs of apples", ["Apples"]),
    ("5 pounds of potatoes", ["Potatoes"]),
    ("2 oz of vanilla", ["Vanilla"]),

    # Complex quantities
    ("2 gallons of milk and 1 dozen eggs", ["Milk", "Eggs"]),
    ("3 lbs apples, 2 lbs oranges", ["Apples", "Oranges"]),

    # Note: If keeping quantities, change expected output to:
    # ("2 gallons of milk", ["Milk (2 gal)"]),
]

# Capitalization tests
CAPITALIZATION_TESTS = [
    ("milk", ["Milk"]),
    ("MILK", ["Milk"]),
    ("MiLk", ["Milk"]),
    ("cheddar cheese", ["Cheddar Cheese"]),
    ("CHEDDAR CHEESE", ["Cheddar Cheese"]),
    ("sour cream", ["Sour Cream"]),
    ("greek yogurt", ["Greek Yogurt"]),
]

# Multi-word item tests
MULTI_WORD_TESTS = [
    ("cheddar cheese", ["Cheddar Cheese"]),
    ("sour cream", ["Sour Cream"]),
    ("almond milk", ["Almond Milk"]),
    ("greek yogurt", ["Greek Yogurt"]),
    ("brown sugar", ["Brown Sugar"]),
    ("olive oil", ["Olive Oil"]),
    ("chicken breast", ["Chicken Breast"]),
    ("ice cream", ["Ice Cream"]),
    ("peanut butter", ["Peanut Butter"]),
]

# Edge case tests
EDGE_CASE_TESTS = [
    ("", []),
    ("   ", []),
    ("we need the a", []),
    ("and or the", []),
    ("123", []),
    ("!!!", []),
    (".", []),
]

# Special character tests
SPECIAL_CHARACTER_TESTS = [
    ("milk!", ["Milk"]),
    ("eggs?", ["Eggs"]),
    ("bread.", ["Bread"]),
    ("milk, eggs, bread!", ["Milk", "Eggs", "Bread"]),
    ("jalapeños", ["Jalapeños"]),
    ("café latte", ["Café Latte"]),
]

# Complex real-world scenarios
COMPLEX_SCENARIOS = [
    (
        "Can you grab 2 gallons of milk, 1 dozen eggs, and a loaf of bread from the store?",
        ["Milk", "Eggs", "Loaf", "Bread"]  # Adjust based on implementation
    ),
    (
        "We need cheddar cheese, sour cream, greek yogurt, and some butter",
        ["Cheddar Cheese", "Sour Cream", "Greek Yogurt", "Butter"]
    ),
    (
        "I'm making dinner tonight so we need chicken breast, olive oil, garlic, and onions",
        ["Chicken Breast", "Olive Oil", "Garlic", "Onions"]
    ),
    (
        "Pick up apples, bananas, oranges, strawberries, and blueberries",
        ["Apples", "Bananas", "Oranges", "Strawberries", "Blueberries"]
    ),
]

# Parametrized test data (all parsing tests combined)
ALL_PARSING_TESTS = (
    BASIC_PARSING_TESTS +
    NATURAL_LANGUAGE_TESTS +
    CAPITALIZATION_TESTS +
    EDGE_CASE_TESTS
)


# =============================================================================
# DEDUPLICATION TEST DATA
# =============================================================================

DUPLICATE_TEST_CASES = [
    {
        'existing': ["Milk", "Eggs", "Bread"],
        'new': "Milk",
        'should_be_duplicate': True,
        'description': 'Exact match'
    },
    {
        'existing': ["Milk", "Eggs", "Bread"],
        'new': "milk",
        'should_be_duplicate': True,
        'description': 'Case insensitive - lowercase'
    },
    {
        'existing': ["Milk", "Eggs", "Bread"],
        'new': "MILK",
        'should_be_duplicate': True,
        'description': 'Case insensitive - uppercase'
    },
    {
        'existing': ["Milk", "Eggs", "Bread"],
        'new': "  Milk  ",
        'should_be_duplicate': True,
        'description': 'Whitespace trimming'
    },
    {
        'existing': ["Milk", "Eggs", "Bread"],
        'new': "Butter",
        'should_be_duplicate': False,
        'description': 'Different item'
    },
    {
        'existing': ["Carrots"],
        'new': "Baby Carrots",
        'should_be_duplicate': False,
        'description': 'Similar but different items'
    },
    {
        'existing': [],
        'new': "Milk",
        'should_be_duplicate': False,
        'description': 'Empty list - no duplicates'
    },
]


# =============================================================================
# API ENDPOINT TEST DATA
# =============================================================================

API_ADD_ITEM_TESTS = [
    {
        'input': {'text': 'milk'},
        'expected_status': 200,
        'expected_added': 1,
        'expected_items': ['Milk'],
        'description': 'Add single item'
    },
    {
        'input': {'text': 'milk, eggs, bread'},
        'expected_status': 200,
        'expected_added': 3,
        'expected_items': ['Milk', 'Eggs', 'Bread'],
        'description': 'Add multiple items'
    },
    {
        'input': {'text': 'We need milk and eggs'},
        'expected_status': 200,
        'expected_added': 2,
        'expected_items': ['Milk', 'Eggs'],
        'description': 'Natural language'
    },
    {
        'input': {},
        'expected_status': 400,
        'description': 'Missing text field - should error'
    },
    {
        'input': {'text': ''},
        'expected_status': 200,
        'expected_added': 0,
        'expected_items': [],
        'description': 'Empty text'
    },
]


# =============================================================================
# IOS SHORTCUT TEST MESSAGES
# =============================================================================

IOS_TEST_MESSAGES = [
    {
        'message': "We need milk",
        'expected_items': ["Milk"],
        'description': "Simple single item"
    },
    {
        'message': "Pick up eggs and bread",
        'expected_items': ["Eggs", "Bread"],
        'description': "Two items with action verb"
    },
    {
        'message': "Get 2 gallons of milk, 1 dozen eggs, and a loaf of bread",
        'expected_items': ["Milk", "Eggs", "Loaf", "Bread"],  # Adjust based on implementation
        'description': "Complex message with quantities"
    },
    {
        'message': "milk, eggs, cheese, butter, yogurt",
        'expected_items': ["Milk", "Eggs", "Cheese", "Butter", "Yogurt"],
        'description': "Simple comma-separated list"
    },
    {
        'message': "Can you grab some cheddar cheese?",
        'expected_items': ["Cheddar Cheese"],
        'description': "Multi-word item in question"
    },
    {
        'message': "We're out of milk and eggs",
        'expected_items': ["Milk", "Eggs"],
        'description': "Conversational style"
    },
    {
        'message': "I'm making pasta tonight. We need pasta sauce, parmesan cheese, and garlic bread",
        'expected_items': ["Pasta Sauce", "Parmesan Cheese", "Garlic Bread"],
        'description': "Shopping list with context"
    },
    {
        'message': "",
        'expected_items': [],
        'description': "Empty message - should handle gracefully"
    },
]


# =============================================================================
# SAMPLE GROCERY LISTS (for file-based tests)
# =============================================================================

SAMPLE_GROCERY_LISTS = {
    'empty': "",

    'single': "Milk\n",

    'small': "Milk\nEggs\nBread\n",

    'medium': "Milk\nEggs\nBread\nButter\nCheese\nYogurt\nChicken\nRice\nPasta\nTomatoes\n",

    'standard': """Milk
Eggs
Bread
Butter
Cheese
Yogurt
Chicken Breast
Ground Beef
Apples
Bananas
Oranges
Carrots
Broccoli
Tomatoes
Onions
Garlic
Rice
Pasta
Olive Oil
Salt
""",

    'large': "\n".join([f"Item{i}" for i in range(100)]) + "\n",

    'very_large': "\n".join([f"Item{i}" for i in range(1000)]) + "\n",

    'with_multi_word': """Cheddar Cheese
Sour Cream
Greek Yogurt
Almond Milk
Brown Sugar
Olive Oil
Chicken Breast
Ice Cream
Peanut Butter
""",
}


# =============================================================================
# END-TO-END TEST SCENARIOS
# =============================================================================

E2E_SCENARIOS = [
    {
        'name': 'Complete add-view-delete journey',
        'steps': [
            {'action': 'add', 'text': 'milk, eggs, bread'},
            {'action': 'get', 'expected': ['Milk', 'Eggs', 'Bread']},
            {'action': 'delete', 'item': 'Milk'},
            {'action': 'get', 'expected': ['Eggs', 'Bread']},
        ]
    },
    {
        'name': 'Multiple additions with duplicates',
        'steps': [
            {'action': 'add', 'text': 'milk, eggs'},
            {'action': 'add', 'text': 'eggs, bread, butter'},
            {'action': 'add', 'text': 'milk, eggs', 'expected_duplicates': 2},
            {'action': 'get', 'expected': ['Milk', 'Eggs', 'Bread', 'Butter']},
        ]
    },
    {
        'name': 'Delete and re-add same item',
        'steps': [
            {'action': 'add', 'text': 'milk, eggs'},
            {'action': 'delete', 'item': 'Milk'},
            {'action': 'get', 'expected': ['Eggs']},
            {'action': 'add', 'text': 'milk'},  # Should work now
            {'action': 'get', 'expected': ['Eggs', 'Milk']},
        ]
    },
]


# =============================================================================
# PERFORMANCE TEST DATA
# =============================================================================

PERFORMANCE_BENCHMARKS = {
    'add_single_item': {
        'max_time': 0.1,  # seconds
        'description': 'Add one item'
    },
    'add_10_items': {
        'max_time': 0.5,
        'description': 'Add 10 items at once'
    },
    'add_100_items': {
        'max_time': 2.0,
        'description': 'Add 100 items at once'
    },
    'get_items_100': {
        'max_time': 0.5,
        'description': 'Get list with 100 items'
    },
    'get_items_1000': {
        'max_time': 1.0,
        'description': 'Get list with 1000 items'
    },
    'delete_from_100': {
        'max_time': 0.2,
        'description': 'Delete one item from 100'
    },
    'delete_from_1000': {
        'max_time': 0.5,
        'description': 'Delete one item from 1000'
    },
    'duplicate_check_500': {
        'max_time': 1.0,
        'description': 'Check duplicates against 500 items'
    },
}


# =============================================================================
# COMMON GROCERY ITEMS (for realistic test data)
# =============================================================================

COMMON_GROCERY_ITEMS = [
    # Dairy
    "Milk", "Eggs", "Butter", "Cheese", "Yogurt", "Cream Cheese", "Sour Cream",
    "Cottage Cheese", "Almond Milk", "Greek Yogurt",

    # Produce
    "Apples", "Bananas", "Oranges", "Strawberries", "Blueberries", "Grapes",
    "Carrots", "Broccoli", "Tomatoes", "Onions", "Garlic", "Potatoes",
    "Lettuce", "Spinach", "Bell Peppers",

    # Meat
    "Chicken Breast", "Ground Beef", "Pork Chops", "Bacon", "Turkey",
    "Salmon", "Shrimp",

    # Pantry
    "Rice", "Pasta", "Bread", "Olive Oil", "Vegetable Oil", "Salt", "Pepper",
    "Sugar", "Brown Sugar", "Flour", "Baking Soda", "Vanilla Extract",

    # Frozen
    "Ice Cream", "Frozen Pizza", "Frozen Vegetables",

    # Beverages
    "Coffee", "Tea", "Orange Juice", "Water",

    # Condiments
    "Ketchup", "Mustard", "Mayonnaise", "Hot Sauce", "Soy Sauce",

    # Snacks
    "Chips", "Crackers", "Cookies", "Peanut Butter",
]


# =============================================================================
# FILLER WORDS TO REMOVE (reference for parsing implementation)
# =============================================================================

FILLER_WORDS = [
    "we", "i", "you", "they", "the", "a", "an", "need", "to", "get", "buy",
    "grab", "pick", "up", "some", "is", "are", "was", "were", "from", "store",
    "can", "please", "don't", "forget", "out", "of", "more", "and", "or"
]


# =============================================================================
# DELIMITER PATTERNS (reference for parsing implementation)
# =============================================================================

DELIMITERS = [
    ",",      # comma
    " and ",  # and
    " or ",   # or
    ", and ", # comma and
    ", or ",  # comma or
]


# =============================================================================
# EXPECTED API RESPONSE FORMATS
# =============================================================================

EXPECTED_ADD_RESPONSE_FORMAT = {
    'success': bool,
    'added': int,
    'duplicates': int,
    'items_added': list,  # List of strings
    'items_skipped': list,  # List of strings
}

EXPECTED_DELETE_RESPONSE_FORMAT = {
    'success': bool,
    'message': str,
}

EXPECTED_GET_RESPONSE_FORMAT = list  # List of strings


# =============================================================================
# ERROR TEST CASES
# =============================================================================

ERROR_TEST_CASES = [
    {
        'endpoint': '/add-item',
        'method': 'POST',
        'data': {},
        'expected_status': 400,
        'description': 'Missing text field'
    },
    {
        'endpoint': '/add-item',
        'method': 'POST',
        'data': 'not json',
        'expected_status': 400,
        'description': 'Malformed JSON'
    },
    {
        'endpoint': '/delete-item',
        'method': 'POST',
        'data': {},
        'expected_status': 400,
        'description': 'Missing item field'
    },
    {
        'endpoint': '/delete-item',
        'method': 'POST',
        'data': {'item': 'NonExistent'},
        'expected_status': 404,
        'description': 'Item not found'
    },
]


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_item_format(item):
    """
    Validate that an item follows expected format:
    - Non-empty string
    - Properly capitalized (Title Case)
    - No leading/trailing whitespace
    """
    if not isinstance(item, str):
        return False, "Item must be a string"
    if not item:
        return False, "Item cannot be empty"
    if item != item.strip():
        return False, "Item has leading/trailing whitespace"
    if item != item.title():
        return False, "Item not in Title Case"
    return True, "Valid"


def validate_grocery_list(items):
    """
    Validate a list of grocery items
    """
    if not isinstance(items, list):
        return False, "Items must be a list"

    for item in items:
        valid, msg = validate_item_format(item)
        if not valid:
            return False, f"Invalid item '{item}': {msg}"

    # Check for duplicates
    if len(items) != len(set(items)):
        return False, "List contains duplicates"

    return True, "Valid"
