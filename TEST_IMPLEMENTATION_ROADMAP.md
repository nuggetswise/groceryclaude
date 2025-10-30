# Test Implementation Roadmap

## Overview

This document provides a step-by-step roadmap for implementing the test suite for the Smart Grocery List application. Follow this order to build tests incrementally as you develop features.

## Phase 0: Setup (15 minutes)

### Step 1: Install Dependencies
```bash
pip install pytest pytest-flask pytest-cov pytest-watch
```

### Step 2: Create Directory Structure
```bash
mkdir -p tests/fixtures tests/test_grocery_lists
touch tests/__init__.py
touch tests/fixtures/__init__.py
```

### Step 3: Create pytest.ini
Create `/home/user/groceryclaude/pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    performance: Performance tests
    regression: Regression tests
    critical: Critical path tests
```

### Step 4: Create conftest.py
Create `/home/user/groceryclaude/conftest.py`:
```python
import pytest
import os
import tempfile
import sys

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True

    # Use temporary file for testing
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    app.config['GROCERY_LIST_FILE'] = path

    with app.test_client() as client:
        yield client

    # Cleanup
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def temp_grocery_file():
    """Create a temporary grocery list file for testing"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def populated_grocery_file(temp_grocery_file):
    """Create a grocery file with sample data"""
    with open(temp_grocery_file, 'w') as f:
        f.write("Milk\nEggs\nBread\nButter\nCheese\n")
    return temp_grocery_file

@pytest.fixture
def large_grocery_file(temp_grocery_file):
    """Create a grocery file with 1000 items"""
    with open(temp_grocery_file, 'w') as f:
        for i in range(1000):
            f.write(f"Item{i}\n")
    return temp_grocery_file
```

### Step 5: Verify Setup
```bash
pytest --version
pytest --co  # Show what would be collected
```

---

## Phase 1: Unit Tests for Parsing (TDD Approach)

### When: Before implementing parse_grocery_text() function

### Step 1: Create test_parsing.py
Create `/home/user/groceryclaude/tests/test_parsing.py`:

```python
"""
Unit tests for grocery text parsing functionality
"""
import pytest
from app import parse_grocery_text


@pytest.mark.unit
class TestBasicParsing:
    """Test basic delimiter parsing"""

    def test_single_item(self):
        """Test parsing single item"""
        assert parse_grocery_text("milk") == ["Milk"]

    def test_comma_separated_items(self):
        """Test parsing comma-separated items"""
        assert parse_grocery_text("milk, eggs, bread") == ["Milk", "Eggs", "Bread"]

    def test_and_separated_items(self):
        """Test parsing 'and' separated items"""
        assert parse_grocery_text("milk and eggs and bread") == ["Milk", "Eggs", "Bread"]

    def test_or_separated_items(self):
        """Test parsing 'or' separated items"""
        assert parse_grocery_text("milk or eggs or bread") == ["Milk", "Eggs", "Bread"]

    def test_mixed_delimiters(self):
        """Test parsing mixed delimiters"""
        assert parse_grocery_text("milk, eggs and bread") == ["Milk", "Eggs", "Bread"]


@pytest.mark.unit
class TestFillerWordRemoval:
    """Test removal of filler words"""

    def test_remove_we_need(self):
        """Test removal of 'we need' prefix"""
        assert parse_grocery_text("we need milk and eggs") == ["Milk", "Eggs"]

    def test_remove_i_need(self):
        """Test removal of 'I need' prefix"""
        assert parse_grocery_text("I need milk") == ["Milk"]

    def test_remove_can_you_grab(self):
        """Test removal of 'can you grab' prefix"""
        assert parse_grocery_text("Can you grab milk and eggs?") == ["Milk", "Eggs"]

    def test_remove_multiple_filler_words(self):
        """Test removal of multiple filler words"""
        assert parse_grocery_text("We need to get the milk") == ["Milk"]


@pytest.mark.unit
class TestCapitalization:
    """Test capitalization and formatting"""

    def test_capitalize_single_word(self):
        """Test capitalization of single word"""
        assert parse_grocery_text("milk") == ["Milk"]

    def test_capitalize_multiple_words(self):
        """Test capitalization of multi-word items"""
        result = parse_grocery_text("cheddar cheese")
        assert result == ["Cheddar Cheese"]

    def test_trim_whitespace(self):
        """Test trimming of extra whitespace"""
        assert parse_grocery_text("  milk  ,   eggs   ") == ["Milk", "Eggs"]


@pytest.mark.unit
class TestEdgeCases:
    """Test edge cases"""

    def test_empty_string(self):
        """Test parsing empty string"""
        assert parse_grocery_text("") == []

    def test_whitespace_only(self):
        """Test string with only whitespace"""
        assert parse_grocery_text("   ") == []

    def test_only_filler_words(self):
        """Test string with only filler words"""
        assert parse_grocery_text("we need the a") == []

    def test_special_characters(self):
        """Test handling special characters"""
        assert parse_grocery_text("milk! eggs? bread.") == ["Milk", "Eggs", "Bread"]


@pytest.mark.unit
@pytest.mark.parametrize("input_text,expected", [
    ("milk", ["Milk"]),
    ("milk, eggs", ["Milk", "Eggs"]),
    ("milk and eggs", ["Milk", "Eggs"]),
    ("We need milk", ["Milk"]),
    ("", []),
    ("   ", []),
    ("cheddar cheese", ["Cheddar Cheese"]),
])
def test_parsing_parametrized(input_text, expected):
    """Parametrized test for various parsing scenarios"""
    assert parse_grocery_text(input_text) == expected
```

