// Array to hold the list of contacts
let contacts = [];

// Function to fetch contacts from the backend and populate the contacts array
function fetchContacts() {
    fetch('../php codes/get_contacts.php', {
        method: 'GET', // HTTP GET request to retrieve contacts
    })
    .then(response => response.json()) // Parse response as JSON
    .then(data => {
        if (data.status === 'success') {
            // If the request is successful, populate the contacts array
            contacts = data.contacts;

            // Render the contacts and update the stats
            renderContacts(currentCategory, searchBar.value);
            renderContactStats();
        } else {
            console.error('Failed to load contacts:', data.message); // Log an error if fetching fails
        }
    })
    .catch(error => {
        console.error('Error fetching contacts:', error); // Handle network or parsing errors
    });
}

// DOM element references for various UI components
const contactsGrid = document.getElementById('contactsGrid');
const filterButtons = document.querySelectorAll('.filter-btn');
const searchBar = document.getElementById('searchBar');
const deleteModal = document.getElementById('deleteModal');
const confirmDelete = document.getElementById('confirmDelete');
const cancelDelete = document.getElementById('cancelDelete');
const addContactBtn = document.getElementById('addContactBtn');
const addContactModal = document.getElementById('addContactModal');
const newContactForm = document.getElementById('newContactForm');
const cancelAdd = document.getElementById('cancelAdd');
const editContactModal = document.getElementById('editContactModal');
const editContactForm = document.getElementById('editContactForm');
const cancelEdit = document.getElementById('cancelEdit');
const importBtn = document.getElementById('importBtn');
const exportBtn = document.getElementById('exportBtn');
const importInput = document.getElementById('importInput');
const signOutBtn = document.getElementById('signOutBtn');
const addCategoryBtn = document.getElementById('sidebarAddCategoryBtn');
const modal = document.getElementById('customCategoryModal');

// Variables to manage state
let currentCategory = 'all';
let contactToDelete = null;
let isMultiSelectMode = false;
let selectedContacts = new Set();

// Initial rendering of stats and contacts
renderContactStats();
document.getElementById('searchOption').addEventListener('change', () => {
    renderContacts(currentCategory, searchBar.value); // Update contact list when search options changes
});
searchBar.addEventListener('input', e => {
    renderContacts(currentCategory, e.target.value);// Update contact list as the user types
});
// Function to display the contacts
function renderContacts(category, searchTerm) {
    contactsGrid.innerHTML = ''; // Clear the contacts grid

    const searchOption = document.getElementById('searchOption').value;
    // Filter contacts by category and search term
    let filteredContacts = contacts.filter(contact => {
        const matchesCategory = category === 'all' || contact.category.toLowerCase() === category.toLowerCase();
        let matchesSearch = false;

        if (searchTerm === '') {
            matchesSearch = true; // If no search term, match all contacts
        } else {
            switch (searchOption) {
                case 'name':
                    matchesSearch = contact.name.toLowerCase().includes(searchTerm.toLowerCase());
                    break;
                case 'email':
                    matchesSearch = contact.email.toLowerCase().includes(searchTerm.toLowerCase());
                    break;
                case 'phone':
                    matchesSearch = contact.phone.toLowerCase().includes(searchTerm.toLowerCase());
                    break;
                case 'all':
                default:
                    matchesSearch = contact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                                    contact.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                                    contact.phone.toLowerCase().includes(searchTerm.toLowerCase());
            }
        }
        return matchesCategory && matchesSearch;
    });

    // Sort the filtered contacts alphabetically by name
    filteredContacts.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));

    // Display a message if no contacts match the criteria
    if (filteredContacts.length === 0) {
        contactsGrid.innerHTML = `
        <div class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            <h3>No contacts found</h3>
            <p>Try adjusting your search or filters, or add a new contact!</p>
        </div>
        `;
        renderContactStats(); // Update stats
        return;
    }

    // Create and display contact cards for each filtered contact
    filteredContacts.forEach(contact => {
        const contactElement = document.createElement('div');
        contactElement.className = 'contact-card';
        contactElement.setAttribute('data-id', contact.id);
        if (selectedContacts.has(contact.id)) {
            contactElement.classList.add('selected');
        }
        contactElement.innerHTML = `
        <input type="checkbox" class="select-checkbox" ${selectedContacts.has(contact.id) ? 'checked' : ''}>
        <button class="delete-btn">Delete</button>
        <button class="edit-btn">Edit</button>
        <button class="email-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
            </svg>
            Email
        </button>
        <div class="contact-avatar">${contact.initial}</div>
        <div class="contact-info">
            <div class="contact-name">${contact.name}</div>
            <div class="contact-category">${contact.category}</div>
            <div class="contact-details">
                <div>${contact.email}</div>
                <div>${contact.phone}</div>
            </div>
        </div>
        `;

        // Add event listeners to the checkbox for multi-select mode
        const checkbox = contactElement.querySelector('.select-checkbox');
        checkbox.addEventListener('change', e => {
            e.stopPropagation();
            if (e.target.checked) {
                selectedContacts.add(contact.id);
                contactElement.classList.add('selected');
                if (!isMultiSelectMode) {
                    toggleMultiSelectMode(true);
                }
            } else {
                selectedContacts.delete(contact.id);
                contactElement.classList.remove('selected');
                if (selectedContacts.size === 0) {
                    toggleMultiSelectMode(false);
                }
            }
            updateSelectedCount();
        });

        // Add event listeners for delete button
        const deleteBtn = contactElement.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', e => {
            e.stopPropagation();
            if (e.shiftKey || isMultiSelectMode) {
                if (!isMultiSelectMode) {
                    toggleMultiSelectMode(true);
                }
                selectedContacts.add(contact.id);
                contactElement.classList.add('selected');
                checkbox.checked = true;
                updateSelectedCount();
            } else {
                contactToDelete = contact.id;
                deleteModal.style.display = 'flex';
            }
        });

        // Append the contact card to the grid
        contactsGrid.appendChild(contactElement);
    });
    // Attach a click event listener to all elements with the 'edit-btn' class
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            // Get the contact ID from the closest parent element with the 'contact-card' class
            const contactId = e.target.closest('.contact-card').getAttribute('data-id');
    
            // Fetch the contact details from the backend using the contact ID
            fetch(`../php codes/get_contacts_for_edit.php?id=${contactId}`)
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                if (data.success) {
                    const contact = data.contact; // Extract the contact data from the response

                    // Populate the edit modal fields with the contact's details
                    document.getElementById('editContactId').value = contact.id;
                    document.getElementById('editFullName').value = `${contact.first_name} ${contact.last_name}`;
                    document.getElementById('editEmail').value = contact.email;
                    document.getElementById('editPhone').value = contact.phone_number;
                    document.getElementById('editCategory').value = contact.category;

                    // Display the edit modal to the user
                    document.getElementById('editContactModal').style.display = 'flex';
                } else {
                    // Show an alert if there is an error in fetching contact details
                    alert('Error fetching contact details');
                }
            })
            .catch(error => {
                // Handle network or unexpected errors
                alert('An error occurred while fetching the contact details');
            });
        });
    });
    renderContactStats();
}
document.getElementById('SaveChanges').addEventListener('click', function () {
    location.reload();
});
// Initialize variables to store the user ID and fetch status
let userId = null; // Holds the user ID of the logged-in user
let isUserIdFetched = false; // Tracks whether the user ID has been successfully fetched

