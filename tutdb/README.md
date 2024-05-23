# TUTCOV Courses API

## Application Overview

The TUTCOV Courses API serves as the backend for the dashboard, courses, questions and students enrollment view of TUTCOV application. It allows authenticated users to communicate with other users in the same department or same courses enrolled. Key features include group messaging view. 


## Usage Instructions for Endpoints

To access the endpoints of these API, you need to authenticate. Use the Token-based authentication method by making a POST request to `/personal-info/` with your username and password.

### 1. Dashboard View

>  ### `/dashboard/`:
> 
>> ###### _View for the home page of the application. Only authenticated users can access this view._
>    
>> **REQUEST METHOD:** GET
>
>> **ARGS:** request (Request): The HTTP request object. Format (None)
>    
>> **RETURNS**: Response: HTTP response with status and data.


### 2. Courses-APIView:

>  ### `/dashboard/courses/`:
> 
>> ###### _This view displays the following:_
>> - _saved courses,_
>> - _faculty courses,_
>> - _departmental courses,_
>> - _all new courses._
>> 
>> NB: Only **authenticated users** can access this view.
>    
>> **REQUEST METHOD:** GET
>
>> **ARGS:**
        request (Request, <slug: department>): The HTTP request object.
        format (str, optional): The format of the response.
>    
>> **RETURNS**: Response: HTTP response with status and data.


### 3. Course-Questions:

>  ### `/questions/all/<str: session>/<str: course_slug>/`:
> 
>> ###### _This view displays the questions for the selected course._
>>
>> NB: **All users** can access this view.
>    
>> **REQUEST METHOD:** GET
>
>> **ARGS:** request, <str: course_slug>, <str: session>, format=None
>    
>> **RETURNS**: Response: HTTP response with status and data.


### 4. Question-Detail-APIView:

>  ### `/questions/<uuid: uuid>/`:
> 
>> ###### _Displays all questions available in the system._
>>
>> NB: **All users** can access this view.
>    
>> **REQUEST METHOD:** GET, PUT 
>
>> **ARGS:** request, <uuid: uuid>, format=None
>    
>> **RETURNS**: Response: HTTP response with status and data.


 ### 5. List-Student-Enrollment:

>  ### `/my-courses/`:
> 
>> ###### _Displays the number of enrolled courses by the user._
>>
>> NB: Only **authenticated users** can access this data.
>    
>> **REQUEST METHOD:** GET
>
>> **ARGS:** request, format=None
>    
>> **RETURNS**: Response: HTTP response with status and data.


 ### 6. Enroll-Student-APIView:

>  ### `/enroll/<str: course_slug>/`:
> 
>> ###### _This endpoint attempts to enroll a student to a course. If the user is already enrolled an error is displayed:_ 
>> `{"error": "You are already enrolled in this course"}`
>>
>> NB: Only **authenticated users** can access this data.
>    
>> **REQUEST METHOD:** POST
>
>> **ARGS:** request, course_slug, format=None
>    
>> **RETURNS**: Response: HTTP response with status and data.


### 7. Question-Response-Create-APIView:

>  ### `/questions/<str: session>/<str: course_slug>/`:
> 
>> ###### _This endpoint contains the logic for displaying the questions for a course quiz._ 
>
>> NB: Only **authenticated users** can access this data.
>    
>> **REQUEST METHOD:** GET
>
>> **ARGS:** request, session, course_slug, format=None
>    
>> **RETURNS**: Response: HTTP response with status and data.


 ### 8. Update-Question-Response-APIView:

>  ### `/questions/<str: session>/<str: course_slug>/change/`:
> 
>> ###### _This endpoint contains the logic for saving the responses made by the user to the quiz questions._
>    
>> **REQUEST METHOD:** PUT
>
>> **ARGS:** request, session, course_slug, format=None
>    
>> **RETURNS**: Response: HTTP response with status and data.
 
 
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