### Step 2: Run Tests (Should Fail - TDD Red Phase)
```bash
pytest tests/test_parsing.py -v
# Expected: All tests fail because parse_grocery_text doesn't exist yet
```

### Step 3: Implement parse_grocery_text() in app.py
Now implement the function to make tests pass (TDD Green Phase)

### Step 4: Run Tests Again (Should Pass - TDD Green Phase)
```bash
pytest tests/test_parsing.py -v
# Expected: All tests pass
```

### Step 5: Check Coverage
```bash
pytest tests/test_parsing.py --cov=app --cov-report=term-missing
# Target: 100% coverage of parse_grocery_text function
```

---

## Phase 2: Unit Tests for Deduplication

### When: Before implementing deduplication logic

### Step 1: Create test_deduplication.py
Create `/home/user/groceryclaude/tests/test_deduplication.py`:

```python
"""
Unit tests for item deduplication functionality
"""
import pytest
from app import is_duplicate, get_existing_items, add_items_to_list


@pytest.mark.unit
class TestDuplicateDetection:
    """Test duplicate detection logic"""

    def test_exact_match_duplicate(self):
        """Test exact match is detected as duplicate"""
        existing = ["Milk", "Eggs", "Bread"]
        assert is_duplicate("Milk", existing) == True

    def test_case_insensitive_duplicate(self):
        """Test case-insensitive duplicate detection"""
        existing = ["Milk", "Eggs"]
        assert is_duplicate("milk", existing) == True
        assert is_duplicate("MILK", existing) == True
        assert is_duplicate("MiLk", existing) == True

    def test_whitespace_trimming(self):
        """Test whitespace is trimmed before comparison"""
        existing = ["Milk", "Eggs"]
        assert is_duplicate("  Milk  ", existing) == True

    def test_not_duplicate(self):
        """Test non-duplicate items"""
        existing = ["Milk", "Eggs"]
        assert is_duplicate("Butter", existing) == False

    def test_empty_existing_list(self):
        """Test no duplicates in empty list"""
        existing = []
        assert is_duplicate("Milk", existing) == False


@pytest.mark.unit
class TestFileBasedDeduplication:
    """Test deduplication with file operations"""

    def test_read_existing_items(self, populated_grocery_file):
        """Test reading existing items from file"""
        items = get_existing_items(populated_grocery_file)
        assert "Milk" in items
        assert "Eggs" in items
        assert len(items) == 5

    def test_add_to_empty_file(self, temp_grocery_file):
        """Test adding items to empty file"""
        new_items = ["Milk", "Eggs", "Bread"]
        result = add_items_to_list(new_items, temp_grocery_file)

        assert result['added'] == 3
        assert result['duplicates'] == 0

        items = get_existing_items(temp_grocery_file)
        assert set(items) == {"Milk", "Eggs", "Bread"}

    def test_add_with_duplicates(self, populated_grocery_file):
        """Test adding items where some are duplicates"""
        new_items = ["Milk", "Yogurt", "Eggs"]
        result = add_items_to_list(new_items, populated_grocery_file)

        assert result['added'] == 1  # Only Yogurt
        assert result['duplicates'] == 2  # Milk and Eggs
        assert "Yogurt" in result['items_added']

    def test_all_duplicates(self, populated_grocery_file):
        """Test when all items are duplicates"""
        new_items = ["Milk", "Eggs", "Bread"]
        result = add_items_to_list(new_items, populated_grocery_file)

        assert result['added'] == 0
        assert result['duplicates'] == 3


@pytest.mark.unit
@pytest.mark.parametrize("existing,new_item,is_dup", [
    (["Milk"], "Milk", True),
    (["Milk"], "milk", True),
    (["Milk"], "MILK", True),
    (["Milk"], "  Milk  ", True),
    (["Milk"], "Butter", False),
    ([], "Milk", False),
])
def test_duplication_parametrized(existing, new_item, is_dup):
    """Parametrized deduplication tests"""
    assert is_duplicate(new_item, existing) == is_dup
```