// Perform an AJAX request to fetch the logged-in user's ID
fetch('../php codes/get_user_id.php')
    .then(response => {
        // Check if the network response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok'); // Throw an error if the response is not ok
        }
        return response.json(); // Parse the response as JSON
    })
    .then(data => {
        // Check if the user ID is present in the response
        if (data.user_id) {
            userId = data.user_id; // Store the user ID
            isUserIdFetched = true; // Mark that the user ID has been successfully fetched
            console.log('User ID:', userId); // Log the user ID to the console
        } else {
            console.error('Error: User not logged in'); // Log an error if the user ID is not found
        }
    })
    .catch(error => {
        // Handle any errors that occur during the fetch request
        console.error('Error fetching user ID:', error); // Log the error to the console
    });

// Event listener for the category dropdown
document.getElementById('editCategory').addEventListener('change', function (e) {
    const selectedValue = e.target.value;

    if (selectedValue === 'custom') {
        // Show the custom category modal
        document.getElementById('customCategoryModal').style.display = 'flex';
        document.getElementById('customCategoryModalInput').focus();
    }
});

// Event listener for the "Add Category" button in the modal
document.getElementById('submitCustomCategory').addEventListener('click', () => {
    // Get the value of the custom category input and trim any whitespace
    const customCategory = document.getElementById('customCategoryModalInput').value.trim();
    const errorMessageDiv = document.getElementById('categoryErrorMessage'); // Reference to error message div
    let categorySelect = document.getElementById('category'); // Reference to the category dropdown

    // Only proceed if customCategory is not empty
    if (customCategory) {
        // Check if the category already exists in custom categories or default categories
        const categoryExists = Array.from(customCategories).some(cat => 
            cat.toLowerCase() === customCategory.toLowerCase());
        const defaultCategories = ['work', 'family', 'friends'];
        const isDuplicate = defaultCategories.some(cat => 
            cat.toLowerCase() === customCategory.toLowerCase());

        // If the category exists, display an error message
        if (categoryExists || isDuplicate) {
            errorMessageDiv.textContent = 'This category already exists. Please choose a different name.';
            errorMessageDiv.style.opacity = '1'; // Make the error message visible
            return;
        }

        // Prepare the data to be sent to the server
        const formData = new FormData();
        formData.append('category_name', customCategory);

        // Send a POST request to add the custom category to the backend
        fetch('../php codes/add_category.php', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
            if (data.success) {
                // If the category is successfully added to the backend
                customCategories.add(customCategory); // Add the new category to the customCategories set
                updateCategoryOptions(); // Update the category dropdown options

                // Create a new filter button for the added category
                const sidebarFilters = document.querySelector('.sidebar-filters');
                const newFilterBtn = document.createElement('button');
                newFilterBtn.className = 'filter-btn';
                newFilterBtn.dataset.category = customCategory;
                newFilterBtn.innerHTML = `
                    <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
                        <rect x="3" y="3" width="18" height="14" rx="2" ry="2" />
                        <line x1="9" y1="8" x2="15" y2="8" />
                        <line x1="9" y1="12" x2="13" y2="12" />
                        <circle cx="6" cy="8" r="1" />
                        <line x1="12" y1="20" x2="12" y2="16" />
                        <line x1="10" y1="18" x2="14" y2="18" />
                    </svg>
                    <span class="text">${customCategory}</span>
                `;

                // Ensure the newly added category is selected in the dropdown
                if (window.lastCategorySelect) {
                    window.lastCategorySelect.value = customCategories[customCategories.length - 1];
                    window.lastCategorySelect = null;
                } else {
                    document.getElementById('category').value = customCategories[customCategories.length - 1];
                }

                // Add click functionality to the new filter button
                newFilterBtn.addEventListener('click', () => {
                    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                    if (currentCategory === customCategory) {
                        currentCategory = 'all';
                        document.querySelector('[data-category="all"]').classList.add('active');
                    } else {
                        currentCategory = customCategory;
                        newFilterBtn.classList.add('active');
                    }
                    renderContacts(currentCategory, searchBar.value); // Re-render the contact list
                });

                // Add the new button to the sidebar
                sidebarFilters.insertBefore(newFilterBtn, addCategoryBtn);

                // Close the modal and reset the input
                document.getElementById('customCategoryModal').style.display = 'none';
                document.getElementById('customCategoryModalInput').value = '';
                errorMessageDiv.style.opacity = '0';
            } else {
                // Handle errors returned by the backend
                errorMessageDiv.textContent = data.error || 'An error occurred while adding the category.';
                errorMessageDiv.style.opacity = '1';
            }
        })
        .catch(error => {
            // Handle any network or unexpected errors during the fetch
            errorMessageDiv.textContent = 'An error occurred while adding the category.';
            errorMessageDiv.style.opacity = '1';
            console.error('Error:', error);
        });
    }
});

