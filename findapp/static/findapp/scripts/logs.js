document.getElementById('username').addEventListener('input', function (e) {
    e.target.value = e.target.value.replace(/[^\w\s]/g, '');
});
function filterInput(input) {
    const regex = /[^a-zA-Z0-9_]/g;
    input.value = input.value.replace(regex, '');
}