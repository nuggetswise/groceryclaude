# Testing Quick Reference Guide

## Essential Test Commands

### Setup
```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov pytest-watch

# Create test directory structure
mkdir -p tests/fixtures tests/test_grocery_lists
touch tests/__init__.py tests/fixtures/__init__.py
```

### Run Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run fast tests only (pre-commit)
pytest tests/ -v -m "not slow and not e2e"

# Run specific test file
pytest tests/test_parsing.py -v

# Run specific test
pytest tests/test_parsing.py::test_comma_separated_items -v

# Run tests matching keyword
pytest tests/ -k "duplicate" -v

# Run by marker
pytest tests/ -m unit -v
pytest tests/ -m integration -v
pytest tests/ -m e2e -v
pytest tests/ -m performance -v

# Auto-run tests on file change
ptw -- tests/ -v
```

### Coverage

```bash
# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Generate terminal coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Coverage for specific file
pytest tests/test_parsing.py --cov=app.parse_grocery_text
```

## Test Priorities (TL;DR)

### Priority 1: Unit Tests (Run First)
- ✅ Parsing function: `pytest tests/test_parsing.py -v`
- ✅ Deduplication: `pytest tests/test_deduplication.py -v`

### Priority 2: Integration Tests
- ✅ API endpoints: `pytest tests/test_api_endpoints.py -v`

### Priority 3: Manual Frontend Tests
- ✅ Follow checklist in TESTING_STRATEGY.md (15 min)

### Priority 4: iOS Integration
- ✅ Deploy and test with real device (20 min)

### Priority 5: E2E & Regression
- ✅ Full scenarios: `pytest tests/ -v -m e2e`
- ✅ Regression: `pytest tests/ -v -m regression`

## Critical Test Cases (Must Pass)

### Parsing
```python
# Test: Basic comma separation
Input: "milk, eggs, bread"
Expected: ["Milk", "Eggs", "Bread"]

# Test: Natural language
Input: "We need milk and eggs"
Expected: ["Milk", "Eggs"]

# Test: Quantity removal
Input: "2 gallons of milk"
Expected: ["Milk"]
```

### Deduplication
```python
# Test: Case insensitive
Existing: ["Milk"]
New: "milk"
Expected: Duplicate detected, not added

# Test: Whitespace trimming
Existing: ["Milk"]
New: "  Milk  "
Expected: Duplicate detected, not added
```

### API Endpoints
```bash
# Test: Add item
curl -X POST http://localhost:5000/add-item \
  -H "Content-Type: application/json" \
  -d '{"text":"milk, eggs"}'
Expected: {"success": true, "added": 2, ...}

# Test: Get items
curl http://localhost:5000/get-items
Expected: ["Milk", "Eggs"]

# Test: Delete item
curl -X POST http://localhost:5000/delete-item \
  -H "Content-Type: application/json" \
  -d '{"item":"Milk"}'
Expected: {"success": true}
```

## Manual Test Checklist

### Before Every Commit
- [ ] Run: `pytest tests/ -v -m "not slow"`
- [ ] Check: Code coverage ≥ 90%
- [ ] Verify: No console errors
- [ ] Test: Basic add/delete via curl

### Before Deployment
- [ ] Run: `pytest tests/ -v --cov=app`
- [ ] Check: All tests pass
- [ ] Test: Frontend manually in browser
- [ ] Test: iOS Shortcut integration
- [ ] Verify: Performance benchmarks met
- [ ] Review: Coverage report

### iOS Shortcut Testing
1. [ ] Deploy to Replit
2. [ ] Create/update iOS Shortcut with URL
3. [ ] Test: "We need milk"
4. [ ] Test: "milk, eggs, bread"
5. [ ] Test: Duplicate prevention
6. [ ] Test: Complex message
7. [ ] Test: Error handling (server down)
8. [ ] Verify: Response time < 3 seconds

## Test Data Examples

### Good Test Inputs
```python
"milk"
"milk, eggs, bread"
"We need milk and eggs"
"2 gallons of milk"
"Can you grab some cheddar cheese?"
"We're out of milk"
```

### Edge Cases to Test
```python
""  # Empty string
"   "  # Whitespace only
"we need the a"  # Only filler words
"123"  # Numbers only
"!!!"  # Special characters only
```

### Expected Parsing Results
```python
"milk, eggs, bread" → ["Milk", "Eggs", "Bread"]
"We need milk" → ["Milk"]
"2 gallons of milk" → ["Milk"]
"cheddar cheese" → ["Cheddar Cheese"]
"" → []
```

## Performance Benchmarks

| Operation | Target | Test Command |
|-----------|--------|--------------|
| Add 1 item | < 0.1s | `pytest tests/test_performance.py::test_add_single_item` |
| Add 100 items | < 2.0s | `pytest tests/test_performance.py::test_add_100_items` |
| Get 1000 items | < 1.0s | `pytest tests/test_performance.py::test_read_large_list` |
| Delete from 1000 | < 0.5s | `pytest tests/test_performance.py::test_delete_from_large_list` |

## Common Issues & Solutions

### Issue: Tests fail with "No such file"
**Solution:** Ensure temp file fixtures are used correctly
```python
@pytest.fixture
def temp_grocery_file():
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)
```

### Issue: Tests pass locally but fail in CI
**Solution:** Check file paths are absolute, not relative
```python
# Bad
grocery_file = 'grocery_list.txt'

