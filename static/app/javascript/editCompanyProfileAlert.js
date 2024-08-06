document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('edit-company-profile-form');
    const edit_company_profile_button = document.getElementById('edit-company-profile-form-button');

    edit_company_profile_button.addEventListener('click', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);

        let temp_url = window.location.href;
        let url = temp_url.replace('editCompanyProfile', 'editCompanyProfileAttempt');
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
                window.location.href = '/companyProfile/';

            }
        } catch (error) {
            console.log(error);
            alert('An error occurred during signing in');
            window.location.href = '/companyProfile/';
        }
    });
});
