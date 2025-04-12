document.addEventListener('DOMContentLoaded', () => {
    const machineForm = document.getElementById('machineForm');

    machineForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(machineForm);
        const machineData = Object.fromEntries(formData.entries());

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
