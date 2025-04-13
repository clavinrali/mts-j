document.addEventListener('DOMContentLoaded', () => {
    const machineForm = document.getElementById('machineForm');
    const warningCodeInput = document.getElementById('warningCodeInput');
    const warningDescriptionInput = document.getElementById('warningDescriptionInput');
    const addWarningBtn = document.getElementById('addWarningBtn');
    const warningList = document.getElementById('warningList');
    const warnings = [];

    addWarningBtn.addEventListener('click', () => {
        const code = warningCodeInput.value.trim();
        const description = warningDescriptionInput.value.trim();
        if (code && description) {
            warnings.push({ code, description });
            const listItem = document.createElement('li');
            listItem.textContent = `${code}: ${description}`;
            warningList.appendChild(listItem);
            warningCodeInput.value = '';
            warningDescriptionInput.value = '';
        } else {
            alert('Please provide both a warning code and description.');
        }
    });

    machineForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(machineForm);
        const machineData = Object.fromEntries(formData.entries());
        machineData.supported_warnings = warnings;

        fetch('/api/machine/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Ensure CSRF token is included
            },
            body: JSON.stringify(machineData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Machine created successfully!');
                window.location.href = '/dashboard/'; // Redirect to dashboard
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error creating machine:', error);
            alert('An error occurred while creating the machine.');
        });
    });

    // Helper function to get CSRF token
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
});
