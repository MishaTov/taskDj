const commentArea = document.querySelector('.comment-area');

const commentList = document.querySelectorAll('.comment-element');
const sendCommentButton = document.querySelector('.send-comment');
const editCommentButtons = document.querySelectorAll('.comment-button.edit');
const deleteCommentButtons = document.querySelectorAll('.comment-button.delete');

let tempContent = null;
let currentCommentId = null;


commentList.forEach(element => {
    const commentActionButtons = element.querySelector('.comment-action-buttons');
    element.onmouseover = () => {
        commentActionButtons.classList.remove('hidden');
    }
    element.onmouseout = () => {
        commentActionButtons.classList.add('hidden');
    }
})


function sendViaSocket(event) {
    const data = {'event': event}
    if (data.event === 'comment.post') {
        data.content = commentArea.value.trimEnd();
    } else if (data.event === 'comment.edit') {
        data.uuid = currentCommentId;
        data.content = commentArea.value.trimEnd();
    } else if (data.event === 'comment.delete') {
        data.uuid = currentCommentId;
    }
    socket.send(JSON.stringify(data));
}


function sendComment() {
    if (!currentCommentId && commentArea.value.trim()) {
        sendViaSocket('comment.post');
    } else if (currentCommentId && tempContent !== commentArea.value.trimEnd()){
        sendViaSocket('comment.edit');
    }
    commentArea.value = '';
    currentCommentId = null;
    tempContent = null;
}

function editComment(id, content) {
    currentCommentId = id.replace('comment-', '');
    commentArea.value = tempContent = content;
}

function deleteComment(id) {
    currentCommentId = id.replace('comment-', '');
    sendViaSocket('comment.delete')
}

sendCommentButton.addEventListener('click', () => {
    sendComment();
});

editCommentButtons.forEach(element => {
    element.addEventListener('click', () => {
        const commentElement = element.closest('.comment-element');
        const currentContent = commentElement.querySelector('.comment-content').textContent;
        editComment(commentElement.id, currentContent);
    });
});

deleteCommentButtons.forEach(element => {
    element.addEventListener('click', () => {
        deleteComment(element.closest('.comment-element').id);
    });
});

commentArea.onkeydown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendComment();
    } else if (e.key === 'Escape') {
        commentArea.value = '';
        commentArea.blur();
        currentCommentId = null;
    }
}
