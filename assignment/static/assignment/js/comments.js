const url = `ws://${window.location.host+window.location.pathname}`;
const socket = new WebSocket(url);

const sendComment = document.querySelector('.send-comment');
const commentArea = document.querySelector('.comment-area');

sendComment.addEventListener('click', () => {
    socket.send(commentArea.value);
});
