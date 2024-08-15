# Jobfinity App

Jobfinity is a web application that allows candidates to apply for jobs and companies to manage job postings and applications.

## Features

- **Candidate Dashboard**: View and manage job applications.
- **Company Dashboard**: View and manage job postings.
- **Profile Management**: Edit candidate and company profiles.
- **Job Application**: Apply for jobs and withdraw applications.
- **Authentication**: Sign in and sign out functionality.

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Postgres SQL 

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/iamj33l/jobfinity_app.git
    cd jobfinity_app
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```sh
   python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

- **Access the application**: Open your web browser and go to `http://127.0.0.1:8000/`.
- **Sign in**: Use the sign-in page to log in to your account.
- **Navigate**: Use the navigation bar to access different sections like candidate dashboard, company dashboard, etc.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**: `git checkout -b feature-name`.
3. **Commit your changes**: `git commit -m 'Add some feature'`.
4. **Push to the branch**: `git push origin feature-name`.
5. **Create a pull request**.

###### Made with ❤️ by [Jeel Patel](https://github.com/iamj33l)
