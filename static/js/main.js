const swiper = new Swiper(".swiper", {
    speed: 500,
    allowTouchMove: false,
});

const gotoSlide = (index) => {

    const input = document.getElementById("category");
    console.log(input)
    const heading = document.getElementById("putCategory");
    heading.textContent = "Enter "+ input.value.split(" ").shift() + " name you want.";
    console.log(heading.textContent)
    swiper.slideTo(index);
};

const restart = () => {
    const inputs = document.querySelectorAll("input");
    const buttons = document.querySelectorAll("button[type=button]");

    buttons.forEach((button) => {
        button.disabled = true;
    });

    inputs.forEach((input) => {
        input.value = "";
    });

    gotoSlide(0);
};

const checkValid = (event) => {
    event.target.nextElementSibling.disabled = !event.target.value.length;
};

// get elements
const ddMenu = document.querySelector('.dd-menu');
const ddButton = document.querySelector('.dd-button');
const hiddenInput = document.querySelector('#category');

// add event listener to dropdown menu
ddMenu.addEventListener('click', function(event) {
  // get the selected item
  const selectedItem = event.target;

  // set the value of the hidden input field
  hiddenInput.value = selectedItem.textContent;

  // update the text of the dd-button div
  ddButton.textContent = selectedItem.textContent;
});