# Good
grocery_file = os.path.join(os.path.dirname(__file__), 'grocery_list.txt')
```

### Issue: Coverage report shows missing lines
**Solution:** Add tests for edge cases and error handling
```bash
# See which lines are missing
pytest --cov=app --cov-report=term-missing
```

## Test Markers Reference

```python
# In pytest.ini
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    performance: Performance tests
    regression: Regression tests
    critical: Critical path tests

# Usage in test files
@pytest.mark.unit
def test_something():
    pass

@pytest.mark.slow
@pytest.mark.performance
def test_large_list():
    pass
```

## Fixture Reference

```python
# conftest.py fixtures

@pytest.fixture
def client():
    """Flask test client"""
    # Auto cleanup, use for API tests

@pytest.fixture
def temp_grocery_file():
    """Empty temp file"""
    # Auto cleanup, use for file operations

@pytest.fixture
def populated_grocery_file(temp_grocery_file):
    """Temp file with sample data"""
    # Contains: Milk, Eggs, Bread, Butter, Cheese
```

## Debugging Tests

```bash
# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Run last failed tests
pytest tests/ --lf

# Drop into debugger on failure
pytest tests/ --pdb

# Show slowest 10 tests
pytest tests/ --durations=10
```

## Pre-commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "Running pre-commit tests..."
pytest tests/ -v -m "not slow and not e2e" -x
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi
echo "✅ All tests passed!"
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## CI/CD GitHub Actions

Minimal `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-flask pytest-cov
      - run: pytest tests/ -v --cov=app
```

## Success Criteria

### Code Coverage
- **Target**: ≥ 90% overall
- **Critical functions**: 100% (parsing, deduplication)
- **API endpoints**: ≥ 90%

### Test Execution Time
- **Unit tests**: < 10 seconds
- **Integration tests**: < 20 seconds
- **All tests**: < 30 seconds
- **With performance tests**: < 90 seconds

### Test Results
- **Unit tests**: 100% pass rate
- **Integration tests**: 100% pass rate
- **iOS integration**: 100% success for test messages
- **Regression tests**: 0 failures

## When to Run What

### Every Code Change (During Development)
```bash
ptw -- tests/ -v  # Auto-run on file change
```

### Before Every Commit
```bash
pytest tests/ -v -m "not slow and not e2e" --cov=app
```

### Before Push to Main
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Before Deployment
```bash
pytest tests/ -v --cov=app
# Then manually test iOS integration
```

### After Deployment
- Manual smoke tests
- iOS Shortcut integration test
- Verify web UI works

## Key Files

| File | Purpose |
|------|---------|
| `tests/test_parsing.py` | Unit tests for parsing function |
| `tests/test_deduplication.py` | Unit tests for deduplication |
| `tests/test_api_endpoints.py` | Integration tests for API |
| `tests/test_integration.py` | End-to-end scenarios |
| `tests/test_regression.py` | Regression test suite |
| `tests/test_performance.py` | Performance benchmarks |
| `tests/conftest.py` | Shared fixtures |
| `tests/fixtures/test_data.py` | Test data constants |
| `pytest.ini` | Pytest configuration |

## Resources

- Full strategy: See `TESTING_STRATEGY.md`
- Requirements: See `claude.md`
- Pytest docs: https://docs.pytest.org/
- Flask testing: https://flask.palletsprojects.com/en/2.3.x/testing/
