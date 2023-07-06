# FSND-capstone-project
Udacity Fullstack Developer Nanodegree Capstone Project combining all of the concepts and the skills taught in the courses to build an API from start to finish and host it

## Project assignment - Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.
* Models includes:
    * Movies with attributes title and release date
    * Actors with attributes name, age and gender
* Endpoints includes:
    * GET /actors and /movies
    * DELETE /actors/ and /movies/
    * POST /actors and /movies and
    * PATCH /actors/ and /movies/
* Roles includes:
    * Casting Assistant:
        * Can view actors and movies
    * Casting Director:
        * All permissions a Casting Assistant has and
        * Add or delete an actor from the database
        * Modify actors or movies
    * Executive Producer:
        * All permissions a Casting Director has and
        * Add or delete a movie from the database
* Tests includes:
    * One test for success behavior of each endpoint
    * One test for error behavior of each endpoint
    * At least two tests of RBAC for each role

## Local Development Setup

### Setup virtual environment

To create a virtual environment if using VSCode, open the project directory and press CTRL + SHIFT + P, then select create environment -> venv.

Use pip to install the required dependencies.
```
pip install -r requirements.txt
```

Once you’ve created the virtual environment, activate it.
```
. venv/bin/activate
```

### Setup enviroment variables
Setup enviroments variable by running:

```
./setup.ps1
```

### Run the server
Start the server using the FLASK development server:
```
./run.ps1
```

NOTE: Those files are made for Windows PowerShell.