// Add an event listener to handle the edit contact form submission
document.getElementById('editContactForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission behavior

    // Ensure the user ID has been fetched before proceeding
    if (!isUserIdFetched) {
        alert('User ID not fetched yet. Please wait...');
        return;
    }

    // Get the values from the edit contact form fields
    const fullName = document.getElementById('editFullName').value;
    const email = document.getElementById('editEmail').value;
    const phone = document.getElementById('editPhone').value;
    const category = document.getElementById('editCategory').value;
    const contactId = document.getElementById('editContactId').value;

    // Validate that all fields are filled in
    if (!fullName || !email || !phone || !category || !contactId) {
        alert('Please fill in all fields');
        return;
    }

    // Split the full name into first and last name parts
    const nameParts = fullName.split(' ');
    const firstName = nameParts[0]; // The first part of the name
    const lastName = nameParts.slice(1).join(' '); // The remaining parts as the last name

    // Create a FormData object to send the updated contact information to the server
    const formData = new FormData();
    formData.append('user_id', userId); // Add the user ID
    formData.append('contact_id', contactId); // Add the contact ID
    formData.append('first_name', firstName); // Add the first name
    formData.append('last_name', lastName); // Add the last name
    formData.append('email', email); // Add the email address
    formData.append('phone_number', phone); // Add the phone number
    formData.append('category', category); // Add the category

    // Send a POST request to update the contact on the server
    fetch('../php codes/edit_contact.php', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok'); // Handle network errors
        }
        return response.json(); // Parse the response as JSON
    })
    .then(data => {
        if (data.success) {
            // Create an updated contact object with the new data
            const updatedContact = {
                id: contactId,
                name: fullName,
                email: email,
                phone: phone,
                category: category
            };

            // Update the contact in the contacts array
            const contactIndex = contacts.findIndex(contact => contact.id === contactId);
            if (contactIndex !== -1) {
                contacts[contactIndex] = updatedContact; // Replace the contact in the array
            }

            // Update the contact card in the DOM
            const contactElement = document.querySelector(`[data-id="${contactId}"]`);
            if (contactElement) {
                contactElement.querySelector('.contact-name').textContent = fullName; // Update name
                contactElement.querySelector('.contact-category').textContent = category; // Update category
                contactElement.querySelector('.contact-details div:nth-child(1)').textContent = email; // Update email
                contactElement.querySelector('.contact-details div:nth-child(2)').textContent = phone; // Update phone
            }

            renderContactStats(); // Re-render contact stats

            // Close the edit modal
            editContactModal.style.display = 'none';
        } else {
            // Handle errors returned by the server
            alert('Error updating contact: ' + data.error);
        }

    })
    .catch(error => {
        // Handle unexpected errors
        console.error('An error occurred:', error);
    });
});

    

cancelEdit.addEventListener('click', () => {
    editContactModal.style.display = 'none';
});

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        filterButtons.forEach(btn => btn.classList.remove('active'));
        const allCustomButtons = document.querySelectorAll('.filter-btn');
        allCustomButtons.forEach(btn => btn.classList.remove('active'));
        if (currentCategory === button.dataset.category) {
            currentCategory = 'all';
            document.querySelector('[data-category="all"]').classList.add('active');
        } else {
            currentCategory = button.dataset.category;
            button.classList.add('active');
        }
        renderContacts(currentCategory, searchBar.value);
    });
});
let customCategories = new Set();
function renderContactStats() {
    // Remove existing stats if present
    const existingStats = document.querySelector('.contact-stats');
    if (existingStats) {
        existingStats.remove();
    }
    // Normalize categories and calculate unique counts
    const categoryCounts = contacts.reduce((acc, contact) => {
        // Normalize category to lowercase and handle undefined/null/empty values
        const category = (contact.category && contact.category.trim()) || "uncategorized";
        acc[category.toLowerCase()] = (acc[category.toLowerCase()] || 0) + 1;
        return acc;
    }, {});

    // Build the stats HTML
    const statsHtml = `
        <div class="contact-stats">
            <div class="stat-item">
                <div class="stat-value">${contacts.length}</div>
                <div class="stat-label">Total Contacts</div>
            </div>
            ${Object.entries(categoryCounts).map(([category, count]) => `
                <div class="stat-item">
                    <div class="stat-value">${count}</div>
                    <div class="stat-label">${category.charAt(0).toUpperCase() + category.slice(1)}</div>
                </div>
            `).join('')}
        </div>
    `;
    // Insert stats after the search bar
    const searchBarElement = document.querySelector('.search-container');
    searchBarElement.insertAdjacentHTML('afterend', statsHtml);
}


