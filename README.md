# TUTCOV Application API

## Project Overview

The TUTCOV Application API serves as the backend of TUTCOV application. It allows users to register, login, enroll for courses, attempt quiz. Key features include user authentication and authorization, user registration, user login, user profile view, course enrollment, quiz questions for courses, group messaging feature among others. 

## Installation Instructions

### Prerequisites

Before setting up the project locally, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/downloads/) (>=3.11.4)
- [Django](https://www.djangoproject.com/download/)
- [Django Rest Framework](https://www.django-rest-framework.org/#installation)
- A Database System (e.g., PostgreSQL, MySQL, SQLite) - [Django Database Installation](https://www.djangoproject.com/download/#database-installation)

### Installation Steps

1. Clone the repository:

        git clone https://github.com/prosper-20/tutcov-backend.git


2. Change into the parent directory:

        cd tutcov-backend


3. Set up a virtual environment:

        python3 -m venv venv


4. Activate your virtual environment:

        venv\Scripts\activate


5. Install the Python dependencies:

        pip install -r requirements.txt


6. Configure the database settings in the `settings.py` file according to your chosen database system.


7. Apply migrations to create the database schema:

        python manage.py migrate


8. Create a superuser for administrative access:

        python manage.py createsuperuser


9. Start the development server:
 python manage.py runserver

The API should now be running locally at [http://localhost:8000/](http://localhost:8000/).


## Usage Instructions
>
> ### Authentication
>
>> To access most endpoints of the API, you need to authenticate the user. Use the Token-based authentication.
>
>> This section of the app contains the logic for user authentication and authorization.
>> To view more details under this application check here > [auth_app](https://github.com/prosper-20/tutcov-backend/tree/corrections/authapp). 


> ### Chat Feature:
>
>> The endpoint here contains the logic for the group messaging feature. A user enrolled to the same course can interact with other users enrolled to the same course. More details here > [chat_app](https://github.com/prosper-20/tutcov-backend/tree/corrections/chat)


> ### Questions, course enrollment, Quiz Feature:
>
>> The endpoints here contains the logic for students course enrollemnt, quiz questions and answers among others. A user enrolled to a course can attempt questions available to the course. More details here > [tutorial_app](https://github.com/prosper-20/tutcov-backend/tree/corrections/tutdb)


> ### Swagger Doc Feature:
>
>> The endpoint here implements swagger's feature to test each endpoint in the application with proper documentation. It is useful as its tests each request method with their required parameters. You prefix `/swagger` after the localhost url.


## Getting Started

To get started with the project, refer to the [Installation Instructions](#installation-instructions) and [Usage Instructions](#usage-instructions) sections. Familiarize yourself with the API endpoints by exploring the [API Documentation](#api-documentation) provided.

## Configuration

Configuration details can be found in the project's `settings.py` file. Make sure to configure the required environment variables or configuration files as needed. Additionally, if any API keys or secrets are required, they should be mentioned in this section.

## Contribution

We welcome contributions from the community. Please follow our [Contribution Guidelines](#contribution-guidelines) for information on how to contribute to the project. You can submit bug reports, feature requests, or pull requests following the outlined process. We recommend creating an issue or replying in a comment to let us know what you are working on first that way we don't overwrite each other.

#### Contribution Guidelines
1. Clone the repo git clone https://github.com/prosper-20/tutcov-backend.git
2. Open your terminal & set the origin branch: `git remote add origin https://github.com/prosper-20/tutcov-backend.git`
3. Pull origin git pull origin corrections
4. Create a new branch for the task you were assigned to, eg TicketNumber/(Feat/Bug/Fix/Chore)/Ticket-title : `git checkout -b ZA-001/Feat/Sign-Up-from`
5. After making changes, do `git add .` 
6. Commit your changes with a descriptive commit message : `git commit -m "your commit message"`.
7. To make sure there are no conflicts, run `git pull origin corrections`.
8. Push changes to your new branch, run `git push -u origin feat-csv-parser`.
9. Create a pull request to the corrections branch not main.
10. Ensure to **describe your pull request**.
11. If you've added code that should be tested, add some test examples.


## Coding Standards

The project follows specific coding standards outlined in our [Coding Style Guide](#coding-standards). We use linting and code formatting tools to maintain code quality.


## Merging
#### Under any circumstances should you merge a pull request on a specific branch to the dev or main branch

### _Commit CheatSheet_
|   Type   |         Meaning          | Description                                                                                                 |
|:--------:|:------------------------:|:------------------------------------------------------------------------------------------------------------|
|   feat   |         Features         | A new feature                                                                                               |
|   fix    |       Bug Fixes          | 	A bug fix                                                                                                  |
|   docs   |      Documentation       | 	Documentation only changes                                                                                 |
|  style   |          Styles          | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)     |
| refactor |     Code Refactoring     | 	A code change that neither fixes a bug nor adds a feature                                                  |
|   perf   | Performance Improvements | 	A code change that improves performance                                                                    |
|   test   |          Tests           | Adding missing tests or correcting existing tests                                                           |
|  build   |          Builds          | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
|    ci    | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
|  chore   |          Chores          | Other changes that don't modify, backend or test files                                                      |
|  revert  |         Reverts          | Reverts a previous commit                                                                                   |

> **Sample Commit Messages**

* `chore: Updated README file`:= `chore` is used because the commit didn't make any changes to the frontend or test folders in any way.

* `feat: Added plugin info endpoints`:= `feat` is used here because the feature was non-existent before the commit.
<!-- ## Testing and Quality Assurance

To ensure code quality, follow the instructions in the [Testing Guidelines](#testing-and-quality-assurance) for running tests and quality checks on the codebase. The project uses a testing framework, and details on the testing tools are provided. -->


## API Documentation (if applicable)

You can access the API documentation [here](#api-documentation) when the server is running. It provides comprehensive information on how to use the API endpoints.

## License Information

This project is open-source and is licensed under the [MIT License](LICENSE). For the full license text, please [click here](LICENSE).

[//]: # (## Contributors)

[//]: # ()
[//]: # (We acknowledge and appreciate the contributions of the following individuals to this project:)

[//]: # ()
[//]: # (- [name]&#40;mailto:name@gmail.com&#41; - GitHub Profile: [here]&#40;https://github.com/name&#41;)

## Project Roadmap (Optional)

Our project roadmap outlines future plans and enhancements for the project. It serves as a guide for potential contributors and collaborators. You can find the roadmap in the [ROADMAP.md](ROADMAP.md) file.

&copy; 2023 TUTCOV Application Backend.