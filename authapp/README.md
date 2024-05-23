# TUTCOV Authentication and Authorization  API

## Application Overview

The TUTCOV Application API serves as the backend for the authentication of TUTCOV application. It allows users to register, login and logout. Key features include user authentication, user registration, user login, user logout and user profile view. 

## Installation Instructions

### Pre-requisites

Before setting up the project locally, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/downloads/) (>=3.10)
- [Django](https://www.djangoproject.com/download/)
- [Django Rest Framework](https://www.django-rest-framework.org/#installation)
- A Database System (e.g., PostgreSQL, MySQL, SQLite) - [Django Database Installation](https://www.djangoproject.com/download/#database-installation)

- Also install packages from the requirements.txt file.

### Installation Steps

1. Clone the repository:

        git clone https://github.com/prosper-20/tutcov-backend.git


2. Change into the parent directory:

        cd tutcov-backend


3. Change into the application directory:

        cd authapp


4. Set up a virtual environment:

        py -m venv env


5. Activate your virtual environment (for windows):

        venv\Scripts\activate


6. Install the Python dependencies:

        pip install -r requirements.txt


7. Configure the database settings in the `settings.py` file according to your chosen database system.


8. Apply migrations to create the database schema:

        python manage.py migrate


9. Create a superuser for administrative access:

        python manage.py createsuperuser


10. Start the development server:
 ```
 python manage.py runserver
 ```

The API should now be running locally at [http://localhost:8000/](http://localhost:8000/).

## Usage Instructions

### Authentication

To access most endpoints of the API, you need to authenticate. Use the Token-based authentication method by making a POST request to `/personal-info/` with your username and password.

<!-- #### User Authentication:

- /api/token/: Obtain an authentication token. -->

### Personal-Info-Registration-View:

>  ### `/personal-info/`:
> 
>> ###### _View for handling user registration and email confirmation._
>    
>> **REQUEST METHOD:** GET, POST- Registers a user, generates and sends an OTP token via email with django's send_mail function.
>
>> **ARGS:**
        request (Request): The HTTP request object.
        format (str, optional): The format of the response.
>    
>> **RETURNS**: Response: HTTP response with status and data.

### School-Info-Registration-View:
> ### `/school-info/`:
>> ###### _View for handling school information registration with the student._
>
>> **REQUEST METHOD:** POST- Registers a user with school information after OTP validation.
>
>> **ARGS:** request (Request): The HTTP request object.
    format (str, optional): The format of the response.
>
>> **RETURNS:** Response: HTTP response with status and data.

### User-Login-View:
> ### `/login/`: 
>
>> ###### _View for logging in only registered users._
>    
>> **REQUEST METHOD**: GET, POST- Logs in a user with information provided after validation and create access and refresh tokens.
>    
>> **ARGS:** request (Request): The HTTP request object.
>  Format (str, optional): The format of the response.
>    
>> **RETURNS:** Response: HTTP response with status and data.


#### User-Logout-View:
>### `/logout/`:
>> ###### _View to log out the current user. This endpoint retrieves the access token from the Authorization header. Checks if the access token is associated with the current user and proceed to log out the user._
>> _If the access token is invalid or not associated, respond with an error:
    {'error': 'Invalid access token or user not authenticated'}_

#### User Profile View:
> ### `/me/`:
> ###### _Only authenticated users can access this page. The user gets to view and edit their information on the application._
> 
_
## Getting Started

To get started with the project, refer to the [Installation Instructions](#installation-instructions) and [Usage Instructions](#usage-instructions) sections. Familiarize yourself with the API endpoints by exploring the [API Documentation](#api-documentation) provided.

## Configuration

Configuration details can be found in the project's `settings.py` file. Make sure to configure the required environment variables or configuration files as needed. Additionally, if any API keys or secrets are required, they should be mentioned in this section.

## Contributing Guidelines

We welcome contributions from the community. Please follow our [Contributing Guidelines](#contributing-guidelines) for information on how to contribute to the project. You can submit bug reports, feature requests, or pull requests following the outlined process.

## Coding Standards

The project follows specific coding standards outlined in our [Coding Style Guide](#coding-standards). We use linting and code formatting tools to maintain code quality.

## Testing and Quality Assurance

To ensure code quality, follow the instructions in the [Testing Guidelines](#testing-and-quality-assurance) for running tests and quality checks on the codebase. The project uses a testing framework, and details on the testing tools are provided.

## Deployment Instructions (if applicable)

For deployment to a production environment, please refer to our [Deployment Instructions](#deployment-instructions-if-applicable). This document includes step-by-step instructions and configuration details for deploying the project.

## API Documentation (if applicable)

You can access the API documentation [here](#api-documentation) when the server is running. It provides comprehensive information on how to use the API endpoints.

## License Information

This project is open-source and is licensed under the [MIT License](LICENSE). For the full license text, please [click here](LICENSE).