### Step 2: Run Tests (TDD Red)
```bash
pytest tests/test_deduplication.py -v
```

### Step 3: Implement Functions (TDD Green)
Implement is_duplicate(), get_existing_items(), add_items_to_list() in app.py

### Step 4: Verify Tests Pass
```bash
pytest tests/test_deduplication.py -v --cov=app
```

---

## Phase 3: Integration Tests for API Endpoints

### When: After basic Flask routes are implemented

### Step 1: Create test_api_endpoints.py
Create `/home/user/groceryclaude/tests/test_api_endpoints.py`:

```python
"""
Integration tests for API endpoints
"""
import pytest
import json


@pytest.mark.integration
class TestAddItemEndpoint:
    """Test /add-item endpoint"""

    def test_add_single_item(self, client):
        """Test adding a single item"""
        response = client.post('/add-item',
                              data=json.dumps({'text': 'milk'}),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['added'] == 1
        assert "Milk" in data['items_added']

    def test_add_multiple_items(self, client):
        """Test adding multiple items"""
        response = client.post('/add-item',
                              data=json.dumps({'text': 'milk, eggs, bread'}),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['added'] == 3

    def test_natural_language(self, client):
        """Test natural language input"""
        response = client.post('/add-item',
                              data=json.dumps({'text': 'We need milk and eggs'}),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['added'] == 2

    def test_missing_text_field(self, client):
        """Test error when 'text' field is missing"""
        response = client.post('/add-item',
                              data=json.dumps({}),
                              content_type='application/json')

        assert response.status_code == 400

    def test_malformed_json(self, client):
        """Test error handling for malformed JSON"""
        response = client.post('/add-item',
                              data='not json',
                              content_type='application/json')

        assert response.status_code == 400

    def test_duplicate_prevention(self, client):
        """Test that duplicates are prevented"""
        # Add items first time
        client.post('/add-item',
                   data=json.dumps({'text': 'milk, eggs'}),
                   content_type='application/json')

        # Try to add same items again
        response = client.post('/add-item',
                              data=json.dumps({'text': 'milk, eggs'}),
                              content_type='application/json')

        data = json.loads(response.data)
        assert data['added'] == 0
        assert data['duplicates'] == 2


@pytest.mark.integration
class TestDeleteItemEndpoint:
    """Test /delete-item endpoint"""

    def test_delete_existing_item(self, client):
        """Test deleting an existing item"""
        # Add items first
        client.post('/add-item',
                   data=json.dumps({'text': 'milk, eggs, bread'}),
                   content_type='application/json')

        # Delete one item
        response = client.post('/delete-item',
                              data=json.dumps({'item': 'Milk'}),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True

        # Verify item is deleted
        get_response = client.get('/get-items')
        items = json.loads(get_response.data)
        assert 'Milk' not in items

    def test_delete_nonexistent_item(self, client):
        """Test deleting an item that doesn't exist"""
        response = client.post('/delete-item',
                              data=json.dumps({'item': 'NonExistent'}),
                              content_type='application/json')

        assert response.status_code == 404


@pytest.mark.integration
class TestGetItemsEndpoint:
    """Test /get-items endpoint"""

    def test_get_empty_list(self, client):
        """Test getting items from empty list"""
        response = client.get('/get-items')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_get_populated_list(self, client):
        """Test getting items from populated list"""
        client.post('/add-item',
                   data=json.dumps({'text': 'milk, eggs, bread'}),
                   content_type='application/json')

        response = client.get('/get-items')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert set(data) == {'Milk', 'Eggs', 'Bread'}
```

