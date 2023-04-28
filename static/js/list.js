const modalBtns = document.querySelectorAll('.modal-btn');
const similarViewBtns = document.querySelectorAll('.similar');
const downloadBtns = document.querySelectorAll('.download');
const modals = document.querySelectorAll('#my-modal');

modalBtns.forEach(function(modalBtn) {
  modalBtn.addEventListener('click', function(event) {
    event.preventDefault();
    let id = modalBtn.getAttribute('name');
    id = ".b"+id;
    let movie_modal = document.querySelector(id);
    movie_modal.style.display = 'block';
  });
});

similarViewBtns.forEach(function(btn) {
  btn.addEventListener('click', function(event) {
    event.preventDefault();
    let title = btn.getAttribute('name');
    btn.innerHTML = "<i class=\"fa-solid fa-circle-notch fa-spin\"></i> Loading";
    window.location.href = "/movie?category=Similar+Movies&category_value=" + title;
  });
});

downloadBtns.forEach(function(btn) {
  btn.addEventListener('click', function(event) {
    event.preventDefault();
    let link = btn.getAttribute('name');
    let url = "https://www.google.com/search?q="+link+"%20%2B(mkv%7Cmp4%7Cavi%7Cmov%7Cmpg%7Cwmv%7Cdivx%7Cmpeg)%20-inurl%3A(jsp%7Cpl%7Cphp%7Chtml%7Caspx%7Chtm%7Ccf%7Cshtml)%20intitle%3Aindex.of%20-inurl%3A(listen77%7Cmp3raid%7Cmp3toss%7Cmp3drug%7Cindex_of%7Cindex-of%7Cwallywashis%7Cdownloadmana)"
    window.open(url, "_blank");
  });
});

window.addEventListener('click', outsideClick);

function outsideClick(e) {
  modals.forEach(function(modal){
    if (e.target == modal) {
      modal.style.display = 'none';
    }
  });
}
