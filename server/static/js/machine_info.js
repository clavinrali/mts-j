function updateActiveWarnings() {
    fetch(`/api/machine/${machineId}/active_warnings/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const warningListContainer = document.querySelector('.active-warning-list');
                warningListContainer.innerHTML = ''; // Clear existing warnings

                if (data.warnings.length > 0) {
                    data.warnings.forEach(warning => {
                        const warningItem = document.createElement('div');
                        warningItem.className = 'warning-item';
                        warningItem.textContent = `⚠️ ${warning.code} - ${warning.description}`;

                        const deleteButton = document.createElement('button');
                        deleteButton.className = 'btn delete-btn';
                        deleteButton.textContent = 'Delete';
                        deleteButton.onclick = () => deleteWarning(warning.id);

                        warningItem.appendChild(deleteButton);
                        warningListContainer.appendChild(warningItem);
                    });
                } else {
                    warningListContainer.innerHTML = '<p>No warnings available.</p>';
                }
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the warnings list.');
        });
}

function setWarning() {
    const warningSelect = document.getElementById('warning-select');
    const warningId = warningSelect.value;

    if (!warningId) {
        alert('Please select a warning.');
        return;
    }

    fetch(`/api/machine/${machineId}/set_warning/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ warning_id: warningId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Warning set successfully!');
            updateActiveWarnings(); // Update the active warnings list
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while setting the warning.');
    });
}

function deleteWarning(warningId) {
    if (!warningId) {
        alert('Please select a warning to delete.');
        return;
    }

    fetch(`/api/machine/${machineId}/delete_warning/${warningId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Warning deleted successfully!');
            updateActiveWarnings(); // Update the active warnings list
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the warning.');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    updateActiveWarnings();
});