### Step 2: Run Tests
```bash
pytest tests/test_api_endpoints.py -v
```

---

## Phase 4: End-to-End Integration Tests

### Step 1: Create test_integration.py
Create `/home/user/groceryclaude/tests/test_integration.py`:

```python
"""
End-to-end integration tests
"""
import pytest
import json


@pytest.mark.e2e
class TestCompleteUserJourney:
    """Test complete user journeys"""

    def test_add_view_delete_journey(self, client):
        """Test complete add -> view -> delete journey"""
        # Add items via API
        add_response = client.post('/add-item',
                                   data=json.dumps({'text': 'milk, eggs, bread'}),
                                   content_type='application/json')
        assert add_response.status_code == 200

        # Get items via API
        get_response = client.get('/get-items')
        items = json.loads(get_response.data)
        assert set(items) == {'Milk', 'Eggs', 'Bread'}

        # Delete one item
        delete_response = client.post('/delete-item',
                                      data=json.dumps({'item': 'Milk'}),
                                      content_type='application/json')
        assert delete_response.status_code == 200

        # Verify deletion
        get_response2 = client.get('/get-items')
        items2 = json.loads(get_response2.data)
        assert 'Milk' not in items2
        assert set(items2) == {'Eggs', 'Bread'}

    def test_multiple_additions_with_duplicates(self, client):
        """Test multiple additions with duplicate detection"""
        # First addition
        client.post('/add-item', json={'text': 'milk, eggs'})

        # Second addition with partial duplicates
        client.post('/add-item', json={'text': 'eggs, bread, butter'})

        # Third addition all duplicates
        response3 = client.post('/add-item', json={'text': 'milk, eggs'})
        data3 = json.loads(response3.data)
        assert data3['duplicates'] == 2

        # Verify final state
        items = json.loads(client.get('/get-items').data)
        assert set(items) == {'Milk', 'Eggs', 'Bread', 'Butter'}


@pytest.mark.e2e
class TestErrorRecovery:
    """Test error recovery scenarios"""

    def test_empty_file_auto_creation(self, client, temp_grocery_file):
        """Test that missing file is auto-created"""
        import os
        from app import app

        # Ensure file doesn't exist
        if os.path.exists(temp_grocery_file):
            os.remove(temp_grocery_file)

        app.config['GROCERY_LIST_FILE'] = temp_grocery_file

        # Try to add item (should create file)
        response = client.post('/add-item', json={'text': 'milk'})
        assert response.status_code == 200

        # Verify file was created
        assert os.path.exists(temp_grocery_file)
```

### Step 2: Run E2E Tests
```bash
pytest tests/test_integration.py -v -m e2e
```

---

## Phase 5: Regression Tests

### Step 1: Create test_regression.py
Create `/home/user/groceryclaude/tests/test_regression.py`:

```python
"""
Regression tests - ensure core functionality never breaks
"""
import pytest
import json


@pytest.mark.regression
@pytest.mark.critical
class TestCriticalPaths:
    """Critical functionality that must always work"""

    def test_can_add_items(self, client):
        """CRITICAL: Must be able to add items"""
        response = client.post('/add-item', json={'text': 'milk'})
        assert response.status_code == 200
        items = json.loads(client.get('/get-items').data)
        assert 'Milk' in items

    def test_can_delete_items(self, client):
        """CRITICAL: Must be able to delete items"""
        client.post('/add-item', json={'text': 'milk'})
        response = client.post('/delete-item', json={'item': 'Milk'})
        assert response.status_code == 200

    def test_can_get_items(self, client):
        """CRITICAL: Must be able to retrieve items"""
        client.post('/add-item', json={'text': 'milk'})
        response = client.get('/get-items')
        assert response.status_code == 200
        assert isinstance(json.loads(response.data), list)


@pytest.mark.regression
class TestRegressionSuite:
    """Regression tests for all features"""

    def test_basic_parsing_still_works(self):
        """Regression: Basic parsing functionality"""
        from app import parse_grocery_text
        assert parse_grocery_text("milk, eggs, bread") == ["Milk", "Eggs", "Bread"]

    def test_deduplication_still_works(self, client):
        """Regression: Deduplication functionality"""
        client.post('/add-item', json={'text': 'milk'})
        response = client.post('/add-item', json={'text': 'milk'})
        data = json.loads(response.data)
        assert data['duplicates'] == 1
```

