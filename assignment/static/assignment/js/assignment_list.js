// const paginateForm = document.getElementById('paginate-form')
//
// paginateForm.addEventListener('change', (event) => {
//     const params = new URLSearchParams(window.location.search);
//     params.set('paginate_by', event.target.value);
//     window.location.href = `${window.location.pathname}?${params.toString()}`;
// })
//

// .paginate-by-element:hover .dropdown-paginate-by {
//     display: block;
// }

const paginateButton = document.querySelector('.paginate-button');
const paginateContent = document.querySelector('.dropdown-paginate-by');
const paginateByLinks = document.querySelectorAll('.dropdown-paginate-by span')

paginateButton.addEventListener('click', () => {
    if (paginateContent.style.display === '' || paginateContent.style.display === 'none') {
        paginateContent.style.display = 'block';
    } else {
        paginateContent.style.display = 'none';
    }
})

document.addEventListener('click', (event) => {
    if (!paginateButton.contains(event.target) && !paginateContent.contains(event.target)) {
        paginateContent.style.display = 'none';
    }
});

paginateByLinks.forEach(element => {
    element.addEventListener('click', (event) => {
        if (event.target.textContent === paginateButton.textContent) {
            paginateContent.style.display = 'none';
        } else {
            const params = new URLSearchParams(window.location.search);
            params.set('paginate_by', event.target.textContent);
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        }
    })
})