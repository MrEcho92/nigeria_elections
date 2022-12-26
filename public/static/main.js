document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.collapsible.expandable');
    var instances = M.Collapsible.init(elems);
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, options);
});
