const assignmentForm = document.querySelector('.task-form');


for (let element of assignmentForm) {
    element.addEventListener('invalid', (event) => {
        event.preventDefault();
        element.classList.add('invalid');
        console.log(element.validationMessage);
    })
}