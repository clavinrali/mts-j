document.addEventListener('DOMContentLoaded', () => {
    const currentUsername = document.getElementById('current-username').value;
    const userPanel = document.querySelector('.user-panel');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    userPanel.addEventListener('click', () => {
        dropdownMenu.classList.toggle('open');
    });

    document.addEventListener('click', (event) => {
        if (!userPanel.contains(event.target)) {
            dropdownMenu.classList.remove('open');
        }
    });

    const machineryList = document.getElementById('machinery-list');

    // Fetch machinery data and populate the list
    fetch('/api/machine/')
        .then(response => response.json())
        .then(data => {
            let machines = data.message || []; // Access the 'message' field if it exists
            machineryList.innerHTML = ''; // Clear existing content

            // Sort machines by priority in increasing order
            machines.sort((a, b) => a.priority - b.priority);

            machines.forEach(machine => {
                const machineryItem = document.createElement('div');
                machineryItem.classList.add('machinery-item');
                machineryItem.setAttribute('data-id', machine.id);
                machineryItem.innerHTML = `
                    <div class="machine-details">
                        <p class="machine-model"><strong>Name:</strong> ${machine.name}</p>
                        <p><strong>Model:</strong> ${machine.model}</p>
                        <p><strong>Machine ID:</strong> ${machine.unique_machine_id}</p>
                        <p><strong>Location:</strong> ${machine.location}</p>
                        <p><strong>Manufacturer:</strong> ${machine.manufacturer || 'N/A'}</p>
                        <p><strong>Last Service:</strong> ${machine.last_service}</p>
                    </div>
                    <div class="issue-details" id="issue-details-${machine.id}">
                        ${machine.current_case ? '<p>Loading case details...</p>' : '<!-- No issue -->'}
                    </div>
                    <div class="machinery-buttons">
                        <button class="assign-button">Assign</button>
                        <div class="status-indicator" id="${machine.status.toLowerCase()}-status">${machine.status.toUpperCase()}</div>
                    </div>
                `;
                machineryList.appendChild(machineryItem);

                // Fetch case details if the machine has a current case
                if (machine.current_case) {
                    fetch(`/api/case/${machine.current_case}/`)
                        .then(caseResponse => caseResponse.json())
                        .then(caseData => {
                            const issueDetails = document.getElementById(`issue-details-${machine.id}`);
                            issueDetails.innerHTML = `
                                <div class="issue-box">
                                    <p><strong>Case #:</strong> ${caseData.message.id}</p>
                                    <p><strong>Details:</strong> ${caseData.message.title}</p>
                                </div>
                            `;
                        })
                        .catch(error => console.error(`Error fetching case details for machine ${machine.id}:`, error));
                }
            });
        })
        .catch(error => console.error('Error fetching machinery data:', error));
});

// Create a custom dialog box
const createDialogBox = (message) => {
    const dialog = document.createElement('div');
    dialog.classList.add('custom-dialog');
    dialog.innerHTML = `
        <div class="dialog-content">
            <p>${message}</p>
            <select class="role-dropdown">
                <option value="None">Select a Role</option>
                <option value="technician">Technician</option>
                <option value="repair">Repair Personnel</option>
            </select>
            <select class="dialog-dropdown">
                <option value="">Select an employee</option>
            </select>
            <div class="dialog-buttons">
                <button class="assign-dialog">Assign</button>
                <button class="close-dialog">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(dialog);

    // Fetch employees based on selected role
    const roleDropdown = dialog.querySelector('.role-dropdown');
    const dialogDropdown = dialog.querySelector('.dialog-dropdown');
    roleDropdown.addEventListener('change', () => {
        const selectedRole = roleDropdown.value;
        if (selectedRole !== "None") {
            fetch(`/api/employees/by_role/?role=${selectedRole}`)
                .then(response => response.json())
                .then(data => {
                    const employees = data.message || [];
                    dialogDropdown.innerHTML = employees.map(employee => `<option value="${employee.id}">${employee.full_name}</option>`).join('');
                })
                .catch(error => console.error('Error fetching employees:', error));
        } else {
            dialogDropdown.innerHTML = '<option value="">Select an employee</option>';
        }
    });

    // Close dialog functionality
    dialog.querySelector('.close-dialog').addEventListener('click', () => {
        document.body.removeChild(dialog);
    });

    // Assign button functionality
    dialog.querySelector('.assign-dialog').addEventListener('click', () => {
        const selectedRole = roleDropdown.value;
        const selectedValue = dialogDropdown.value;
        console.log(`Assigned Role: ${selectedRole}, Assigned: ${selectedValue}`); // Replace with actual assignment logic
        document.body.removeChild(dialog);
    });
};

// Function to create a delete dialog box
const createDeleteDialogBox = () => {
    const dialog = document.createElement('div');
    dialog.classList.add('custom-dialog');
    dialog.innerHTML = `
        <div class="dialog-content">
            <p>Select a machine to delete:</p>
            <select class="dialog-dropdown">
                <option value="">Loading machines...</option>
            </select>
            <div class="dialog-buttons">
                <button class="delete-dialog">Delete</button>
                <button class="close-dialog">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(dialog);

    const dialogDropdown = dialog.querySelector('.dialog-dropdown');

    // Fetch machine details and populate the dropdown
    fetch('/api/machine/')
        .then(response => response.json())
        .then(data => {
            const machines = data.message || [];
            dialogDropdown.innerHTML = machines.map(machine => `
                <option value="${machine.id}">
                    ${machine.name} - ${machine.unique_machine_id} - ${machine.model || 'N/A'} - ${machine.location}
                </option>
            `).join('');
        })
        .catch(error => {
            console.error('Error fetching machines:', error);
            dialogDropdown.innerHTML = '<option value="">Error loading machines</option>';
        });

    // Close dialog functionality
    dialog.querySelector('.close-dialog').addEventListener('click', () => {
        document.body.removeChild(dialog);
    });

    // Helper function to get CSRF token
    const getCSRFToken = () => {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    };

    // Delete button functionality
    dialog.querySelector('.delete-dialog').addEventListener('click', () => {
        const selectedMachineId = dialogDropdown.value;
        if (selectedMachineId) {
            fetch(`/api/machine/${selectedMachineId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken() // Include CSRF token
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Machine deleted successfully');
                    document.body.removeChild(dialog);
                    location.reload(); // Reload the page to reflect changes
                } else {
                    alert('Error deleting machine: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error deleting machine:', error);
                alert('An error occurred while deleting the machine.');
            });
        } else {
            alert('Please select a machine to delete.');
        }
    });
};

// Modify event listener for assign buttons
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('assign-button')) {
        event.stopPropagation(); // Prevent machinery-item click event
        createDialogBox('Select an option to assign:');
        return; // Exit to ensure no further processing
    }

    if (event.target.closest('.machinery-item')) {
        const machineryItem = event.target.closest('.machinery-item');
        const machineId = machineryItem.getAttribute('data-id'); // Get machineId from data-id
        window.location.href = `/machine/${machineId}/info/`; // Redirect to machine info page
    }
});

// Add event listener for the delete button
document.addEventListener('DOMContentLoaded', () => {
    const deleteMachineButton = document.getElementById('delete-machine-btn');
    if (deleteMachineButton) {
        deleteMachineButton.addEventListener('click', () => {
            createDeleteDialogBox();
        });
    }
});