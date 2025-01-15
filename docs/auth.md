# Auth

## Signup
- **URL:** `http://127.0.0.1:8000/auth/registration/`
- **method:** `POST`
- **Permissions:**
- **code lists:**
    - `201`, `400`

| paramName  |   type   | required | unique  | read_only | write_only |         info         |
| :--------: | :------: | :------: | :-----: | :-------: | :--------: | :------------------: |
|  username  |  Sting   | **Yes**  | **Yes** |    No     |     No     |                      |
| password1  |  Sting   | **Yes**  |   No    |    No     |  **Yes**   |                      |
| password2  |  Sting   | **Yes**  |   No    |    No     |  **Yes**   | Password1 repetition |
| first_name |  Sting   |    No    |   No    |    No     |     No     |                      |
| last_name  |  Sting   |    No    |   No    |    No     |     No     |                      |
|   email    |  Sting   |    No    |   No    |    No     |     No     |                      |
| last_login | DateTime |    No    |   No    |  **Yes**  |     No     |                      |
|     id     |  Number  |    No    | **Yes** |  **Yes**  |     No     |                      |

Exampe return successful with code **`201`**:
```js
{
    "id": 9,
    "last_login": null,
    "username": "rer",
    "first_name": "",
    "last_name": "",
    "email": "",
    "date_joined": "2025-01-13T13:28:58.580949Z"
}
```

Exampe return failed with code **`400`**:
```js
{
    "username": [
        "This field is required."
    ]
}
```




## Login: with Token
- **URL:** `http://127.0.0.1:8000/auth/login/token-authenticate/`
- **method:** `POST`
- **Permissions:** 
- **code lists:**
    - `200`, `400`


| paramName | type  | required | unique  | read_only | write_only | info  |
| :-------: | :---: | :------: | :-----: | :-------: | :--------: | :---: |
| username  | Sting | **Yes**  | **Yes** |    No     |  **Yes**   |       |
| password  | Sting | **Yes**  |   No    |    No     |  **Yes**   |       |

Example success result With `200`:
```js
{
    "token": "9e5349c9a3ef9e6b9fccc316565591a6eecef0e4"
}
```

Example faild result With `400`:
```js
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```


## Logout: with Token
This will delete the current token address of the user who is making the request with it.

- **URL:** `http://127.0.0.1:8000/auth/logout/token-authenticate/`
- **method:** `DELETE`
- **Permissions:** Authenticate

Example success result success with code 204

No Content

## Login: JWT

- **URL:** `http://127.0.0.1:8000/auth/login/jwt/token/`
- **method:** `POST`
- **Permissions:** 


| paramName | type  | required | unique  | read_only | write_only | info  |
| :-------: | :---: | :------: | :-----: | :-------: | :--------: | :---: |
| username  | Sting | **Yes**  | **Yes** |    No     |  **Yes**   |       |
| password  | Sting | **Yes**  |   No    |    No     |  **Yes**   |       |

Example success result success with code `200`
```js
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjk0OTMxNCwiaWF0IjoxNzM2Nzc2NTE0LCJqdGkiOiJkM2I0MzM2OTAyMDk0YzYzOTdjNzA3NDI4NDQwNDhhNSIsInVzZXJfaWQiOjl9.vGX8OGuqXWrO-DXA74HuIjRCO_ap4lNdYhwYDO0TS2w",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2Nzc2NzU0LCJpYXQiOjE3MzY3NzY1MTQsImp0aSI6ImQ1ZDk1NDQyYjQ4YjQ1ZTdiMjVhOWZmNzlhOGFlNTYxIiwidXNlcl9pZCI6OX0.r6J4tfs-wWU5zvGzBVrKZtWaJTAlKek4oKNf2Rbn2g4"
}
```

- **Note:** use access to authorization on urls
- **Note:** the life time of access is 4 Minutes
- **Note:** the life time of refresh is 2 Days


Example failed result failed with code `400`:
```js
{
    "username": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ]
}
```
or with code `401`:
```js
{
    "detail": "No active account found with the given credentials"
}
```


## Get refresh token
- **URL:** `http://127.0.0.1:8000/auth/login/jwt/token/refresh/`
- **method:** `POST`
- **Permissions:**

| paramName | type  | required | unique  | read_only | write_only | info  |
| :-------: | :---: | :------: | :-----: | :-------: | :--------: | :---: |
|  refresh  | Sting | **Yes**  | **Yes** |    No     |  **Yes**   |       |

**refresh:** get this token on each request to [login with jwt](#login-jwt)

Example success result success with code `200`:
```js
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2Nzc4NTE3LCJpYXQiOjE3MzY3Nzc3MDAsImp0aSI6IjFmNzg5MzYwYzM4OTQzOWFhY2Y3ODEyZWY5ZmQxNzI2IiwidXNlcl9pZCI6OX0.2OIh15hhivTJaXoxsF1OmKAuCSemaCkiGcpv8WDB5_s"
}
```
Example failed result success with code `401`:

```js
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

## Check access token

- **URL:** `http://127.0.0.1:8000/auth/login/jwt/token/check`
- **method:**
- **Permissions**


| paramName | type  | required | unique  | read_only | write_only | info  |
| :-------: | :---: | :------: | :-----: | :-------: | :--------: | :---: |
|   token   | Sting | **Yes**  | **Yes** |    No     |  **Yes**   |       |


- **Note:** The token is mean access. get it on each reaquest to [login with jwt](#login-jwt)

Example success result success with code `200`
```js
{}
```

Example failed result failed with code `401`

```js
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

End of page