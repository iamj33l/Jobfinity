// navigation bar

let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');
let menuIcon = document.querySelector('#menu-icon img');
let isMenuOpen = false;

menu.onclick = () => {
    if (isMenuOpen) {
        menuIcon.src = 'static/app/images/menu.png';
    } 
      
    else {
        menuIcon.src = 'static/app/images/close.png';
    }
    isMenuOpen = !isMenuOpen;
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open');
}

// job card slider
const slider = document.querySelector(".card-slider");
const carousel = document.querySelector(".carousel");
const arrowButtons = document.querySelectorAll(".arrow");
const firstCardWidth = carousel.querySelector(".card").offsetWidth;
const carouselChildren = [...carousel.children];

let timeoutId;

let cardPerView = Math.round(carousel.offsetWidth / firstCardWidth);

carouselChildren.slice(-cardPerView).reverse().forEach (card => {
    carousel.insertAdjacentHTML("afterbegin", card.outerHTML);
});

carouselChildren.slice(0, cardPerView).forEach (card => {
    carousel.insertAdjacentHTML("beforeend", card.outerHTML);
});

arrowButtons.forEach(button => {
    button.addEventListener("click", () => {
        carousel.scrollLeft += button.id === "left" ? -firstCardWidth : firstCardWidth;
    });
});

const autoSlide = () => {
    if (window.innerWidth < 768) {
        return;
    }
    timeoutId = setTimeout(() => carousel.scrollLeft += firstCardWidth, 2500);
}
autoSlide();

const infiniteScroll = () => {
    if (carousel.scrollLeft === 0) {
        carousel.classList.add("no-transition");
        carousel.scrollLeft = carousel.scrollWidth - (2 * carousel.offsetWidth);
        carousel.classList.remove("no-transition");
    }
    else if (Math.ceil(carousel.scrollLeft) === carousel.scrollWidth - carousel.offsetWidth) {
        carousel.classList.add("no-transition");
        carousel.scrollLeft = carousel.offsetWidth;
        carousel.classList.remove("no-transition");
    }

    clearTimeout(timeoutId);
    if(!slider.matches(":hover")) {
        autoSlide();
    }
}

carousel.addEventListener("scroll", infiniteScroll);
slider.addEventListener("mouseenter", () => clearTimeout(timeoutId));
slider.addEventListener("mouseleave", autoSlide);