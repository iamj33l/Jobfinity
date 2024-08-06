document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('sign-up-form');
    const sign_up_button = document.getElementById('sign-up');

    sign_up_button.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);

        fetch('/signUp/', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if ('error' in data) {
                alert(data.error);
            } else if ('success' in data) {
                alert(data.success);
                // redirect the user to the sign in page after successful login
                window.location.href = '/signIn/';

            }
        })
        .catch(error => {
            console.log(error);
            alert('An error occurred during signing up');
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('sign-in-form');
    const sign_in_button = document.getElementById('sign-in');

    sign_in_button.addEventListener('click', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);

        try {
            const response = await fetch('/login/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            if ('error' in data) {
                alert(data.error);
            } else if ('success' in data) {
                alert(data.success);

                // redirect the user to the home page after successful login
                window.location.href = '/';

            }
        } catch (error) {
            console.log(error);
            alert('An error occurred during signing in');
        }
    });
});

