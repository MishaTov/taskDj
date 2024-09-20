const assignmentForm = document.querySelector('.task-form');


for (let element of assignmentForm) {
    element.addEventListener('invalid', (event) => {
        event.preventDefault();
        element.classList.add('invalid');
        const errorMsg = element.parentNode.querySelector('.field-error-msg');
        if (!errorMsg){
            const errorMsg = document.createElement('p');
            errorMsg.classList.add('field-error-msg');
            errorMsg.innerHTML = element.validationMessage;
            element.parentNode.appendChild(errorMsg);
        } else {
            errorMsg.innerHTML = element.validationMessage;
        }
    })
}