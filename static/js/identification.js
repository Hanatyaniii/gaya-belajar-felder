document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const modal = document.getElementById('deleteUserModal');
    const confirmDelete = document.getElementById('confirmDelete');
    const cancelDelete = document.getElementById('cancelDelete');
    let dataIdToDelete = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            dataIdToDelete = this.getAttribute('data-id');
            console.log('Delete button clicked, data-id:', dataIdToDelete);
            modal.style.display = 'block';
        });
    });

    cancelDelete.addEventListener('click', function () {
        modal.style.display = 'none';
        dataIdToDelete = null;
    });

    confirmDelete.addEventListener('click', function () {
        if (dataIdToDelete) {
            console.log('Confirm delete clicked, data-id:', dataIdToDelete);
            fetch(`/api/Responden/${dataIdToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Server response:', data);
                    if (data.success) {
                        const row = document.querySelector(`tr[data-id='${dataIdToDelete}']`);
                        row.remove();
                        modal.style.display = 'none';
                        dataIdToDelete = null;
                    } else {
                        alert(data.message || 'Error deleting assessment');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    const closeBtn = document.querySelector('.close');
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
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
