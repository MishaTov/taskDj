const dropdownElements = document.querySelectorAll('.dropdown-element');
const orderingButton = document.querySelector('.ordering-button.b');


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
        let param;
        if (dropdownElement.classList.contains('pagination')) {
            param = 'paginate_by';
        } else if (dropdownElement.classList.contains('ordering')) {
            param = 'order_by';
        }
        element.addEventListener('click', (event) => {
            if (event.target.textContent === dropdownButton.textContent) {
                dropdownListOptions.style.display = 'none';
            } else {
                const params = new URLSearchParams(window.location.search);
                params.set(param, event.target.getAttribute('value'));
                window.location.href = `${window.location.pathname}?${params.toString()}`;
            }
        });
    });
}


dropdownElements.forEach(element => {
    adjustDropdownElement(element);
});

orderingButton.addEventListener('click', () => {
    const params = new URLSearchParams(window.location.search);
    const value = orderingButton.getAttribute('reverse');
    if (value === 'False') {
        params.set('reverse', 'True');
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    } else if (value === 'True') {
        params.delete('reverse');
        window.location.href = `${window.location.pathname}?${params.toString()}`;
    }
});
