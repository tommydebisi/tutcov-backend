# TUTCOV Chat API

## Application Overview

The TUTCOV Chat API serves as the backend for the chatting system of TUTCOV application. It allows authenticated users to communicate with other users in the same department or same courses enrolled. Key features include group messaging view. 


## Usage Instructions

### Authentication

To access the endpoints of the API, you need to authenticate. Use the Token-based authentication method by making a POST request to `/personal-info/` with your username and password.


### Faculty-Chat-Room:

>  ### `/room/<slug: department>/`:
> 
>> ###### _View for faculty group messaging._
>    
>> **REQUEST METHOD:** GET, POST- An authenticated user can access this endpoint for group messaging.
>
>> **ARGS:**
        request (Request, `<slug: department>`): The HTTP request object.
        format (str, optional): The format of the response.
>    
>> **RETURNS**: Response: HTTP response with status and data.

_
## Getting Started

To get started with the project, refer to the [Installation Instructions](#installation-instructions) and [Usage Instructions](#usage-instructions) sections. Familiarize yourself with the API endpoints by exploring the [API Documentation](#api-documentation) provided.

## Configuration

Configuration details can be found in the project's `settings.py` file. Make sure to configure the required environment variables or configuration files as needed. Additionally, if any API keys or secrets are required, they should be mentioned in this section.

## Contributing Guidelines

We welcome contributions from the community. Please follow our [Contributing Guidelines](#contributing-guidelines) for information on how to contribute to the project. You can submit bug reports, feature requests, or pull requests following the outlined process.

## Coding Standards

The project follows specific coding standards outlined in our [Coding Style Guide](#coding-standards). We use linting and code formatting tools to maintain code quality.


## API Documentation (if applicable)  **_Not yet implemented!!_**

You can access the API documentation [here](#api-documentation) when the server is running. It provides comprehensive information on how to use the API endpoints.

## License Information

This project is open-source and is licensed under the [MIT License](LICENSE). For the full license text, please [click here](LICENSE).
