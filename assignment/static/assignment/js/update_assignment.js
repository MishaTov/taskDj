const deleteFileButtons = document.querySelectorAll('.delete-file');
const taskForm = document.getElementById('task-form');
const filesToDelete = document.getElementById('files-to-delete');
const selectAllFiles = document.getElementById('select-all');
const fileListToDelete = new Set();


selectAllFiles.addEventListener('click', () => {
    deleteFileButtons.forEach(button => {
        if (selectAllFiles.checked) {
            button.checked = true;
            fileListToDelete.add(button.value);
        } else {
            button.checked = false;
            fileListToDelete.delete(button.value);
        }
    });
});


deleteFileButtons.forEach(button => {
    button.addEventListener('click', () => {
        if (button.checked) {
            fileListToDelete.add(button.value);
        } else {
            fileListToDelete.delete(button.value);
        }
        selectAllFiles.checked = fileListToDelete.size === deleteFileButtons.length;
    });
})


taskForm.addEventListener('submit', (event) => {
    event.preventDefault();
    filesToDelete.value = Array.from(fileListToDelete).join(' ');
    console.log(filesToDelete);
    taskForm.submit();
});
