const deleteFileButtons = document.querySelectorAll('.delete-file');
const taskForm = document.getElementById('task-form');
const filesToDelete = document.getElementById('files-to-delete');


taskForm.addEventListener('submit', (event) => {
    event.preventDefault();
    deleteFileButtons.forEach(button => {
        if (button.checked) {
            filesToDelete.value += button.value + ' ';
        }
    })
    taskForm.submit();
})
