const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('.navbar > li > a');

navLinks.forEach((link) => {
    if (link.getAttribute('href') === activePage) {
        link.classList.add('active');
    }
});