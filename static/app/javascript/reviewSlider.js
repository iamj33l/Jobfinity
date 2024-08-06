// review card reviewSlider

const reviewSlider = document.querySelector(".review-slider");
const reviewCarousel = document.querySelector(".review-carousel");
const reviewFirstCardWidth = reviewCarousel.querySelector(".review-card").offsetWidth;
const reviewCarouselChildren = [...reviewCarousel.children];

let reviewIsDragging = false, reviewStartX, reviewStartScrollLeft, reviewTimeoutId;

let reviewCardPerView = Math.round(reviewCarousel.offsetWidth / reviewFirstCardWidth);

reviewCarouselChildren.slice(-reviewCardPerView).reverse().forEach (card => {
    reviewCarousel.insertAdjacentHTML("afterbegin", card.outerHTML);
});

reviewCarouselChildren.slice(0, reviewCardPerView).forEach (card => {
    reviewCarousel.insertAdjacentHTML("beforeend", card.outerHTML);
});

const reviewAutoSlide = () => {
    reviewTimeoutId = setTimeout(() => reviewCarousel.scrollLeft += reviewFirstCardWidth, 2500);
}
reviewAutoSlide();

const reviewInfiniteScroll = () => {
    if (reviewCarousel.scrollLeft === 0) {
        reviewCarousel.classList.add("no-transition");
        reviewCarousel.scrollLeft = reviewCarousel.scrollWidth - (reviewCarousel.offsetWidth);
        reviewCarousel.classList.remove("no-transition");
    }
    else if (Math.ceil(reviewCarousel.scrollLeft) === reviewCarousel.scrollWidth - reviewCarousel.offsetWidth) {
        reviewCarousel.classList.add("no-transition");
        reviewCarousel.scrollLeft = reviewCarousel.offsetWidth;
        reviewCarousel.classList.remove("no-transition");
    }

    clearTimeout(reviewTimeoutId);
    if(!reviewSlider.matches(":hover")) {
        reviewAutoSlide();
    }
}

reviewCarousel.addEventListener("scroll", reviewInfiniteScroll);
reviewSlider.addEventListener("mouseenter", () => clearTimeout(reviewTimeoutId));
reviewSlider.addEventListener("mouseleave", reviewAutoSlide);