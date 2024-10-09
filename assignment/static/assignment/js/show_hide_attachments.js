const showAttachmentsButton = document.querySelector('.show-attachments-button');
const attachments = document.querySelector('.attachments-section');


showAttachmentsButton.addEventListener('click', () => {
    if (attachments.classList.contains('hidden')) {
        showAttachmentsButton.textContent = showAttachmentsButton.textContent.replace('↓', '↑');
        attachments.classList.remove('hidden');
    } else {
        showAttachmentsButton.textContent = showAttachmentsButton.textContent.replace('↑', '↓');
        attachments.classList.add('hidden');
    }
})
