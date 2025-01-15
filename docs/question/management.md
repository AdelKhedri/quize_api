# Question Management
this urls for creator of question

## Create question
- **URL:** `http://127.0.0.1:8000/quiz/test/question/list-create/`
- **Method:** `POST`
- **Permissions:** Authenticate
- **code lists:**
    - `201`, `400`, `401`

### *parameters*
|   paramName    |   type   | required | unique  | read_only | write_only | info  |
| :------------: | :------: | :------: | :-----: | :-------: | :--------: | :---: |
| text_question  |  Sting   | **Yes**  |   No    |    No     |            |       |
| image_question | file/img |    No    |   No    |    No     |            |       |
|    choise1     |  Sting   | **Yes**  |   No    |    No     |            |       |
|    choise2     |  Sting   | **Yes**  |   No    |    No     |            |       |
|    choise3     |  Sting   | **Yes**  |   No    |    No     |            |       |
|    choise4     |  Sting   | **Yes**  |   No    |    No     |            |       |
| correct_choise |  Number  | **Yes**  |   No    |    No     |            |       |
|     point      |  Float   | **Yes**  |   No    |    No     |            |       |
|       id       |  Number  |    No    | **Yes** |  **Yes**  |            |       |


### *Examples*
Example result with code `201`:
```js
{
    "id": 3,
    "text_question": "fqwfqwfqw",
    "image_question": null,
    "choise1": "fqwdqw",
    "choise2": "dwqqw",
    "choise3": "dqdqqwdqwas",
    "choise4": "wqdqwdqwdqw",
    "correct_choise": 3,
    "point": "1.00"
}
```

Example result with code `400`
```js
{
    "text_question": [
        "This field is required."
    ],
    "choise1": [
        "This field is required."
    ],
    "correct_choise": [
        "\"34\" is not a valid choice."
    ],
    "point": [
        "A valid number is required."
    ]
}
```

___
## List your question

- **URL:** `http://127.0.0.1:8000/quiz/test/question/list-create/`
- **Method:** `GET`
- **Permission:** Authenticate
- **Notes:**
    - **Note:** You will only receive questions that you have created
    - **Note:** Each page contains 50 items (questions).
    - **Note:** to change the page `?page=2` add to url. 2 is page number.

### *recived data:*

| paramName |   type   |           info           |
| :-------: | :------: | :----------------------: |
|   count   |  Number  |  count of all questions  |
|   next    | URL/null |      next page url       |
| previous  | URL/null |    previous page url     |
|  results  |   arry   | all objects in this page |

### *Examples*
Example success result with code `200`:
```js
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "text_question": "rgerg",
            "image_question": null,
            "choise1": "e4f",
            "choise2": "fq",
            "choise3": "d",
            "choise4": "f",
            "correct_choise": 2,
            "point": "2.00"
        }
    ]
}
```

___

## Update question

- **URL:** `http://127.0.0.1:8000/quiz/test/question/QUESTION_ID/`
- **Method:** `PUT`
- **Permissions:** Authenticat, Creator of question
- **code lists:**
    - `200`, `400`, `403`, `401`
- **Note:** 
    - the **`QUESTUIN_ID`** in url is id of question. after create a question id with other info returned.

parameters exactly like [create question](#create-question)

___

## Retrive question

- **URL:** `http://127.0.0.1:8000/quiz/test/question/QUESTION_ID/`
- **Method:** `PUT`
- **Permissions:** Authenticat, Creator of question
- **code lists:**
    - `200`, `403`, `401`
- **Note:** 
    - the **`QUESTUIN_ID`** in url is id of question. after create a question id with other info returned.

### *Parameters*
parameters like [create question](#create-question)

### *Examples*
Example success result with code 200:
```js
{
    "id": 3,
    "text_question": "fqwfqwfqw",
    "image_question": null,
    "choise1": "fqwdqw",
    "choise2": "dwqqw",
    "choise3": "dqdqqwdqwas",
    "choise4": "wqdqwdqwdqw",
    "correct_choise": 3,
    "point": "1.00"
}
```

Example failed result with code 403:
```js
{
    "detail": "only the creator of the TestQuestion can edit it"
}
```

Example failed result with code 401:
```js
{
    "detail": "Authentication credentials were not provided."
}
```

___
