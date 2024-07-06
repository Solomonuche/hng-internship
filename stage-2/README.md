# BACKEND Stage 2 Task: User Authentication & Organisation
Using your most comfortable backend framework of your choice, adhere to the following acceptance:
## READ CAREFULLY!!!
## Acceptance Criteria
- Connect your application to a Postgres database server. (optional: you can choose to use any ORM of your choice if you want or not).
- Create a User model using the properties below
- NB: user id and email must be unique
{
	"userId": "string" // must be unique
	"firstName": "string", // must not be null
	"lastName": "string" // must not be null
	"email": "string" // must be unique and must not be null
	"password": "string" // must not be null
	"phone": "string"
}
- Provide validation for all fields. When there’s a validation error, return status code 422 with payload:
{
  "errors": [
    {
      "field": "string",
      "message": "string"
    },
  ]
}
- Using the schema above, implement user authentication
- User Registration:
-- Implement an endpoint for user registration
-- Hash the user’s password before storing them in the database.
-- successful response: Return the payload with a 201 success status code.
- User Login
Implement an endpoint for user Login.
Use the JWT token returned to access PROTECTED endpoints.
Organisation
- A user can belong to one or more organisations
- An organisation can contain one or more users.
- On every registration, an organisation must be created.
- The name property of the organisation takes the user’s firstName and appends “Organisation” to it. For example: user’s first name is John , organisation name becomes "John's Organisation" because firstName = "John" .
- Logged in users can access organisations they belong to and organisations they created.
- Create an organisation model with the properties below.
Organisation Model:
{
	"orgId": "string", // Unique
	"name": "string", // Required and cannot be null
	"description": "string",
}