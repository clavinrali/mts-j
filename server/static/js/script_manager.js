document.addEventListener('DOMContentLoaded', () => {
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
            const machines = data.message || []; // Access the 'message' field if it exists
            machineryList.innerHTML = ''; // Clear existing content
            machines.forEach(machine => {
                const machineryItem = document.createElement('div');
                machineryItem.classList.add('machinery-item');
                machineryItem.innerHTML = `
                    <div class="machine-details">
                        <p class="machine-model"><strong>Model:</strong> ${machine.name}</p>
                        <p><strong>Location:</strong> ${machine.location}</p>
                        <p><strong>Manufacturer:</strong> ${machine.model}</p>
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
                    dialogDropdown.innerHTML = employees.map(employee => `<option value="${employee.id}">${employee.username}</option>`).join('');
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

// Modify event listener for assign buttons
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('assign-button')) {
        createDialogBox('Select an option to assign:');
    }
});