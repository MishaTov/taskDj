const forms = document.querySelectorAll('form')


for (let form of forms) {
    for (let element of form) {
        element.addEventListener('invalid', (event) => {
            event.preventDefault();
            element.classList.add('invalid');
            const errorMsg = element.parentNode.querySelector('.field-error-msg');
            if (!errorMsg) {
                const errorMsg = document.createElement('p');
                errorMsg.classList.add('field-error-msg');
                errorMsg.innerHTML = element.validationMessage;
                element.parentNode.appendChild(errorMsg);
            } else {
                errorMsg.innerHTML = element.validationMessage;
            }
        })
        if (element.getAttribute('aria-invalid') === 'true') {
            element.classList.add('invalid');
        }
    }
}