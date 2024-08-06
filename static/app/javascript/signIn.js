const signInButton = document.querySelector('#sign-in-button')
const signUpButton = document.querySelector('#sign-up-button')
const signInButton2 = document.querySelector('#sign-in-button2')
const signUpButton2 = document.querySelector('#sign-up-button2')
const main = document.querySelector('.sign-in-main')

signUpButton.addEventListener("click", () => {
    main.classList.add('sign-up-mode');
});

signInButton.addEventListener("click", () => {
    main.classList.remove('sign-up-mode');
});

signUpButton2.addEventListener("click", () => {
    main.classList.add('sign-up-mode2');
});

signInButton2.addEventListener("click", () => {
    main.classList.remove('sign-up-mode2');
});