function toggleMultiSelectMode(enable) {
    isMultiSelectMode = enable;
    document.querySelector('.multi-select-controls').classList.toggle('active', enable);
    document.querySelector('.move-selected-btn').disabled = selectedContacts.size === 0;
    
    document.querySelectorAll('.contact-card').forEach(card => {
        card.classList.toggle('multi-select-mode', enable);
    });
    
    if (!enable) {
        selectedContacts.clear();
        updateSelectedCount();
    }
}
function updateSelectedCount() {
    document.getElementById('selectedCount').textContent = selectedContacts.size;
}
// ---------------------------------------------------------- Manipulate Category ----------------------------------------------------------
document.getElementById('customCategoryInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        const customCategory = e.target.value.trim();

        if (!customCategory) {
            alert('Please enter a valid category name.');
            return;
        }

        // Add the custom category to the dropdown
        const categoryDropdown = document.getElementById('editCategory');
        const customOption = document.createElement('option');
        customOption.value = customCategory;
        customOption.textContent = customCategory;
        categoryDropdown.appendChild(customOption);

        // Select the newly added custom category
        categoryDropdown.value = customCategory;

        // Clear and hide the custom input field
        e.target.value = '';
        document.getElementById('customCategoryModal').style.display = 'none';
    }
})

// Handle form submission
newContactForm.addEventListener('submit', e => {
    e.preventDefault();  // Prevent form submission
    
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    let category = document.getElementById('category').value;
    
    const newContact = {
        name: fullName,
        category: category,
        initial: fullName.split(' ').map(word => word[0]).join(''),
        email: email,
        phone: phone
    };
    
    // **Dynamic Category Handling**: Add custom category if not predefined or already in customCategories
    if (!['work', 'family', 'friends'].includes(category.toLowerCase()) && !customCategories.has(category.toLowerCase())) {
        category = category.charAt(0).toUpperCase() + category.slice(1).toLowerCase();  // Format as proper noun
        customCategories.add(category.toLowerCase());  // Add the custom category to the set
        updateCategoryOptions();  // Update the dropdown options with updated categories
    }

    // Send the form data to the backend via fetch (AJAX)
    const formData = new FormData();
    formData.append('fullName', fullName);
    formData.append('email', email);
    formData.append('phone', phone);
    formData.append('category', category);

    // Send the contact data to the backend
    fetch('../php codes/add_contact.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Parse JSON response from the backend
    .then(data => {
        if (data.status === 'success') {
            // Backend returns the actual contact_id
            const contactId = data.contact_id; // Assuming the backend returns the contact ID
            const newContactWithId = { ...newContact, id: contactId }; // Assign the correct ID
            
            // Add the new contact to the frontend
            contacts.push(newContactWithId);
            
            // Re-render the contact list based on the current category and search bar value
            renderContacts(currentCategory, searchBar.value);
            renderContactStats(); // Re-render contact stats like the total count
            
            // Re-select the new custom category in the dropdown
            const categoryDropdown = document.getElementById('category');
            categoryDropdown.value = category;  // Set the new custom category as selected
            
            // Hide the modal and reset the form
            addContactModal.style.display = 'none';
            newContactForm.reset();
        } else {
            alert('Error adding contact: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error adding contact:', error);
        alert('Error adding contact');
    });
});



// Fetch categories when the page loads
fetchCategories();


function renderCategoryButtons() {
    // Default categories with their respective SVG icons
    const defaultCategories = [
        { name: "Work", icon: `<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>` },
        { name: "Friends", icon: `<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>` },
        { name: "Family", icon: `<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <line x1="19" y1="8" x2="19" y2="14"/>
            <line x1="16" y1="11" x2="22" y2="11"/>
        </svg>` }
    ];

    // Fetch categories from the backend
    fetch('../php codes/fetch_categories.php')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const categories = data.categories || [];
                const sidebarFilters = document.querySelector('.sidebar-filters');
                const addCategoryBtn = document.getElementById('sidebarAddCategoryBtn');

                // Clear existing buttons (except "Add Category" button)
                sidebarFilters.querySelectorAll('.filter-btn').forEach(btn => btn.remove());

                // Add "All Contacts" button
                const allBtn = document.createElement('button');
                allBtn.className = 'filter-btn active';
                allBtn.dataset.category = 'all';
                allBtn.innerHTML = `
                    <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 2v20M2 12h20"/>
                    </svg>
                    <span class="text">All Contacts</span>
                `;
                allBtn.addEventListener('click', () => {
                    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                    allBtn.classList.add('active');
                    renderContacts('all', searchBar.value);
                });
                sidebarFilters.insertBefore(allBtn, addCategoryBtn);

                // Render default categories with their custom SVGs
                defaultCategories.forEach(defaultCategory => {
                    const categoryBtn = document.createElement('button');
                    categoryBtn.className = 'filter-btn';
                    categoryBtn.dataset.category = defaultCategory.name.toLowerCase();
                    categoryBtn.innerHTML = `
                        ${defaultCategory.icon}
                        <span class="text">${defaultCategory.name}</span>
                    `;

                    categoryBtn.addEventListener('click', () => {
                        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                        categoryBtn.classList.add('active');
                        renderContacts(defaultCategory.name.toLowerCase(), searchBar.value);
                    });

                    // Insert the button before "Add Category" button
                    sidebarFilters.insertBefore(categoryBtn, addCategoryBtn);
                });

                // Render fetched categories (excluding default categories)
                categories.forEach(category => {
                    if (!defaultCategories.map(cat => cat.name.toLowerCase()).includes(category.toLowerCase())) {
                        const categoryBtn = document.createElement('button');
                        categoryBtn.className = 'filter-btn';
                        categoryBtn.dataset.category = category;
                        categoryBtn.innerHTML = `
                            <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="3" width="18" height="14" rx="2" ry="2" />
                                <line x1="9" y1="8" x2="15" y2="8" />
                                <line x1="9" y1="12" x2="13" y2="12" />
                                <circle cx="6" cy="8" r="1" />
                                <line x1="12" y1="20" x2="12" y2="16" />
                                <line x1="10" y1="18" x2="14" y2="18" />
                            </svg>
                            <span class="text">${category}</span>
                        `;

                        categoryBtn.addEventListener('click', () => {
                            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                            categoryBtn.classList.add('active');
                            renderContacts(category, searchBar.value);
                        });

                        // Insert the button before "Add Category" button
                        sidebarFilters.insertBefore(categoryBtn, addCategoryBtn);
                    }
                });
            } else {
                console.error('Failed to fetch categories: ', data.error);
            }
        })
        .catch(error => {
            console.error('Error fetching categories:', error);
        });
}

