const paginateForm = document.getElementById('paginate-form')

paginateForm.addEventListener('change', (event) => {
    const params = new URLSearchParams(window.location.search);
    params.set('paginate_by', event.target.value);
    paginateForm.action += '?' + params.toString();
    paginateForm.submit();
})

