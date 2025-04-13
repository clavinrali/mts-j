// Technician-specific JavaScript code
function loadAssignedTasks() {
    const creatorId = document.getElementById('current-userid').value;
    fetch('/api/tasks/assigned/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch tasks');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const taskListContainer = document.querySelector('.task-list');
                taskListContainer.innerHTML = ''; // Clear existing tasks
                if (data.tasks.length > 0) {
                    data.tasks.forEach(task => {
                        const taskItem = document.createElement('li');
                        taskItem.className = 'task-item';
                        taskItem.innerHTML = `
                            <div class="task-container">
                                <span>Machine: ${task.machine}</span>
                                <span>Status: ${task.status}</span>
                                <span>Creator: ${task.creator}</span>
                                <span>Assigned Date: ${task.created_at}</span>
                            </div>
                        `;
                        taskListContainer.appendChild(taskItem);
                    });
                } else {
                    taskListContainer.innerHTML = '<li class="task-item"><div class="task-container">No tasks assigned</div></li>';
                }
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading tasks:', error);
        });

    const machineryList = document.getElementById('machinery-list');
    // Fetch and display machines assigned to the user
    fetch('/api/machine/user/' + creatorId + '/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch machines');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
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
                        <div class="status-indicator" id="${machine.status.toLowerCase()}-status">${machine.status.toUpperCase()}</div>
                    </div>
                `;
                machineryList.appendChild(machineryItem);
            });
                 } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading machines:', error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
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
    loadAssignedTasks();
});