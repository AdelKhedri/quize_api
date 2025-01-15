# Quiz API
## 1. Run With Django
```bash
cs quiz_api
python manage.py runserver
```
started on http://127.0.0.1:8000

## Run documentation:

```bash
mkdocs serve -a 127.0.0.1:8001
```

mkdocs started on `http://127.0.0.1:8001`

## URLS:
### Auth
- Signup: `http://127.0.0.1:8000/auth/registration/`
- Login: with Token: `http://127.0.0.1:8000/auth/login/token-authenticate/`
- Logout: with Token: `http://127.0.0.1:8000/auth/logout/token-authenticate/`
- Login: JWT: `http://127.0.0.1:8000/auth/login/jwt/token/`
- Get refresh token: `http://127.0.0.1:8000/auth/login/jwt/token/refresh/`
- Check access token: `http://127.0.0.1:8000/auth/login/jwt/token/check`

### Questions
- Create question: `http://127.0.0.1:8000/quiz/test/question/list-create/`
- List your question: `http://127.0.0.1:8000/quiz/test/question/list-create/`
- Update question: `http://127.0.0.1:8000/quiz/test/question/QUESTION_ID/`
- Retrive question: `http://127.0.0.1:8000/quiz/test/question/QUESTION_ID/`

### Category
- See all Categorys: `http://127.0.0.1:8000/quiz/categorys`