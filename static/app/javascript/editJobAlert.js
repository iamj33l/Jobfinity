document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('update-job-form');
    const update_job_button = document.getElementById('update-job-submit');

    update_job_button.addEventListener('click', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);

        let temp_url = window.location.href;
        let url = temp_url.replace('http://127.0.0.1:8000/updateJob', '/updateJobAttempt');
        console.log(url);

        try {
            const response = await fetch(url, {
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
            window.location.href = '/companyDashboard/';
        }
    });
});