// Call renderCategoryButtons on page load
document.addEventListener('DOMContentLoaded', renderCategoryButtons);


addCategoryBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
});

document.getElementById('category').addEventListener('change', function() {
    if (this.value === 'custom') {
        document.getElementById('customCategoryModal').style.display = 'flex';
    }
});






document.getElementById('sidebarAddCategoryBtn').addEventListener('click', () => {
    document.getElementById('customCategoryModal').style.display = 'flex';
    document.getElementById('customCategoryModalInput').focus();
});
document.getElementById('cancelCustomCategory').addEventListener('click', () => {
    document.getElementById('customCategoryModal').style.display = 'none';
    document.getElementById('customCategoryModalInput').value = '';
    document.getElementById('categoryErrorMessage').style.opacity = '0';
});

function updateCategoryOptions() {
    // Fetch the current categories (default and custom) from the backend
    fetch('../php codes/get_categories.php')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const categories = data.categories || []; // Default and custom categories
                const categorySelects = [document.getElementById('category'), document.getElementById('editCategory')];

                categorySelects.forEach(select => {
                    const currentValue = select.value;

                    // Populate categories dynamically (categories are directly passed as an array of names in this case)
                    select.innerHTML = `
                        ${categories.map(cat => `<option value="${cat}">${cat}</option>`).join('')}
                        <option value="custom">Add Custom Category</option>
                    `;

                    // Restore the previously selected value (if it still exists in the options)
                    if (select.querySelector(`option[value="${currentValue}"]`)) {
                        select.value = currentValue;
                    }
                });

                const moveSelect = document.getElementById('moveToCategory');
                if (moveSelect) {
                    const currentValue = moveSelect.value;
                    moveSelect.innerHTML = `
                        ${categories.map(cat => `<option value="${cat}">${cat}</option>`).join('')}
                        <option value="custom">Add Custom Category</option>
                    `;

                    // Restore the previously selected value
                    if (moveSelect.querySelector(`option[value="${currentValue}"]`)) {
                        moveSelect.value = currentValue;
                    }
                }

                renderContactStats();
            } else {
                console.error('Failed to fetch categories:', data.error);
            }
        })
    .catch(error => {
        console.error('Error fetching categories:', error);
    });

}

// ---------------------------------------------------------- Move Contacts ----------------------------------------------------------
document.querySelector('.move-selected-btn').addEventListener('click', () => {
    if (selectedContacts.size === 0) {
        const alert = document.createElement('div');
        alert.className = 'import-alert';
        alert.style.backgroundColor = '#ff4444';
        alert.textContent = 'Please select contacts to move';
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
        return;
    }
    
    document.getElementById('categorySelectModal').style.display = 'flex';
});
    
document.getElementById('confirmMove').addEventListener('click', () => {
    const newCategory = document.getElementById('moveToCategory').value;
    if (newCategory && newCategory !== 'custom') {
        const movedCount = selectedContacts.size;

        // Send selected contact IDs and the new category to the server
        const selectedContactIds = Array.from(selectedContacts);
        const formData = new FormData();
        formData.append('category_name', newCategory);
        formData.append('contact_ids', JSON.stringify(selectedContactIds));  // Send contact IDs as a JSON string

        fetch('../php codes/move_contacts.php', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the local data with the new category
                contacts = contacts.map(contact => {
                    if (selectedContactIds.includes(contact.id)) {
                        return {
                        ...contact,
                        category: newCategory
                        };
                    }
                    return contact;
                });

            const alert = document.createElement('div');
            alert.className = 'import-alert';
            alert.style.backgroundColor = '#1877f2';
            alert.textContent = `Successfully moved ${movedCount} contact${movedCount > 1 ? 's' : ''} to ${newCategory}`;
            renderContactStats();
            document.body.appendChild(alert);
            setTimeout(() => alert.remove(), 3000);

            toggleMultiSelectMode(false);
            document.getElementById('categorySelectModal').style.display = 'none';
            renderContacts(currentCategory, searchBar.value);
            renderContactStats();
        } else {
            const alert = document.createElement('div');
            alert.className = 'import-alert';
            alert.style.backgroundColor = '#ff4444';
            alert.textContent = data.error || 'An error occurred while moving the contacts.';
            document.body.appendChild(alert);
            setTimeout(() => alert.remove(), 3000);
        }
        })
        .catch(error => {
            const alert = document.createElement('div');
            alert.className = 'import-alert';
            alert.style.backgroundColor = '#ff4444';
            alert.textContent = 'An error occurred while moving the contacts.';
            document.body.appendChild(alert);
            setTimeout(() => alert.remove(), 3000);
            console.error('Error:', error);
        });
    }
});

