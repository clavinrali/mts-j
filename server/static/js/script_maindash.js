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