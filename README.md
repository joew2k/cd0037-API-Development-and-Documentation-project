# Trivia Project Documentation

The Trivia application test users knowledge using questions related to various fields, ranging from science to arts. There is also a game section where user can play a quiz of five questions. While user can interact with the front end application, there is also API endpoints available for developers.

The coding style for this project follow PEP8

# Getting Started

## Pre-requisite and Installations
Once you have cloned this repository, I recommend you setup a virtual environment, Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
### Frontend Dependencies
The `--reload` flag will detect file changes and restart the server automatically.

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [np](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

# API REFERENCE

## Getting Started
- Base URL: Currently the application run locally on and its not hosted as base url. The backend is hosted at default http://127.0.0.1:5000/ which is set as a proxy to the frontend.
- Authentication: The API does not require authetication

## Error Handling
The error of this API are turned as json format. See sample below
{   
    'success': False,
    'error': 422,
    'message':'Unprocessable'
}

The API will return 4 error types when request fails
400: Bad request
404: Resource not found
422: Unprocessable
500: Internal Server error

# Endpoints
GET /categories
- General
    - Return all questions categories
- Sample: curl http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
GET /questions
- General 
    - Return all questions and its paginated with 10 questions per page. it also return a success massage, total questions and the categories.
- Sample: curl http://127.0.0.1:5000/questions

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nominati
on, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise i
n the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton
 about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tour
nament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 18
}

Note that the page can also be specified
curl http://127.0.0.1:5000/questions?page=6

DELETE /questions/<int:question_id>
- General
    - This endpoint remove a question with a given quention id 
- Sample curl -X http://127.0.0.1:5000/questions/15
{
  "deleted_id": 15,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nominati
on, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise i
n the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton
 about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tour
nament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of
 optical illusions?"
    }
  ],
  "success": true,
  "total_questions_NOW": 17
}

GET categories/2/questions
- General 
    - The endpoint return questiosn based on category
- Sample: curl http://127.0.0.1:5000/categories/2/questions
{
  "currentCategory": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of
 optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism
, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 4



POST /questions
- General
    - Add new question to when question details are specified, it also return a search term when a search term is specified.
- Adding new question: curl -d '{"question": "Hello John", "answer": "Hi Guys", "category": 1, "difficulty": 4}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/questions

POST /questions/search
- General
    - return a search questions.
- Search a question: curl -d '{"searchTerm": "hello"}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/questions/search

{
  "questions": [
    {
      "answer": "Hi Hi",
      "category": 1,
      "difficulty": 1,
      "id": 52,
      "question": "Hello Hello"
    },
    {
      "answer": "Hi Guys",
      "category": 1,
      "difficulty": 4,
      "id": 68,
      "question": "Hello John"
    }
  ],
  "totalQuestions": 20

POST /quizzes
- General:
  - Play quiz game by providing the quiz category and previous questions. Note that the game will not repeat question.
- Sample curl -d '{"previous_questions":[], "quiz_category": {"id":0}}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/quizzes

{
  "question": {
    "answer": "Hi Guys",
    "category": 4,
    "difficulty": 1,
    "id": 68,
    "question": "Hello John"
  }
}

# Authors
Joseph Ogwuche

# Acknowledgment
The Udacity Team
