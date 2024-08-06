document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('post-job-form');
    const post_job_button = document.getElementById('post-job-submit');

    post_job_button.addEventListener('click', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);

        try {
            const response = await fetch('/postJobAttempt/', {
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
                window.location.href = '/companyDashboard/';

            }
        } catch (error) {
            console.log(error);
            alert('An error occurred during signing in');
            window.location.href = '/postJob/';
        }
    });
});
