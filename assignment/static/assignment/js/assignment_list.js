const dropdownElements = document.querySelectorAll('.dropdown-element');


function adjustDropdownElement(dropdownElement) {
    const dropdownButton = dropdownElement.querySelector('.dropdown-button');
    const dropdownListOptions = dropdownElement.querySelector('.dropdown-list-options');
    const dropdownOptions = dropdownElement.querySelectorAll('.dropdown-list-options span');

    dropdownButton.addEventListener('click', () => {
        if (dropdownListOptions.style.display === '' || dropdownListOptions.style.display === 'none') {
            dropdownListOptions.style.display = 'block';
        } else {
            dropdownListOptions.style.display = 'none';
        }
    })

    document.addEventListener('click', (event) => {
        if (!dropdownButton.contains(event.target) && !dropdownListOptions.contains(event.target)) {
            dropdownListOptions.style.display = 'none';
        }
    });

    dropdownOptions.forEach(element => {
        element.addEventListener('click', (event) => {
            if (event.target.textContent === dropdownButton.textContent) {
                dropdownListOptions.style.display = 'none';
            } else {
                const params = new URLSearchParams(window.location.search);
                params.set('paginate_by', event.target.textContent);
                window.location.href = `${window.location.pathname}?${params.toString()}`;
            }
        });
    });
}


dropdownElements.forEach(element => {
    adjustDropdownElement(element);
});
