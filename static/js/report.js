document.addEventListener('DOMContentLoaded', function() {
    // Get references to the modal and buttons
    const deleteModal = document.getElementById('deleteUserModal');
    const confirmDeleteButton = document.getElementById('confirmDelete');
    const cancelDeleteButton = document.getElementById('cancelDelete');
    const closeModalSpan = deleteModal.querySelector('.close');
    
    // Variable to store the ID of the user to be deleted
    let userIdToDelete = null;

    // Function to open the delete confirmation modal
    function openDeleteModal(userId) {
        userIdToDelete = userId;
        deleteModal.style.display = 'block';
    }

    // Function to close the delete confirmation modal
    function closeDeleteModal() {
        deleteModal.style.display = 'none';
        userIdToDelete = null;
    }

    // Event listener for view buttons
    document.querySelectorAll('.view-btn').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-id');
            // For demonstration, just show an alert. Replace with your view logic.
            alert(`View details for user ID: ${userId}`);
            // You can also redirect to a detailed view page:
            // window.location.href = `/view_user/${userId}`;
        });
    });

    // Event listener for delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-id');
            openDeleteModal(userId);
        });
    });

    // Event listener for the confirm delete button
    confirmDeleteButton.addEventListener('click', function() {
        if (userIdToDelete) {
            // Perform the delete operation
            fetch(`/delete_user/${userIdToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: userIdToDelete })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove the row from the table
                    document.querySelector(`tr[data-id="${userIdToDelete}"]`).remove();
                    closeDeleteModal();
                } else {
                    alert('Failed to delete the user.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the user.');
            });
        }
    });

    // Event listener for the cancel delete button
    cancelDeleteButton.addEventListener('click', function() {
        closeDeleteModal();
    });

    // Event listener for the close (X) button in the modal
    closeModalSpan.addEventListener('click', function() {
        closeDeleteModal();
    });

    // Close the modal if the user clicks outside of it
    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) {
            closeDeleteModal();
        }
    });
});
