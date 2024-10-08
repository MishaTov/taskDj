const showAttachmentsButton = document.querySelector('.show-attachments-button');
const attachments = document.querySelector('.attachments-element');

const deleteFileButtons = document.querySelectorAll('.delete-file');
const taskForm = document.getElementById('task-form');
const filesToDelete = document.getElementById('files-to-delete');

showAttachmentsButton.addEventListener('click', () => {
    if (attachments.classList.contains('hidden')) {
        showAttachmentsButton.textContent = showAttachmentsButton.textContent.replace('↓', '↑');
        attachments.classList.remove('hidden');
    } else {
        showAttachmentsButton.textContent = showAttachmentsButton.textContent.replace('↑', '↓');
        attachments.classList.add('hidden');
    }
})

taskForm.addEventListener('submit', (event) => {
    event.preventDefault();
    deleteFileButtons.forEach(button => {
        if (button.checked) {
            filesToDelete.value += button.value + ' ';
        }
    })
    taskForm.submit();
})
