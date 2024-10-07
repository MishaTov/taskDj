const showAttachmentsButton = document.querySelector('.show-attachments-button');
const attachmentsList = document.querySelector('.attachments');

const deleteFileButtons = document.querySelectorAll('.delete-file-button');
let totalAttachments = deleteFileButtons.length;

showAttachmentsButton.addEventListener('click', () => {
    if (attachmentsList.classList.contains('hidden')) {
        showAttachmentsButton.textContent = showAttachmentsButton.textContent.replace('↓', '↑');
        attachmentsList.classList.remove('hidden');
    } else {
        showAttachmentsButton.textContent = showAttachmentsButton.textContent.replace('↑', '↓');
        attachmentsList.classList.add('hidden');
    }
})

deleteFileButtons.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.remove();
        totalAttachments -= 1;
        if (!totalAttachments) {
            attachmentsList.remove();
            showAttachmentsButton.remove();
        }
    });
})
