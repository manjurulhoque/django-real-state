/**
 * Wishlist functionality for Real Estate listings
 * Handles adding/removing properties to/from user wishlist
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize wishlist buttons when page loads
    initializeWishlistButtons();
    
    // Use event delegation to handle wishlist button clicks
    // This prevents multiple event listeners from being attached
    document.addEventListener('click', function(e) {
        if (e.target.closest('.wishlist-btn')) {
            handleWishlistClick(e);
        }
    });
});

/**
 * Initialize all wishlist buttons on the page
 * Check current wishlist status for each property
 */
function initializeWishlistButtons() {
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach(button => {
        const listingId = button.getAttribute('data-listing-id');
        
        if (listingId) {
            checkWishlistStatus(button, listingId);
        }
    });
}

/**
 * Check if a property is already in the user's wishlist
 * @param {HTMLElement} button - The wishlist button element
 * @param {string} listingId - The property listing ID
 */
function checkWishlistStatus(button, listingId) {
    fetch(`/wishlist/check/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.in_wishlist) {
                button.classList.add('active');
                button.title = 'Remove from wishlist';
            } else {
                button.classList.remove('active');
                button.title = 'Add to wishlist';
            }
        })
        .catch(error => {
            console.log('Error checking wishlist status:', error);
        });
}

/**
 * Handle wishlist button clicks
 * @param {Event} e - The click event
 */
function handleWishlistClick(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const button = e.target.closest('.wishlist-btn');
    const listingId = button.getAttribute('data-listing-id');
    
    if (!listingId) {
        console.error('No listing ID found');
        return;
    }
    
    const isActive = button.classList.contains('active');
    const action = isActive ? 'remove' : 'add';
    
    // Disable button temporarily to prevent double clicks
    button.disabled = true;
    
    // Make the API call
    fetch(`/wishlist/${action}/${listingId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateButtonState(button, action);
            showNotification(
                action === 'add' 
                    ? 'Property added to your wishlist!' 
                    : 'Property removed from your wishlist!',
                action === 'add' ? 'success' : 'info'
            );
        } else {
            showNotification(data.message || 'Something went wrong. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Wishlist error:', error);
        showNotification('Something went wrong. Please try again.', 'error');
    })
    .finally(() => {
        // Re-enable button
        button.disabled = false;
    });
}

/**
 * Update button visual state after successful API call
 * @param {HTMLElement} button - The wishlist button
 * @param {string} action - The action performed ('add' or 'remove')
 */
function updateButtonState(button, action) {
    if (action === 'add') {
        button.classList.add('active');
        button.title = 'Remove from wishlist';
    } else {
        button.classList.remove('active');
        button.title = 'Add to wishlist';
    }
}

/**
 * Get CSRF token for Django AJAX requests
 * @returns {string} CSRF token
 */
function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (!csrfToken) {
        console.warn('CSRF token not found');
        return '';
    }
    return csrfToken;
}

/**
 * Show notification messages to user
 * @param {string} message - The message to display
 * @param {string} type - The type of notification ('success', 'error', 'info')
 */
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.notification-toast');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    const alertClass = type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info';
    
    notification.className = `alert alert-${alertClass} alert-dismissible fade show notification-toast`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add styles for positioning
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: none;
        border-radius: 8px;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 150);
        }
    }, 4000);
}

/**
 * Refresh wishlist buttons after dynamic content changes
 * Call this function if you load new listing cards via AJAX
 */
function refreshWishlistButtons() {
    initializeWishlistButtons();
}

// Export function for use in other scripts if needed
if (typeof window !== 'undefined') {
    window.refreshWishlistButtons = refreshWishlistButtons;
} 