document.getElementById('cancelMove').addEventListener('click', () => {
    document.getElementById('categorySelectModal').style.display = 'none';
});
    
document.getElementById('moveToCategory').addEventListener('change', function() {
    if (this.value === 'custom') {
        document.getElementById('categorySelectModal').style.display = 'none';
        document.getElementById('customCategoryModal').style.display = 'flex';
        document.getElementById('customCategoryModalInput').focus();
        window.lastCategorySelect = this;
}
});
    
document.querySelector('.cancel-select-btn').addEventListener('click', () => {
    toggleMultiSelectMode(false);
    selectedContacts.clear();
    document.querySelectorAll('.contact-card').forEach(card => {
        card.classList.remove('selected');
        const checkbox = card.querySelector('.select-checkbox');
        if (checkbox) {
            checkbox.checked = false;
        }
    });
    updateSelectedCount();
});

// ---------------------------------------------------------- Add Contact ----------------------------------------------------------
addContactBtn.addEventListener('click', () => {
    addContactModal.style.display = 'flex';
});
cancelAdd.addEventListener('click', () => {
    addContactModal.style.display = 'none';
    newContactForm.reset();
});

// ---------------------------------------------------------- Delete Contacts ----------------------------------------------------------
// Function to delete a contact by ID
function deleteContact(contactId) {
    // Check if a contact ID is provided
    if (!contactId) {
        console.error('No contact ID provided.');  // Log error if no ID
        return;
    }

    // Send the contact ID to the backend to delete the contact
    fetch('../php codes/delete_contact.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Send as JSON
        },
        body: JSON.stringify({ contact_id: contactId })  // Pass contact ID in the request body
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {
        if (data.status === 'success') {
            console.log(`Contact with ID ${contactId} deleted successfully.`);  // Success message
        } else {
            console.error('Error deleting contact:', data.message);  // Log error if failed
        }
    })
    .catch(error => {
        console.error('Error deleting contact:', error);  // Log any network or other errors
    });
}

// Event listener for confirming the delete action
confirmDelete.addEventListener('click', () => {
    // Check if multi-select mode is enabled and there are selected contacts
    if (isMultiSelectMode && selectedContacts.size > 0) {
        // Apply transition effects to selected contact cards
        document.querySelectorAll('.contact-card.selected').forEach(card => {
            const rect = card.getBoundingClientRect();  // Get card's position and size
            createPaperParticle(rect);  // Create visual particle effect
            card.style.transition = 'all 0.3s ease-out';  // Transition effect for disappearing
            card.style.opacity = '0';  // Fade out
            card.style.transform = 'scale(0.8)';  // Shrink the card
        });

        // After animation delay, delete the contacts in frontend and backend
        setTimeout(() => {
            // Remove selected contacts from the local array
            contacts = contacts.filter(contact => !selectedContacts.has(contact.id));
            // Delete each contact from the backend
            selectedContacts.forEach(contactId => {
                deleteContact(contactId);
            });
            // Exit multi-select mode
            toggleMultiSelectMode(false);
            // Re-render the contact list and stats
            renderContacts(currentCategory, searchBar.value);
            renderContactStats();
            deleteModal.style.display = 'none';  // Close the delete modal
            selectedContacts.clear();  // Clear selected contacts
        }, 300);  // Delay to allow transition effects to finish
    } else if (contactToDelete) {
        // If only one contact is selected for deletion, apply transition effects
        const contactElement = document.querySelector(`.contact-card[data-id="${contactToDelete}"]`);
        if (contactElement) {
            const rect = contactElement.getBoundingClientRect();  // Get contact card position
            createPaperParticle(rect);  // Create visual particle effect
            contactElement.style.transition = 'all 0.3s ease-out';  // Apply transition
            contactElement.style.opacity = '0';  // Fade out
            contactElement.style.transform = 'scale(0.8)';  // Shrink the card
        }

        // After animation delay, delete the contact in frontend and backend
        setTimeout(() => {
            const index = contacts.findIndex(contact => contact.id === contactToDelete);  // Find contact in local array
            if (index !== -1) {
                contacts.splice(index, 1);  // Remove from local array
            }

            deleteContact(contactToDelete);  // Delete the contact from the backend
            renderContacts(currentCategory, searchBar.value);  // Re-render the contact list
            renderContactStats();  // Update stats
            deleteModal.style.display = 'none';  // Close the delete modal
            contactToDelete = null;  // Clear the selected contact
        }, 300);  // Delay for transition effects
    }
});

// Event listener for canceling the delete action
cancelDelete.addEventListener('click', () => {
    deleteModal.style.display = 'none';  // Close the delete modal
    contactToDelete = null;  // Clear the selected contact
});

// Event listener to open the delete modal for selected contacts
document.querySelector('.delete-selected-btn').addEventListener('click', () => {
    // If no contacts are selected, do nothing
    if (selectedContacts.size === 0) return;
    deleteModal.style.display = 'flex';  // Open the delete modal
});

