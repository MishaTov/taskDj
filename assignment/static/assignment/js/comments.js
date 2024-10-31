const url = `ws://${window.location.host+window.location.pathname}`;
const socket = new WebSocket(url);

const sendCommentButton = document.querySelector('.send-comment');
const commentArea = document.querySelector('.comment-area');


function sendComment() {
    if (commentArea.value.trim()) {
        socket.send(commentArea.value);
    }
    commentArea.value = '';
}

sendCommentButton.addEventListener('click', () => {
    sendComment();
});

commentArea.onkeydown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendComment();
    } else if (e.key === 'Escape') {
        commentArea.value = '';
        commentArea.blur();
    }
}
