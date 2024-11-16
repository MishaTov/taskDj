const url = `ws://${window.location.host + window.location.pathname}`;
const socket = new WebSocket(url);

const commentsSection = document.querySelector('.comments-section');

commentsSection.scrollTop = commentsSection.scrollHeight;

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'comment.post') {
        showNewComment(data);
    } else if (data.event === 'comment.edit') {
        editCommentElement(data);
    } else if (data.event === 'comment.delete') {
        deleteCommentElement(data.uuid);
    }
}

function showNewComment(comment) {
    const commentElement = document.createElement('div');
    const commentAuthor = document.createElement('div');
    const commentAuthorLink = document.createElement('a');
    const commentContentElement = document.createElement('div');
    const commentContent = document.createElement('span');
    const commentDate = document.createElement('div');

    let commentActionButtons;

    if (currentUser === comment.created_by) {
        commentActionButtons = document.createElement('div');
        const editCommentButton = document.createElement('button');
        const deleteCommentButton = document.createElement('button');
        const editCommentIcon = document.createElement('img');
        const deleteCommentIcon = document.createElement('img');

        commentActionButtons.classList.add('comment-action-buttons');
        editCommentButton.classList.add('comment-button', 'edit');
        deleteCommentButton.classList.add('comment-button', 'delete');
        editCommentIcon.classList.add('comment-button');
        deleteCommentIcon.classList.add('comment-button');

        editCommentIcon.src = '/static/assignment/img/edit_comment.png';
        editCommentIcon.alt = 'Edit comment';
        deleteCommentIcon.src = '/static/assignment/img/delete_comment.png';
        deleteCommentIcon.alt = 'Delete comment';

        editCommentButton.appendChild(editCommentIcon);
        deleteCommentButton.appendChild(deleteCommentIcon);

        commentActionButtons.appendChild(editCommentButton);
        commentActionButtons.appendChild(deleteCommentButton);
    }

    commentElement.classList.add('comment-element');
    commentAuthor.classList.add('comment-author');
    commentAuthorLink.classList.add('user-link');
    commentContentElement.classList.add('comment-content-element');
    commentContent.classList.add('comment-content');
    if (currentUser === comment.created_by) {
        commentContentElement.classList.add('author');
    }
    commentDate.classList.add('comment-date');

    commentElement.setAttribute('id', `comment-${comment.uuid}`)
    commentAuthorLink.textContent = comment.created_by;
    commentContent.textContent = comment.content;
    commentDate.textContent = comment.created_at;

    commentAuthor.appendChild(commentAuthorLink);
    if (typeof commentActionButtons !== 'undefined') {
        commentAuthor.appendChild(commentActionButtons);
    }
    commentContentElement.appendChild(commentContent);
    commentContentElement.appendChild(commentDate);

    commentElement.appendChild(commentAuthor);
    commentElement.appendChild(commentContentElement);

    commentsSection.appendChild(commentElement);

    commentsSection.scrollTop = commentsSection.scrollHeight;
}

function editCommentElement(comment) {
    const commentElement = document.getElementById(`comment-${comment.uuid}`);
    commentElement.querySelector('.comment-content').textContent = comment.content;
}

function deleteCommentElement(comment_uuid) {
    const commentElement = document.getElementById(`comment-${comment_uuid}`);
    commentElement.remove();
}