// ---------------------------------------------------------- Delete Effect ----------------------------------------------------------
function createPaperParticle(rect) {
    for (let i = 0; i < 100; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        const edge = Math.floor(Math.random() * 4);
        let startX, startY;
        switch (edge) {
            case 0:
            startX = rect.left + Math.random() * rect.width;
            startY = rect.top;
            break;
            case 1:
            startX = rect.right;
            startY = rect.top + Math.random() * rect.height;
            break;
            case 2:
            startX = rect.left + Math.random() * rect.width;
            startY = rect.bottom;
            break;
            case 3:
            startX = rect.left;
            startY = rect.top + Math.random() * rect.height;
            break;
        }
        const angle = Math.random() * Math.PI * 2;
        const force = 100 + Math.random() * 300;
        const tx = Math.cos(angle) * force;
        const ty = Math.sin(angle) * force + 200;
        const rotation = Math.random() * 1080 - 540;
        particle.style.left = `${startX}px`;
        particle.style.top = `${startY}px`;
        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);
        particle.style.setProperty('--rot', `${rotation}deg`);
        const hue = 35 + Math.random() * 15;
        const sat = 20 + Math.random() * 40;
        const light = 85 + Math.random() * 10;
        particle.style.background = `hsl(${hue}, ${sat}%, ${light}%)`;
        const size = 6 + Math.random() * 12;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        const duration = 0.6 + Math.random() * 0.8;
        particle.style.animation = `particleAnimation ${duration}s cubic-bezier(.36,.07,.19,.97) forwards`;
        document.body.appendChild(particle);
        setTimeout(() => {
            particle.remove();
        }, duration * 1000);
    }
    const tearLine = document.createElement('div');
    tearLine.className = 'cutting-line';
    tearLine.style.position = 'absolute';
    tearLine.style.left = `${rect.left}px`;
    tearLine.style.top = `${rect.top + rect.height / 2}px`;
    tearLine.style.width = `${rect.width}px`;
    tearLine.style.animation = 'cutAnimation 0.3s ease-out forwards';
    document.body.appendChild(tearLine);
    setTimeout(() => tearLine.remove(), 300);
}

// ---------------------------------------------------------- Import Contact ----------------------------------------------------------
// Trigger file input when the import button is clicked
importBtn.addEventListener('click', () => {
    importInput.click();  // Simulate file input click to open the file dialog
});

// Event listener for when the file is selected
importInput.addEventListener('change', e => {
    const file = e.target.files[0];  // Get the selected file
    if (!file) return;  // Exit if no file is selected

    const reader = new FileReader();  // Create a FileReader instance

    // Function to show an alert message on the page
    const showImportAlert = message => {
        const alert = document.createElement('div');
        alert.className = 'import-alert';  // Add a class for styling
        alert.textContent = message;  // Set the alert message
        document.body.appendChild(alert);  // Append the alert to the body
        setTimeout(() => {
            alert.remove();  // Remove the alert after 3 seconds
        }, 3000);
    };

    // Read the content of the file once it's loaded
    reader.onload = event => {
        try {
            // Determine the maximum existing contact ID for new contacts
            const maxId = Math.max(...contacts.map(c => c.id), 0);
            const newContacts = [];  // Array to store the new contacts
            let existingCategories = new Set();  // Set to track unique categories

            // Parse the file based on its type (JSON or CSV)
            if (file.name.endsWith('.json')) {
                const importedContacts = JSON.parse(event.target.result);  // Parse JSON content
                if (Array.isArray(importedContacts)) {
                    // Loop through each contact and assign an ID
                    importedContacts.forEach((contact, index) => {
                        newContacts.push({
                            ...contact,
                            id: maxId + index + 1  // Assign unique ID
                        });
                        // Add category to the existing categories set
                        existingCategories.add(contact.category.charAt(0).toUpperCase() + contact.category.slice(1).toLowerCase());
                    });
                }
            } else if (file.name.endsWith('.csv')) {
                const csvContent = event.target.result;  // Get CSV content
                const lines = csvContent.split('\n');  // Split into lines
                const headers = lines[0].split(',');  // Split headers (not used further)

                // Loop through the CSV lines to create contacts
                for (let i = 1; i < lines.length; i++) {
                    if (!lines[i].trim()) continue;  // Skip empty lines
                    const values = lines[i].split(',');  // Split the CSV line into values

                    // Create a contact object
                    const contact = {
                        id: maxId + i,  // Assign unique ID
                        name: values[1],
                        email: values[4],
                        phone: values[5],
                        category: values[2] || 'work',  // Default to 'work' if no category provided
                        initial: values[3].split(' ').map(word => word[0]).join('')  // Create initial from the name
                    };
                    newContacts.push(contact);  // Add the contact to the newContacts array
                    existingCategories.add(contact.category);  // Add category to the set
                }
            } else {
                alert('Please upload a .json or .csv file');  // Alert if the file is not JSON or CSV
                return;
            }

            // Update the category dropdown dynamically if new categories are found
            const categoryDropdown = document.getElementById('editCategory');
            existingCategories.forEach(category => {
                // Add new category options to the dropdown if not already present
                if (!Array.from(categoryDropdown.options).some(option => option.value === category)) {
                    const newOption = document.createElement('option');
                    newOption.value = category;
                    newOption.textContent = category.charAt(0).toUpperCase() + category.slice(1);
                    categoryDropdown.appendChild(newOption);
                }
            });

            // Display categories and filter buttons in the sidebar
            displayCategoryFilters(Array.from(existingCategories));

            // Send the new contacts to the backend for storage
            fetch('../php codes/import_contacts.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ contacts: newContacts })  // Send contacts as JSON
            })
            .then(response => response.json())  // Handle the response from the backend
            .then(data => {
                if (data.status === 'success') {
                    // If import is successful, add the new contacts to the local array and update the UI
                    contacts.push(...newContacts);
                    renderContacts(currentCategory, searchBar.value);  // Re-render the contacts
                    renderContactStats();  // Update the stats
                    showImportAlert(`Successfully imported ${newContacts.length} contacts!`);  // Show success alert
                } else {
                    showImportAlert(`Error importing contacts: ${data.message}`);  // Show error alert
                }
                location.reload();
            })
            .catch(error => {
                alert('Error importing contacts. Please try again.');  // Show a general error if the fetch fails
                console.error(error);  // Log the error to the console
            });

        } catch (error) {
            alert('Error importing contacts. Please check the file format.');  // Show error for invalid file format
            console.error(error);  // Log the error to the console
        }
    };

    // Read the file as text depending on its extension
    if (file.name.endsWith('.json')) {
        reader.readAsText(file);  // Read JSON file as text
    } else if (file.name.endsWith('.csv')) {
        reader.readAsText(file);  // Read CSV file as text
    } else {
        alert('Please upload a .json or .csv file');  // Alert if the file is not valid
    }
});

