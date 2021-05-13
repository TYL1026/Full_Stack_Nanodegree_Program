# Trivia_API
## Error handling
1. Error massage is returned as JSON object format
```
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```
2. The API will return **2 errors**
* 404: Bad Request
* 422: Not Processable
## End Point
### GET /catigory
* General:
  * Return all catigories for questions
* sample: ```curl http://127.0.0.1:5000/categories```
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET /questions
* General:
  * Return all questions, all catigories and total questions
  * The questions are paginated to 10/page  
* sample: ```curl http://127.0.0.1:5000/questions?page=1```
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
      "question": "Which is the only team to play in every soccer World Cup tournament?"
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
  "total_questions": 39
}
```
### DELETE /questions
* General:
  * Delete given question it
* sample: ```curl http://127.0.0.1:5000/questions/1```
```
   {
     'success':True,
     'delete':1
   }
```

### POST /questions
* General:
  * Post new questions with given question, answer, catigory and difficalty
* sample: ```curl -d '{"question": "123","answer": "456","category":"Geography","difficulty":1' -H 'Content-Type: application/json}' -X POST http://127.0.0.1:5000/questions```
```
{
  "created": 40
  "success": true
}
```
### POST /questions/search
* General:
  * Search questions based on given string
*sample: ```curl -d '{"searchTerm": "123"' -H 'Content-Type: application/json}' -X POST http://127.0.0.1:5000/questions/search```
```
{
  "created": 40
  "success": true
}
```
### GET /categories/<int:id>/questions
* General:
  * Get questions by categories
*sample: ```curl http://127.0.0.1:5000/categories/1/questions```
```
 {
  "currentCategory": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}
```
### POST /quizzes
* General:
  * Start quiz with given categories
*sample: ```curl -X POST "http://127.0.0.1:5000/quizzes" -d "{\"previous_questions\": [2],\"quiz_category\": {\"type\":\"Geography\",\"id\": \"2\"}}" -H "Content-Type: application/json"```
```
{
  "previousQuestions": [
    2,
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 17,
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}
```
