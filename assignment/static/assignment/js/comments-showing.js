const url = `ws://${window.location.host + window.location.pathname}`;
const socket = new WebSocket(url);

const commentsSection = document.querySelector('.comments-section');

commentsSection.scrollTop = commentsSection.scrollHeight;


function createCommentButton(buttonType) {
    const commentButton = document.createElement('button');
    commentButton.classList.add('comment-button', buttonType);
    commentButton.type = 'button';

    const commentIcon = document.createElement('img');
    commentIcon.classList.add('comment-button');
    commentIcon.src = `/static/assignment/img/${buttonType}_comment.png`;
    commentIcon.alt = `${buttonType} comment`;

    commentButton.appendChild(commentIcon);
    return commentButton;
}


function postCommentElement(comment) {
    const newCommentElement = document.createElement('div');
    newCommentElement.classList.add('comment-element');
    newCommentElement.setAttribute('id', `comment-${comment.uuid}`)

    const newCommentAuthor = document.createElement('div');
    newCommentAuthor.classList.add('comment-author');

    const newCommentAuthorLink = currentUser === comment.created_by ?
        document.createElement('span') :
        document.createElement('a');
    newCommentAuthorLink.classList.add('user-link', 'comment');

    const newCommentContentElement = document.createElement('div');
    newCommentContentElement.classList.add('comment-content-element');

    const newCommentContent = document.createElement('span');
    newCommentContent.classList.add('comment-content');
    newCommentContent.textContent = comment.content;

    const newCommentFooter = document.createElement('div');
    newCommentFooter.classList.add('comment-footer');

    const newCommentDate = document.createElement('div');
    newCommentDate.classList.add('comment-date');
    newCommentDate.textContent = comment.created_at;

    let newCommentActionButtons;

    if (currentUser === comment.created_by) {
        newCommentAuthorLink.classList.add('author');
        newCommentAuthorLink.textContent = 'you';

        newCommentContentElement.classList.add('author');

        newCommentActionButtons = document.createElement('div');
        newCommentActionButtons.classList.add('comment-action-buttons', 'hidden');

        const newCommentEditButton = createCommentButton('edit');
        const newCommentDeleteButton = createCommentButton('delete');

        editClickEvent(newCommentEditButton);
        deleteClickEvent(newCommentDeleteButton);

        newCommentActionButtons.appendChild(newCommentEditButton);
        newCommentActionButtons.appendChild(newCommentDeleteButton);

        showHideCommentActionButtons(newCommentElement, newCommentActionButtons);
    } else {
        newCommentAuthorLink.textContent = comment.created_by;
        newCommentAuthorLink.href = '#';
    }


    newCommentAuthor.appendChild(newCommentAuthorLink);
    if (typeof newCommentActionButtons !== 'undefined') {
        newCommentAuthor.appendChild(newCommentActionButtons);
    }

    newCommentFooter.appendChild(newCommentDate);

    newCommentContentElement.appendChild(newCommentContent);
    newCommentContentElement.appendChild(newCommentFooter);

    newCommentElement.appendChild(newCommentAuthor);
    newCommentElement.appendChild(newCommentContentElement);

    commentsSection.appendChild(newCommentElement);

    if (currentUser === comment.created_by) {
        commentsSection.scrollTop = commentsSection.scrollHeight;
    }
}


function editCommentElement(comment) {
    const commentElement = document.getElementById(`comment-${comment.uuid}`);
    commentElement.querySelector('.comment-content').textContent = comment.content;
    const isEdited = commentElement.querySelector('.comment-edited-label');
    if (!isEdited) {
        const commentEditedLabel = document.createElement('span');
        commentEditedLabel.classList.add('comment-edited-label');
        commentEditedLabel.innerHTML = 'edited' + '&nbsp';
        commentElement.querySelector('.comment-footer').prepend(commentEditedLabel);
    }
}


function deleteCommentElement(comment) {
    const commentElement = document.getElementById(`comment-${comment.uuid}`);
    commentElement.remove();
}


socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'comment.post') {
        postCommentElement(data);
    } else if (data.event === 'comment.edit') {
        editCommentElement(data);
    } else if (data.event === 'comment.delete') {
        deleteCommentElement(data);
    }
}