// ---------------------------------------------------------- Export Contact ----------------------------------------------------------
exportBtn.addEventListener('click', () => {
    const exportData = JSON.stringify(contacts, null, 2);
    const blob = new Blob([exportData], {
        type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contacts.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// ---------------------------------------------------------- Sign Out ----------------------------------------------------------
signOutBtn.addEventListener('click', () => {
    document.getElementById('signOutModal').style.display = 'flex';
});
document.getElementById('confirmSignOut').addEventListener('click', () => {
    window.location.href = "../php codes/logout.php";
});
document.getElementById('cancelSignOut').addEventListener('click', () => {
    document.getElementById('signOutModal').style.display = 'none';
});

// Fetch categories from the backend and populate the dropdown
async function fetchCategories() {
    try {
        // Send a request to the PHP script to fetch categories
        const response = await fetch('../php codes/fetch_categories.php'); // Your PHP script

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Failed to fetch categories');  // If not successful, throw an error
        }

        // Parse the response as JSON
        const data = await response.json();

        // Check if the server response indicates success
        if (data.success) {
            const categories = data.categories;  // Extract the categories array from the response

            // Use the updateCategoryOptions function to populate the dropdown with the fetched categories
            updateCategoryOptions(categories);
        } else {
            throw new Error('Failed to load categories: ' + data.message);  // If unsuccessful, throw an error with the message
        }
    } catch (error) {
        // Catch any errors (network issues, parsing errors, etc.)
        console.error('Error fetching categories:', error);  // Log the error to the console
    }
}


// Display categories and the "All Contacts" button
function displayCategoryFilters(categories) {
    const sidebarFilters = document.querySelector('.sidebar-filters'); // Select the container for buttons

    // Clear existing dynamically added buttons (if any)
    const existingButtons = sidebarFilters.querySelectorAll('.filter-btn');
    existingButtons.forEach(button => button.remove());

    // Add "All Contacts" button at the top
    const allContactsButton = document.createElement('button');
    allContactsButton.className = 'filter-btn';
    allContactsButton.dataset.category = 'all'; // Set data attribute for filtering
    allContactsButton.innerHTML = `
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
            <path d="M4 9h16M4 15h16M4 5h16M4 19h16M10 3v2m4-2v2M4 19a2 2 0 0 0 2-2h12a2 2 0 0 0 2 2H4z"></path>
        </svg>
        <span class="text">All Contacts</span>
    `;
    sidebarFilters.insertBefore(allContactsButton, document.getElementById('sidebarAddCategoryBtn'));

    // Add event listener for "All Contacts"
    allContactsButton.addEventListener('click', () => {
        filterContactsByCategory('all');
    });

    // Add a filter button for each category
    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.dataset.category = category; // Set data attribute for filtering

        // Create the SVG icon with the category name
        const svgIcon = `
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
                <rect x="3" y="3" width="18" height="14" rx="2" ry="2" />
                <line x1="9" y1="8" x2="15" y2="8" />
                <line x1="9" y1="12" x2="13" y2="12" />
                <circle cx="6" cy="8" r="1" />
                <line x1="12" y1="20" x2="12" y2="16" />
                <line x1="10" y1="18" x2="14" y2="18" />
            </svg>
            <span class="text">${category}</span>
        `;

        // Set the button's inner HTML to the SVG icon and category name
        button.innerHTML = svgIcon;

        // Add event listener for filtering contacts
        button.addEventListener('click', () => {
            filterContactsByCategory(category);
        });

        // Insert the button before the Add Category button
        sidebarFilters.insertBefore(button, document.getElementById('sidebarAddCategoryBtn'));
    });
}

// Filter contacts by category (including "All Contacts")
function filterContactsByCategory(category) {
    // Update the current category
    currentCategory = category;

    // Highlight the active category button
    const allButtons = document.querySelectorAll('.filter-btn');
    allButtons.forEach(btn => btn.classList.remove('active'));

    const activeButton = document.querySelector(`[data-category="${category}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }

    // Filter contacts based on the selected category
    searchBar.addEventListener('input', e => {
        renderContacts(currentCategory, e.target.value);
    });

    renderContacts(currentCategory, searchBar.value);
}

// Main Call Functions
fetchContacts();
renderContactStats();
renderContacts();


