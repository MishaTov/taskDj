const deleteAssignmentButton = document.getElementById('delete-assignment');
const deleteAssignmentBackground = document.querySelector('.delete-assignment-background');
const cancelAssignmentDeletionButton = document.getElementById('cancel-assignment-deletion');


deleteAssignmentButton.addEventListener('click', () => {
    deleteAssignmentBackground.classList.remove('hidden');
});

cancelAssignmentDeletionButton.addEventListener('click', () => {
    deleteAssignmentBackground.classList.add('hidden');
});