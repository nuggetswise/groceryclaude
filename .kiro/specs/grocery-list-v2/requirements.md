# Requirements Document - Smart Grocery List v2

## Introduction

Enhanced grocery list application with AI-powered parsing, categorization, shopping trip tracking, and purchase history. Users can manage multiple shopping trips per week, track when items were last purchased, and maintain a 4-week history of shopping activities.

## Glossary

- **System**: The Smart Grocery List web application
- **User**: Person using the application to manage grocery shopping
- **Current List**: Active shopping list for the current/upcoming trip
- **Shopping Trip**: A completed shopping session with checked-off items
- **Item**: A grocery product (e.g., "Apples", "Milk")
- **Category**: Grouping of similar items (e.g., Produce, Dairy, Meat)
- **History**: Archive of past shopping trips (last 4 weeks)
- **Gemini AI**: Google's LLM used for natural language parsing
- **Item Stats**: Metadata tracking purchase frequency and last bought date

## Requirements

### Requirement 1: Enhanced Input Field Visibility

**User Story:** As a user, I want to immediately see where to add items, so that I can quickly start building my grocery list.

#### Acceptance Criteria

1. WHEN the user opens the application, THE System SHALL display a prominent input field at the top of the interface
2. THE System SHALL style the input field with high visual contrast and clear placeholder text
3. THE System SHALL position the input field above all other content with minimum 20px padding
4. THE System SHALL display the input field with a minimum height of 50px for easy mobile interaction
5. THE System SHALL include a visually distinct "Add" button adjacent to the input field

---

### Requirement 2: Item Categorization

**User Story:** As a user, I want my grocery items automatically organized by category, so that I can shop more efficiently in the store.

#### Acceptance Criteria

1. WHEN an item is added to the list, THE System SHALL automatically assign it to one of the predefined categories
2. THE System SHALL support the following categories: Produce, Dairy, Meat & Seafood, Bakery, Pantry, Frozen, Household, Snacks, Beverages, Other
3. THE System SHALL display items grouped by category with category headers
4. THE System SHALL display category icons/emojis for visual identification
5. WHERE a category has no items, THE System SHALL hide that category section
6. THE System SHALL use Gemini AI to determine the appropriate category for each item

---

### Requirement 3: Non-Destructive Item Checking

**User Story:** As a user, I want to check off items as I shop without deleting them, so that I can see what I've bought and undo mistakes.

#### Acceptance Criteria

1. WHEN the user taps/clicks an item checkbox, THE System SHALL toggle the item between checked and unchecked states
2. WHEN an item is checked, THE System SHALL apply a strike-through style to the item text
3. WHEN an item is checked, THE System SHALL update the checkbox to show a checkmark icon
4. WHEN an item is unchecked, THE System SHALL remove the strike-through style
5. THE System SHALL NOT delete items when they are checked
6. THE System SHALL persist the checked state in the data storage

---

### Requirement 4: Shopping Trip Management

**User Story:** As a user, I want to complete my shopping trip and start a fresh list, so that I can track multiple shopping sessions per week.

#### Acceptance Criteria

1. THE System SHALL display a "Complete Shopping Trip" button below the current list
2. WHEN the user clicks "Complete Shopping Trip", THE System SHALL move all current items to history with the current date
3. WHEN a trip is completed, THE System SHALL create a new empty current list
4. WHEN a trip is completed, THE System SHALL display a confirmation message showing the number of items archived
5. THE System SHALL only enable the "Complete Shopping Trip" button when at least one item exists in the current list
6. THE System SHALL record the completion timestamp for each shopping trip

---

### Requirement 5: Purchase History Tracking

**User Story:** As a user, I want to see when I last bought each item, so that I know if I need to reorder it.

#### Acceptance Criteria

1. WHEN an item is displayed in the current list, THE System SHALL show "Last bought: X days ago" if the item was purchased before
2. THE System SHALL calculate the days since last purchase based on the most recent shopping trip containing that item
3. WHERE an item has never been purchased, THE System SHALL display "Never bought before"
4. THE System SHALL update the "last bought" information when a shopping trip is completed
5. THE System SHALL track purchase frequency for each item across all shopping trips

---

### Requirement 6: Shopping History Display

**User Story:** As a user, I want to view my past shopping trips, so that I can see what I bought and when.

#### Acceptance Criteria

1. THE System SHALL display a "History" section below the current list
2. THE System SHALL show shopping trips from the last 4 weeks only
3. THE System SHALL display each trip with its date and list of items
4. THE System SHALL show checked items with strike-through in the history
5. THE System SHALL display trips in reverse chronological order (newest first)
6. THE System SHALL allow the history section to be collapsed/expanded
7. WHEN history exceeds 4 weeks, THE System SHALL automatically remove older trips

---

### Requirement 7: Item Statistics and Insights

**User Story:** As a user, I want to see patterns in my shopping habits, so that I can better plan my grocery trips.

#### Acceptance Criteria

1. THE System SHALL track the total number of times each item has been purchased
2. THE System SHALL calculate the average frequency (in days) between purchases for each item
3. WHERE an item is purchased regularly, THE System SHALL display a frequency indicator (e.g., "Weekly", "Every 3 days")
4. THE System SHALL store item statistics in persistent storage
5. THE System SHALL update statistics when a shopping trip is completed

