const commentArea = document.querySelector('.comment-area');

const commentList = document.querySelectorAll('.comment-element');
const sendCommentButton = document.querySelector('.send-comment');
const editCommentButtons = document.querySelectorAll('.comment-button.edit');
const deleteCommentButtons = document.querySelectorAll('.comment-button.delete');

const commentTempInfo = {
    'editId': null,
    'deleteId': null,
    'content': null
}

function sendViaSocket(event) {
    const data = {'event': event}
    if (data.event === 'comment.post') {
        data.content = commentArea.value.trimEnd();
    } else if (data.event === 'comment.edit') {
        data.uuid = commentTempInfo.editId;
        data.content = commentArea.value.trimEnd();
    } else if (data.event === 'comment.delete') {
        data.uuid = commentTempInfo.deleteId;
    }
    socket.send(JSON.stringify(data));
}


function sendComment() {
    if (!commentTempInfo.editId && commentArea.value.trim()) {
        sendViaSocket('comment.post');
    } else if (commentTempInfo.editId && commentTempInfo.content !== commentArea.value.trimEnd()) {
        sendViaSocket('comment.edit');
    }
    commentArea.value = '';
    commentTempInfo.editId = null;
    commentTempInfo.content = null;
}

function editComment(id, content) {
    commentTempInfo.editId = id.replace('comment-', '');
    commentArea.value = commentTempInfo.content = content;
    commentArea.focus();
}

function deleteComment(id) {
    commentTempInfo.deleteId = id.replace('comment-', '');
    if (commentTempInfo.deleteId === commentTempInfo.editId) {
        commentTempInfo.editId = null;
        commentTempInfo.content = null;
        commentArea.value = ''
        commentArea.blur();
    }
    sendViaSocket('comment.delete');
    commentTempInfo.deleteId = null;
}


function showHideCommentActionButtons(commentElement, buttonsParentElement) {
    commentElement.onmouseover = () => {
        if (buttonsParentElement.classList.contains('hidden')) {
            buttonsParentElement.classList.remove('hidden');
        }
    }
    commentElement.onmouseout = () => {
        if (!buttonsParentElement.classList.contains('hidden')) {
            buttonsParentElement.classList.add('hidden');
        }
    }
}


function editClickEvent(editButton) {
    editButton.addEventListener('click', () => {
        const commentElement = editButton.closest('.comment-element');
        const currentContent = commentElement.querySelector('.comment-content').textContent;
        editComment(commentElement.id, currentContent);
    });
}


function deleteClickEvent(deleteButton) {
    deleteButton.addEventListener('click', () => {
        deleteComment(deleteButton.closest('.comment-element').id);
    });
}


sendCommentButton.addEventListener('click', () => {
    sendComment();
});

commentList.forEach(element => {
    const commentActionButtons = element.querySelector('.comment-action-buttons');
    if (commentActionButtons) {
        showHideCommentActionButtons(element, commentActionButtons);
    }
});

editCommentButtons.forEach(element => {
    editClickEvent(element);
});

deleteCommentButtons.forEach(element => {
    deleteClickEvent(element);
});

commentArea.onkeydown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendComment();
    } else if (e.key === 'Escape') {
        commentTempInfo.editId = null;
        commentTempInfo.content = null;
        commentArea.value = '';
        commentArea.blur();
    }
}
