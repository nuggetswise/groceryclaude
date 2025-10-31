// DOM Elements
const itemInput = document.getElementById('item-input');
const addForm = document.getElementById('add-form');
const groceryListContainer = document.getElementById('grocery-list-container');
const emptyState = document.getElementById('empty-state');
const loading = document.getElementById('loading');
const itemCount = document.getElementById('item-count');
const clearAllBtn = document.getElementById('clear-all');
const completeTripBtn = document.getElementById('complete-trip-btn');
const completeTripSection = document.getElementById('complete-trip-section');
const historySection = document.getElementById('history-section');
const historyContent = document.getElementById('history-content');
const copyLastTripBtn = document.getElementById('copy-last-trip-btn');
const toast = document.getElementById('toast');

// State
let currentList = {
    categories: {},
    totalItems: 0,
    checkedItems: 0
};

// Category emoji mapping
const CATEGORY_EMOJIS = {
    "Produce": "🍎",
    "Dairy": "🥛",
    "Meat & Seafood": "🥩",
    "Bakery": "🍞",
    "Pantry": "🥫",
    "Frozen": "🧊",
    "Household": "🧴",
    "Snacks": "🍫",
    "Beverages": "🥤",
    "Other": "📦"
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadItems();
    loadHistory();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    addForm.addEventListener('submit', handleAddItem);
    clearAllBtn.addEventListener('click', handleClearAll);
    completeTripBtn.addEventListener('click', handleCompleteTrip);
    copyLastTripBtn.addEventListener('click', handleCopyFromLastTrip);
}

// Load items from server (v2)
async function loadItems() {
    try {
        const response = await fetch('/get-current-list');
        currentList = await response.json();
        renderItems();
    } catch (error) {
        console.error('Error loading items:', error);
        showToast('Failed to load items', 'error');
    }
}

// Render items to DOM (v2 - categorized)
function renderItems() {
    // Update count
    itemCount.textContent = currentList.totalItems;

    // Show/hide empty state
    if (currentList.totalItems === 0) {
        groceryListContainer.classList.add('hidden');
        completeTripSection.style.display = 'none';
        emptyState.classList.add('show');
        return;
    }

    emptyState.classList.remove('show');
    groceryListContainer.classList.remove('hidden');
    
    // Show complete trip button if there are items
    completeTripSection.style.display = 'block';

    // Clear container
    groceryListContainer.innerHTML = '';

    // Render each category
    for (const [categoryName, items] of Object.entries(currentList.categories)) {
        if (items.length === 0) continue;

        const categorySection = createCategorySection(categoryName, items);
        groceryListContainer.appendChild(categorySection);
    }
}

// Create category section
function createCategorySection(categoryName, items) {
    const section = document.createElement('div');
    section.className = 'category-section';
    
    const emoji = CATEGORY_EMOJIS[categoryName] || '📦';
    
    section.innerHTML = `
        <div class="category-header">
            <span class="category-emoji">${emoji}</span>
            <span class="category-name">${categoryName}</span>
            <span class="category-count">${items.length}</span>
        </div>
        <ul class="category-items"></ul>
    `;
    
    const itemsList = section.querySelector('.category-items');
    items.forEach(item => {
        const li = createItemElement(item);
        itemsList.appendChild(li);
    });
    
    return section;
}

// Create item element (v2 - with checkbox)
function createItemElement(item) {
    const li = document.createElement('li');
    li.className = 'grocery-item';
    if (item.checked) {
        li.classList.add('checked');
    }
    li.dataset.itemId = item.id;

    const checkmarkSvg = item.checked 
        ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        : '';

    // Build metadata string
    let metadataHtml = '';
    if (item.lastBought && item.daysSinceLastBought !== null) {
        metadataHtml = `<span class="item-metadata">Last bought: ${item.daysSinceLastBought} days ago</span>`;
    } else if (item.frequency) {
        metadataHtml = `<span class="item-metadata">${item.frequency}</span>`;
    }

    li.innerHTML = `
        <div class="item-content">
            <div class="item-checkbox ${item.checked ? 'checked' : ''}">
                ${checkmarkSvg}
            </div>
            <div class="item-details">
                <span class="item-name ${item.checked ? 'checked' : ''}">${escapeHtml(item.name)}</span>
                ${metadataHtml}
            </div>
        </div>
        <button class="delete-btn" title="Delete item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    `;

    // Click checkbox area to toggle
    const checkbox = li.querySelector('.item-checkbox');
    const itemContent = li.querySelector('.item-content');
    
    itemContent.addEventListener('click', (e) => {
        if (!e.target.closest('.delete-btn')) {
            handleToggleItem(item.id, li);
        }
    });

    // Delete button
    const deleteBtn = li.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        handleDeleteItem(item.id, li);
    });

    return li;
}

