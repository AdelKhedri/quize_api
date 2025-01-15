# Category

## See all Categorys

-   **URL:** `http://127.0.0.1:8000/quiz/categorys`
-   **Method:** `GET`
-   **Permissions:** Authenticate
- **code lists:**
    - `200`, `401`
- **Note:**
    2. Can use any categorys that `allow_quiz_assignment` is true


### Examples

Example success result with code `200`:

```js
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "gggggg",
            "slug": "gggggg",
            "allow_quiz_assignment": true,
            "parent": null
        },
        {
            "id": 1,
            "name": "esf",
            "slug": "hdrgr",
            "allow_quiz_assignment": true,
            "parent": null
        }
    ]
}
```

