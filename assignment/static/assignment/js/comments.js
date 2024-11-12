const url = `ws://${window.location.host+window.location.pathname}`;
const socket = new WebSocket(url);

const sendCommentButton = document.querySelector('.send-comment');
const commentArea = document.querySelector('.comment-area');
const commentsSection = document.querySelector('.comments-section');

commentsSection.scrollTop = commentsSection.scrollHeight;

socket.onmessage = (event) => {
    showNewComment(JSON.parse(event.data));
}

function showNewComment(comment) {
    const commentElement = document.createElement('div');
    const commentAuthor = document.createElement('div');
    const commentAuthorLink = document.createElement('a');
    const commentContent = document.createElement('div');
    const commentDate = document.createElement('div');

    commentElement.classList.add('comment-element');
    commentAuthor.classList.add('comment-author');
    commentAuthorLink.classList.add('user-link');
    commentContent.classList.add('comment-content');
    commentDate.classList.add('comment-date');

    commentAuthorLink.textContent = comment.created_by;
    commentContent.textContent = comment.content;
    commentDate.textContent = comment.created_at;

    commentAuthor.appendChild(commentAuthorLink);
    commentContent.appendChild(commentDate);

    commentElement.appendChild(commentAuthor);
    commentElement.appendChild(commentContent);

    commentsSection.appendChild(commentElement);

    commentsSection.scrollTop = commentsSection.scrollHeight;
}

function sendComment() {
    if (commentArea.value.trim()) {
        socket.send(JSON.stringify({
            'content': commentArea.value
        }));
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