// Handle add item
async function handleAddItem(e) {
    e.preventDefault();

    const text = itemInput.value.trim();
    if (!text) return;

    // Show loading
    loading.classList.add('show');
    itemInput.disabled = true;

    try {
        const response = await fetch('/add-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();

        if (data.success) {
            // Show feedback
            if (data.added.length > 0) {
                const addedText = data.added.length === 1 
                    ? `Added: ${data.added[0]}` 
                    : `Added ${data.added.length} items`;
                showToast(addedText, 'success');
            }

            if (data.skipped.length > 0) {
                const skippedText = data.skipped.length === 1
                    ? `${data.skipped[0]} already in list`
                    : `${data.skipped.length} items already in list`;
                setTimeout(() => showToast(skippedText, 'warning'), 2000);
            }

            if (data.added.length === 0 && data.skipped.length === 0) {
                showToast('No items found in text', 'warning');
            }

            // Clear input and reload
            itemInput.value = '';
            await loadItems();
        } else {
            showToast(data.error || 'Failed to add items', 'error');
        }
    } catch (error) {
        console.error('Error adding item:', error);
        showToast('Failed to add items', 'error');
    } finally {
        loading.classList.remove('show');
        itemInput.disabled = false;
        itemInput.focus();
    }
}

// Handle toggle item (v2)
async function handleToggleItem(itemId, element) {
    try {
        const response = await fetch('/toggle-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ itemId }),
        });

        const data = await response.json();

        if (data.success) {
            // Update UI immediately
            const checkbox = element.querySelector('.item-checkbox');
            const itemName = element.querySelector('.item-name');
            
            if (data.checked) {
                element.classList.add('checked');
                checkbox.classList.add('checked');
                itemName.classList.add('checked');
                checkbox.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            } else {
                element.classList.remove('checked');
                checkbox.classList.remove('checked');
                itemName.classList.remove('checked');
                checkbox.innerHTML = '';
            }
            
            // Reload to update counts
            await loadItems();
        } else {
            showToast('Failed to toggle item', 'error');
        }
    } catch (error) {
        console.error('Error toggling item:', error);
        showToast('Failed to toggle item', 'error');
    }
}

// Handle delete item (v2)
async function handleDeleteItem(itemId, element) {
    // Animate out
    element.classList.add('deleting');

    try {
        const response = await fetch('/delete-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ itemId }),
        });

        const data = await response.json();

        if (data.success) {
            // Wait for animation
            setTimeout(async () => {
                await loadItems();
                showToast(`Deleted: ${data.deleted}`, 'success');
            }, 300);
        } else {
            element.classList.remove('deleting');
            showToast('Failed to delete item', 'error');
        }
    } catch (error) {
        console.error('Error deleting item:', error);
        element.classList.remove('deleting');
        showToast('Failed to delete item', 'error');
    }
}

// Handle clear all (v2)
async function handleClearAll() {
    if (currentList.totalItems === 0) return;

    if (!confirm(`Delete all ${currentList.totalItems} items?`)) {
        return;
    }

    try {
        const response = await fetch('/clear-all', {
            method: 'POST',
        });

        const data = await response.json();

        if (data.success) {
            await loadItems();
            showToast('All items cleared', 'success');
        } else {
            showToast('Failed to clear items', 'error');
        }
    } catch (error) {
        console.error('Error clearing items:', error);
        showToast('Failed to clear items', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle complete trip
async function handleCompleteTrip() {
    if (currentList.totalItems === 0) return;

    const checkedCount = currentList.checkedItems || 0;
    const message = checkedCount > 0 
        ? `Complete trip with ${checkedCount} of ${currentList.totalItems} items checked off?`
        : `Complete trip? (No items are checked off yet)`;

    if (!confirm(message)) {
        return;
    }

    try {
        const response = await fetch('/complete-trip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();

        if (data.success) {
            await loadItems();
            await loadHistory(); // Reload history after completing trip
            showToast(data.message, 'success');
        } else {
            showToast(data.error || 'Failed to complete trip', 'error');
        }
    } catch (error) {
        console.error('Error completing trip:', error);
        showToast('Failed to complete trip', 'error');
    }
}

// Load shopping history
async function loadHistory() {
    try {
        const response = await fetch('/get-history');
        const data = await response.json();
        renderHistory(data);
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Render history to DOM
function renderHistory(historyData) {
    // Show/hide history section
    if (historyData.totalTrips === 0) {
        historySection.style.display = 'none';
        return;
    }

    historySection.style.display = 'block';
    copyLastTripBtn.style.display = 'inline-flex';

    // Clear content
    historyContent.innerHTML = '';

    // Render each trip
    historyData.trips.forEach(trip => {
        const tripElement = createTripElement(trip);
        historyContent.appendChild(tripElement);
    });
}

// Create trip element
function createTripElement(trip) {
    const div = document.createElement('div');
    div.className = 'history-trip';
    
    const tripDate = new Date(trip.completedAt).toLocaleDateString();
    const daysAgoText = trip.daysAgo === 0 ? 'Today' : 
                       trip.daysAgo === 1 ? 'Yesterday' : 
                       `${trip.daysAgo} days ago`;

    // Create items summary
    const checkedItems = trip.items.filter(item => item.checked);
    const uncheckedItems = trip.items.filter(item => !item.checked);
    
    let itemsSummary = '';
    if (checkedItems.length > 0) {
        const checkedNames = checkedItems.slice(0, 3).map(item => item.name);
        if (checkedItems.length > 3) {
            checkedNames.push(`+${checkedItems.length - 3} more`);
        }
        itemsSummary = checkedNames.join(', ');
    }

    div.innerHTML = `
        <div class="trip-header">
            <div class="trip-date">
                <strong>${tripDate}</strong>
                <span class="trip-days-ago">${daysAgoText}</span>
            </div>
            <div class="trip-stats">
                ${trip.checkedItems}/${trip.totalItems} items
            </div>
        </div>
        <div class="trip-items">
            ${itemsSummary || 'No items checked off'}
        </div>
    `;

    return div;
}

// Handle copy from last trip
async function handleCopyFromLastTrip() {
    try {
        const response = await fetch('/copy-from-last-trip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();

        if (data.success) {
            await loadItems();
            const message = data.copiedCount > 0 
                ? `Copied ${data.copiedCount} items from last trip`
                : 'No new items to copy';
            showToast(message, 'success');
        } else {
            showToast(data.error || 'Failed to copy items', 'error');
        }
    } catch (error) {
        console.error('Error copying from last trip:', error);
        showToast('Failed to copy items', 'error');
    }
}

// No auto-refresh needed (not using iOS Shortcuts)
