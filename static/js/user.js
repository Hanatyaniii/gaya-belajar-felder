document.addEventListener("DOMContentLoaded", function() {
    // Get modals and buttons
    const addUserModal = document.getElementById("addUserModal");
    const editUserModal = document.getElementById("editUserModal");
    const deleteUserModal = document.getElementById("deleteUserModal");
    const closeButtons = document.getElementsByClassName("close");
    
    let userIdToEdit = null;
    let userIdToDelete = null;

    // Show the add user modal
    document.getElementById("addUserBtn").onclick = function() {
        addUserModal.style.display = "block";
    };

    // Show the edit user modal
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.onclick = function() {
            userIdToEdit = this.getAttribute('data-id');
            document.getElementById('editUsername').value = this.getAttribute('data-username');
            document.getElementById('editEmail').value = this.getAttribute('data-email');
            document.getElementById('editPassword').value = this.getAttribute('data-password');
            editUserModal.style.display = "block";
        };
    });

    // Show the delete confirmation modal
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.onclick = function() {
            userIdToDelete = this.getAttribute('data-id');
            deleteUserModal.style.display = "block";
        };
    });

    // Close modals
    Array.from(closeButtons).forEach(button => {
        button.onclick = function() {
            addUserModal.style.display = "none";
            editUserModal.style.display = "none";
            deleteUserModal.style.display = "none";
        };
    });

    window.onclick = function(event) {
        if (event.target === addUserModal) {
            addUserModal.style.display = "none";
        }
        if (event.target === editUserModal) {
            editUserModal.style.display = "none";
        }
        if (event.target === deleteUserModal) {
            deleteUserModal.style.display = "none";
        }
    };

    // Handle add user form submission
    document.getElementById('addUserForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const result = await response.json();
        alert(result.message);
        if (response.ok) {
            addUserModal.style.display = "none";
            location.reload();
        }
    });

    // Handle edit user form submission
    document.getElementById('editUserForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('editUsername').value;
        const email = document.getElementById('editEmail').value;
        const password = document.getElementById('editPassword').value;

        const response = await fetch(`/api/users/${userIdToEdit}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const result = await response.json();
        alert(result.message);
        if (response.ok) {
            editUserModal.style.display = "none";
            location.reload();
        }
    });

    // Handle delete user confirmation
    document.getElementById('confirmDelete').onclick = async function() {
        const response = await fetch(`/api/users/${userIdToDelete}`, {
            method: 'DELETE',
        });

        const result = await response.json();
        alert(result.message);
        if (response.ok) {
            deleteUserModal.style.display = "none";
            location.reload();
        }
    };

    document.getElementById('cancelDelete').onclick = function() {
        deleteUserModal.style.display = "none";
    };
});


// Handle sidebar menu active state
const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');
allSideMenu.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', function () {
        allSideMenu.forEach(i => {
            i.parentElement.classList.remove('active');
        });
        li.classList.add('active');
    });
});

// Toggle sidebar
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');
menuBar.addEventListener('click', function () {
    sidebar.classList.toggle('hide');
});