---

## Phase 6: Performance Tests

### Step 1: Create test_performance.py
Create `/home/user/groceryclaude/tests/test_performance.py`:

```python
"""
Performance tests
"""
import pytest
import time


@pytest.mark.slow
@pytest.mark.performance
class TestPerformance:
    """Performance benchmarks"""

    def test_add_100_items_performance(self, client):
        """Test performance when adding 100 items"""
        items = [f"Item{i}" for i in range(100)]
        text = ", ".join(items)

        start = time.time()
        response = client.post('/add-item', json={'text': text})
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 2.0, f"Too slow: {elapsed}s"

    def test_read_large_list_performance(self, large_grocery_file, client):
        """Test reading large list"""
        from app import app
        app.config['GROCERY_LIST_FILE'] = large_grocery_file

        start = time.time()
        response = client.get('/get-items')
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 1.0, f"Too slow: {elapsed}s"
```

---

## Running the Complete Test Suite

### Quick Development Cycle
```bash
# Watch mode - auto-run on file change
ptw -- tests/ -v -m "not slow"
```

### Before Commit
```bash
# Fast tests only
pytest tests/ -v -m "not slow and not e2e" --cov=app
```

### Full Test Suite
```bash
# All tests with coverage
pytest tests/ -v --cov=app --cov-report=html
```

### Performance Tests Only
```bash
pytest tests/test_performance.py -v -m performance
```

### Critical Tests Only
```bash
pytest tests/ -v -m critical
```

---

## Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| parse_grocery_text() | 100% |
| Deduplication functions | 100% |
| API endpoints | 90% |
| File operations | 90% |
| Overall | 85%+ |

---

## Next Steps After Implementation

1. **Generate Coverage Report**
   ```bash
   pytest tests/ --cov=app --cov-report=html
   open htmlcov/index.html
   ```

2. **Identify Coverage Gaps**
   - Look for red lines in coverage report
   - Add tests for uncovered code paths

3. **Manual Testing**
   - Follow frontend testing checklist
   - Test iOS Shortcut integration

4. **Performance Validation**
   - Run performance tests
   - Ensure all benchmarks are met

5. **Documentation**
   - Document any test failures or issues
   - Update test cases based on findings

---

## Troubleshooting

### Tests fail with ModuleNotFoundError
**Solution:** Ensure app.py is in Python path
```python
# In conftest.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
```

### Fixtures not found
**Solution:** Ensure conftest.py is in root directory

### Tests pass locally but fail in CI
**Solution:** Use absolute paths, not relative
```python
app.config['GROCERY_LIST_FILE'] = os.path.join(
    os.path.dirname(__file__), 'grocery_list.txt'
)
```

### Coverage reports show 0%
**Solution:** Ensure you're covering the right module
```bash
pytest tests/ --cov=app  # Not --cov=tests
```

---

## Success Checklist

- [ ] pytest.ini configured
- [ ] conftest.py with fixtures created
- [ ] test_parsing.py implemented and passing
- [ ] test_deduplication.py implemented and passing
- [ ] test_api_endpoints.py implemented and passing
- [ ] test_integration.py implemented and passing
- [ ] test_regression.py implemented and passing
- [ ] test_performance.py implemented and passing
- [ ] Coverage ≥ 90% for critical functions
- [ ] All critical tests passing
- [ ] Pre-commit hook configured
- [ ] Manual frontend tests completed
- [ ] iOS integration tests completed

---

This roadmap provides a clear path from zero tests to a comprehensive test suite. Follow the phases in order, using TDD where possible (write tests first, then implement features).