### Open browser
Navigate to project homepage [http://localhost:5000](http://localhost:5000) 

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL
**_https://capstone-project-eu1y.onrender.com_**

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (get:actors): Can see all actors
  - GET /movies (get:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (patch:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (patch:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

The token for each role for testing are the following:

```
{"casting_assistant":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3R051UnphMFdOMk9BY2ZCdXhVZyJ9.eyJpc3MiOiJodHRwczovL2FydGh1ci1kZXYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YTcwYjVkYzhlN2Y0MjNjYjUyNWNiNCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjg4NjY5MzU0LCJleHAiOjE2ODg2NzY1NTQsImF6cCI6Im0xUlAxbk44bVJsVUJSRzVVdEw5a3dWbUVVMVlrRVRzIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.XrRFsFEqD1enqc0HxsAx0UwztnchLTeRg6bTBrDSqBnLPMlQtVFiLO8EZplPE5-LZBJRWSHWDvUvL02oEx1XJ9vSsDbh3tHeHth4aJCSA5ciOzmlsrzHVGyIwsG39cpDOFh6eDgO2XdP5kV3-s1Kx08vBQA_g8VqBDzevmWWCN0AeyF7USTLA08oGWZFM_jF_9j4nRrzLgEY0551OtZRV1DNPjw5pP43uj2qhksTgOssokQApRa_NaUYixD9xHc7sFl07CpYk385KSz6zg4vOe_ZPbEM1xlYdM3AjYGiXP4_pRTFJMivc0ruDEZmAbw_bZCtNvgcAT3INrOu1gicNw"}
```

```
{"casting_director":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3R051UnphMFdOMk9BY2ZCdXhVZyJ9.eyJpc3MiOiJodHRwczovL2FydGh1ci1kZXYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0OTJmODkwOGI4NWM4YTY5NDlmZjIwZSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjg4NjY5NDkxLCJleHAiOjE2ODg2NzY2OTEsImF6cCI6Im0xUlAxbk44bVJsVUJSRzVVdEw5a3dWbUVVMVlrRVRzIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.HhvDVgffjcz613ui2AOXjM1MaHhZvXw5zA9gn6lNuSNpet3qJ8sAUuzsDgeXg3EYCekofP6kPo2-mUHUT8kMKeADUD5bP4EujH8rM-OE_8j_qcUPP0YyL4Lq8y3srbf7FqXZQKhw1M_b5DW9XliCxtxnOPC_DcIMnBwJf-m9xY0DR4-Ht9sNiS-B_oFYBQJbxNfQrfKpCCBREd6Mttx3i2f0z68fW5uI8dvgpLcML0FE9fKj6GK9nAJyV10DErS6b8qyq-DBmxnbZwAKscNfqkoiv2qJUzz5YHAZ789kIbDq8w0kuyrqX63xMgjdPPg_vzf0l1zaQ8rVzgKO9sO66Q"}
```

```
{"executive_director":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3R051UnphMFdOMk9BY2ZCdXhVZyJ9.eyJpc3MiOiJodHRwczovL2FydGh1ci1kZXYudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTExMTMwNTYwMDg5MjkxMTk1NDQzIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2ODg2Njk1MjQsImV4cCI6MTY4ODY3NjcyNCwiYXpwIjoibTFSUDFuTjhtUmxVQlJHNVV0TDlrd1ZtRVUxWWtFVHMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.OH9hqGQ-oYskgKBhiAw756njN8sZ9mfYv2oID59EFPUUdoxN4uewD3g3ZdRLWKoLUlFjv5iR3Zw_HTUo1TZofZA1m54MT6yev-iE8p3Hk8MeAWlcwlu6XgtzBwHdme0fH-jk1kaxAYg3ovsTbNIPsAC1cIC1zZplKrMA7LVCDbgyw50apC6qba3OzwNPI0jeyPjn3y_fa9wYdqUTQD3mOG8mkhqBJ2XwWyeQP_4JG6kveKnYUN3QCrftU4Oz2lL3MG_IjteN4PTGvGO9v7aEUTskqzXmPmt9kmhOqKgBP_ZY06mJg3oxZZHgEddznePryWA6BeQuQO6SApnVsR8xkQ"}
```

### How to work with each endpoint

Along the project you can find the file to run all the tests on postman locally (capstone.postman_collection).

# <a name="get-actors"></a>
### 1. GET /actors

Query paginated actors.

```bash
$ curl -X GET https://capstone-project-eu1y.onrender.com/actors?page1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 actors per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `get:actors`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`

#### Example response
```js
{
  "actors": [
    {
      "age": 25,
      "gender": "Male",
      "id": 1,
      "name": "Arthur"
    }
  ],
  "success": true
}
```
#### Errors
If you try fetch a page which does not have any actors, you will encounter an error which looks like this:

```bash
$ curl -X GET https://capstone-project-eu1y.onrender.com/actors?page23567
```

will return

```js
{
  "error": 404,
  "message": "no actors found in database.",
  "success": false
}
```

# <a name="post-actors"></a>
### 2. POST /actors

Insert new actor into database.

```bash
$ curl -X POST https://capstone-project-eu1y.onrender.com/actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
       4. **integer** `movie_id`
- Requires permission: `post:actors`
- Returns: 
  1. **integer** `id from newly created actor`
  2. **boolean** `success`

#### Example response
```js
{
    "created": 5,
    "success": true
}

```
#### Errors
If you try to create a new actor without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://capstone-project-eu1y.onrender.com/actors?page52346
```

will return

```js
{
  "error": 422,
  "message": "no name provided.",
  "success": false
}
```

# <a name="patch-actors"></a>
### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH https://capstone-project-eu1y.onrender.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `patch:actors`
- Returns: 
  1. **integer** `id from updated actor`
  2. **boolean** `success`
  3. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`

#### Example response
```js
{
    "actor": [
        {
            "age": 30,
            "gender": "Other",
            "id": 1,
            "name": "Test Actor"
        }
    ],
    "success": true,
    "updated": 1
}
```
#### Errors
If you try to update an actor with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://capstone-project-eu1y.onrender.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "Actor with id 125 not found in database.",
  "success": false
}
```
Additionally, trying to update an Actor with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "provided field values are already set. No update needed.",
  "success": false
}
```

# <a name="delete-actors"></a>
### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE https://capstone-project-eu1y.onrender.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`
- Returns: 
  1. **integer** `id from deleted actor`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete actor with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://capstone-project-eu1y.onrender.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "Actor with id 125 not found in database.",
  "success": false
}
```

# <a name="get-movies"></a>
### 5. GET /movies

Query paginated movies.

```bash
$ curl -X GET https://capstone-project-eu1y.onrender.com/movies?page1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 movies per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `get:movies`
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `name`
      - **date** `release_date`
  2. **boolean** `success`

#### Example response
```js
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 09 Dec 2020 00:00:00 GMT",
      "title": "Arthur first Movie"
    }
  ],
  "success": true
}

```
#### Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl -X GET https://capstone-project-eu1y.onrender.com/movies?page31241
```

will return

```js
{
  "error": 404,
  "message": "no movies found in database.",
  "success": false
}
```

# <a name="post-movies"></a>
### 6. POST /movies

Insert new Movie into database.

```bash
$ curl -X POST https://capstone-project-eu1y.onrender.com/movies
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `post:movies`
- Returns: 
  1. **integer** `id from newly created movie`
  2. **boolean** `success`

#### Example response
```js
{
    "created": 5,
    "success": true
}
```
#### Errors
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://capstone-project-eu1y.onrender.com/movies?page1555433
```

will return

```js
{
  "error": 422,
  "message": "no name provided.",
  "success": false
}
```

# <a name="patch-movies"></a>
### 7. PATCH /movies

Edit an existing Movie

```bash
$ curl -X PATCH https://capstone-project-eu1y.onrender.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `edit:movies`
- Returns: 
  1. **integer** `id from updated movie`
  2. **boolean** `success`
  3. List of dict of movies with following fields:
        - **integer** `id`
        - **string** `title` 
        - **date** `release_date` 

#### Example response
```js
{
    "created": 1,
    "movie": [
        {
            "id": 1,
            "release_date": "Tue, 19 Ago 2020 00:00:00 GMT",
            "title": "Sunshine"
        }
    ],
    "success": true
}

```
#### Errors
If you try to update an movie with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://capstone-project-eu1y.onrender.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "Movie not found in database.",
  "success": false
}
```
Additionally, trying to update an Movie with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "provided field values are already set. No update needed.",
  "success": false
}
```

# <a name="delete-movies"></a>
### 8. DELETE /movies

Delete an existing movie

```bash
$ curl -X DELETE https://capstone-project-eu1y.onrender.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movies`
- Returns: 
  1. **integer** `id from deleted movie`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete movie with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://capstone-project-eu1y.onrender.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "Movie with id 125 not found in database.",
  "success": false
}
```


## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

