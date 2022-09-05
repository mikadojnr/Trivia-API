# Project Description

## Title: Full Stack Trivia
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.


### Motivation
As part of the completion of the API lessons under the fullstack course by udacity, that am working on this great project


### Code Style
This project follows the [PEP 8 style guide](https://peps.python.org/pep-0008/) and common practices such as:
- Clear variable and function names
- Logically named enpoints
- Appropriate in-code comments
<hr>

# Getting Started

### Prerequisites and Installation
#### - Backend
Installaion for backend:
1. **Python 3.7+** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

##### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

##### Running the server
From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

#### Frontend
> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). <br>It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.


##### Installing Dependencies
1. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. <br>After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**


##### Running Your Frontend in Dev Mode
The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. <br>You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```
<hr>

# API Reference
### Base URL
The project is locally hosted. When the frontend server is started, it runs the application on the local server:
**127.0.0.1:3000/**

## Errors
Here are lists of expected errors while running the app and the interpretations of their meaning
- **400 -Bad Request:** It indicates that the client sent a request that could not be processed by the server
- **404 - Not Found:** This means the requested resource or URL does not exist as the server can't locate it
- **405 - Method Not Allowed:** This error indicates that the server understand the action by the client but is not allowed to execute on such resource
- **422 - Unprocessable:** It means your request was corectly recieved but the instructions could not be processed
- **500 - Internal Server Error:**  This means that the server encountered something unexpected that prevented it from fulfilling the request.


## Resource Endpoint Library
### All Endpoints
```js
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```


```js
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

```js
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

```js
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions. 
```

```js
POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object 
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```

```js
POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
- Returns: Does not return any new data
```

```js
POST '/questions'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```

### Sample Requests with CURL
- To display all categories:
```bash
curl http://127.0.0.1:5000/categories |jq '.'
```

- Get all questions (paginated to 10 questions per page):
```bash
curl http://127.0.0.1:5000/questions |jq '.'
```

- Delete a question with specified id:
```bash
curl -X DELETE http://127.0.0.1:5000/questions/1 |jq '.'
```

- Add new question to list of questions:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"question":"Which subject studies living and non-living things?", "answer":"Biology", "category":"1", "difficulty":"1"}' http://127.0.0.1:5000/questions  |jq '.'
```

- Search for question with specific term:
```bash
curl -X POST -H"Content-Type: application/json" -d '{"searchTerm":"american"}'  http://127.0.0.1:5000/questions/search |jq '.'
```
<hr>

## Author(s)
**Edidiong David Udoidiok** - _Fullstack Developer_

<hr>

## Acknowledgements 

I acknowledge all the guys at [stack**overflow**](stackoverflow.com) for their timely feedback to help fix bugs while developing the app. <br>Special thanks to my fellow scholars in Udacity who helped out on the slack community to debug and fix bugs

