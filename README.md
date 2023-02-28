
Production URL: https://safe-plains-62725.herokuapp.com/ 


| HTTP Verbs | Endpoints                       | Action                                 |
| ---------- | ------------------------------- | -------------------------------------- |
| GET        | /lists/                         | Lists all lists made.                  |
| GET        | /lists/me/                      | Gets all lists made from LI user.      |
| POST       | /lists/me/                      | Creates a new list for LI user.        |
| GET        | /lists/<int:pk>                 | Gets details for a specific list.      |
| PATCH      | /lists/<int:pk>                 | Updates details for a specific list.   |
| DELETE     | /lists/<int:pk>                 | Deletes a specific list.               |
| POST       | /auth/token/login               | To login to an existing account        |
| GET        | /auth/token/logout              | Logout from account                    |
| POST       | /auth/users/                    | Register new user                      |
| GET        | /items/                         | Gets a list of all items for LI user.  |
| POST       | /items/                         | Create an item for a specific list.    |
| GET        | /items/<int:pk>                 | Gets a specific item's details.        |
| PATCH      | /items/<int:pk>                 | Update a specific item's details.      |
| DELETE     | /items/<int:pk>                 | Deletes a specific item.               |
