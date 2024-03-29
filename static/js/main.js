const swiper = new Swiper(".swiper", {
    speed: 500,
    allowTouchMove: false,
});

const gotoSlide = (index) => {

    const input = document.getElementById("category");
    const heading = document.getElementById("putCategory");
    heading.textContent = "Enter "+ input.value.split(" ").shift() + " name you want.";
    console.log(heading.textContent)
    swiper.slideTo(index);
};

const checkValid = (event) => {
    event.target.nextElementSibling.disabled = !event.target.value.length;
};

// get elements
const ddMenu = document.querySelector('.dd-menu');
const ddButton = document.querySelector('.dd-button');
const hiddenInput = document.querySelector('#category');
const submit = document.querySelector('#submit');

// add event listener to dropdown menu
ddMenu.addEventListener('click', function(event) {
  // get the selected item
  const selectedItem = event.target;

  // set the value of the hidden input field
  hiddenInput.value = selectedItem.textContent;

  // update the text of the dd-button div
  ddButton.textContent = selectedItem.textContent;
});

submit.addEventListener('click',function(event){
  submit.innerHTML = "<i class=\"fa fa-circle-o-notch fa-spin\"></i> Loading";
})
