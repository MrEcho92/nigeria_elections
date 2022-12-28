document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.collapsible.expandable');
    var instances = M.Collapsible.init(elems);
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, options);
});

// Code to set progress bar for result in /vote/success
const dataList = document.querySelectorAll(".bar");
const colors = ['#68A672', '#E75353', '#4663C7', '#D3C753']

for (let i = 0; i < dataList.length; i++) {
    const val = dataList[i].firstElementChild.innerHTML;
    dataList[i].style.width = val;
    var item = colors[Math.floor(Math.random() * colors.length)];
    dataList[i].style.background = item;
}
