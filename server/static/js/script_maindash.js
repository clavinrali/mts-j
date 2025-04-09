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
});