---

### Requirement 8: Data Persistence and Structure

**User Story:** As a developer, I need a robust data structure to support trip tracking and history, so that the system can scale and maintain data integrity.

#### Acceptance Criteria

1. THE System SHALL store data in JSON format instead of plain text
2. THE System SHALL maintain separate objects for current list, history, and item statistics
3. THE System SHALL include timestamps for all item additions and trip completions
4. THE System SHALL validate data structure on read and write operations
5. THE System SHALL handle migration from the old text-based format to the new JSON format
6. THE System SHALL implement atomic write operations to prevent data corruption

---

### Requirement 9: Enhanced AI Parsing with Category Detection

**User Story:** As a user, I want the AI to not only extract items but also categorize them automatically, so that I don't have to organize my list manually.

#### Acceptance Criteria

1. WHEN text is submitted to the add-item endpoint, THE System SHALL use Gemini AI to extract both item names and categories
2. THE System SHALL provide the AI with the list of valid categories
3. THE System SHALL handle cases where the AI cannot determine a category by defaulting to "Other"
4. THE System SHALL maintain the existing parsing rules (remove quantities, filler words, normalize case)
5. THE System SHALL return both item name and category in the API response

---

### Requirement 10: Item Deletion (Swipe/Button)

**User Story:** As a user, I want to permanently remove items I don't need, so that my list stays clean and relevant.

#### Acceptance Criteria

1. THE System SHALL provide a delete button that appears on hover (desktop) or is always visible (mobile)
2. WHEN the user clicks the delete button, THE System SHALL remove the item from the current list
3. THE System SHALL display a confirmation toast message after deletion
4. THE System SHALL NOT remove items from history when deleted from current list
5. THE System SHALL support swipe-left gesture on mobile to reveal delete button

---

### Requirement 11: Copy from Previous Trip

**User Story:** As a user, I want to quickly add items from my last shopping trip, so that I can save time on recurring purchases.

#### Acceptance Criteria

1. THE System SHALL display a "Copy from Last Trip" button when history exists
2. WHEN the user clicks "Copy from Last Trip", THE System SHALL add all items from the most recent trip to the current list
3. THE System SHALL avoid duplicates when copying items
4. THE System SHALL display a confirmation message showing how many items were copied
5. THE System SHALL maintain the original categories when copying items

---

### Requirement 12: Responsive Mobile-First Design

**User Story:** As a user, I want the app to work seamlessly on my phone, so that I can use it while shopping in the store.

#### Acceptance Criteria

1. THE System SHALL display optimally on screen sizes from 320px to 1920px width
2. THE System SHALL use touch-friendly tap targets (minimum 44px)
3. THE System SHALL display category sections in a single column on mobile
4. THE System SHALL show delete buttons without requiring hover on mobile devices
5. THE System SHALL support swipe gestures for item interactions on touch devices

---

### Requirement 13: Empty State Improvements

**User Story:** As a user, I want helpful guidance when my list is empty, so that I know what to do next.

#### Acceptance Criteria

1. WHEN the current list is empty, THE System SHALL display an empty state message
2. THE System SHALL show example inputs in the empty state
3. WHERE history exists but current list is empty, THE System SHALL suggest copying from last trip
4. THE System SHALL display the empty state with appropriate iconography
5. THE System SHALL hide the empty state when items are added

---

### Requirement 14: API Enhancements

**User Story:** As a developer, I need enhanced API endpoints to support the new features, so that the frontend can access all necessary data.

#### Acceptance Criteria

1. THE System SHALL provide a GET /get-current-list endpoint returning current items with categories and metadata
2. THE System SHALL provide a GET /get-history endpoint returning the last 4 weeks of trips
3. THE System SHALL provide a POST /complete-trip endpoint to archive the current list
4. THE System SHALL provide a POST /toggle-item endpoint to check/uncheck items
5. THE System SHALL provide a POST /copy-from-last-trip endpoint
6. THE System SHALL provide a GET /get-item-stats endpoint for purchase frequency data
7. THE System SHALL return appropriate HTTP status codes and error messages for all endpoints

---

### Requirement 15: Performance and Optimization

**User Story:** As a user, I want the app to respond quickly, so that I can efficiently manage my grocery list.

#### Acceptance Criteria

1. THE System SHALL respond to item additions within 2 seconds (including AI processing)
2. THE System SHALL load the current list within 500ms
3. THE System SHALL handle lists with up to 100 items without performance degradation
4. THE System SHALL cache item statistics to avoid recalculation on every request
5. THE System SHALL implement debouncing for rapid user interactions

---

## Success Metrics

1. **User Engagement:** Users complete shopping trips at least 2x per week
2. **Data Accuracy:** 95%+ accuracy in AI category assignment
3. **Performance:** 90% of operations complete within target time
4. **User Satisfaction:** Intuitive UX with minimal learning curve
5. **Data Integrity:** Zero data loss incidents over 4-week period

---

## Out of Scope (Future Enhancements)

- Multi-user support / shared lists
- Recipe integration
- Price tracking
- Store-specific lists
- Barcode scanning
- Voice input
- Push notifications for recurring items
- Export to other formats
- Integration with delivery services

---

**Document Version:** 1.0  
**Created:** 2025-10-30  
**Status:** ✅ Ready for Design Phase
