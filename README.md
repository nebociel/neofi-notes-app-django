# NeoFi Python Backend Assignment API Documentation 🚀

Welcome to the NeoFi Python Backend API documentation. This API powers a state-of-the-art note-taking application, offering a robust set of endpoints for user registration, authentication, note management, and version history tracking.

## Table of Contents

- [📝 Introduction](#📝-introduction)
- [🔒 Authentication](#🔒-authentication)
- [📜 Setup Instructions](#📜-setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [🧪 Running Tests](#🧪-running-tests)
- [🛠️ cURL Commands](#🛠️-curl-commands)
- [🚀 Endpoints](#🚀-endpoints)
  - [📝 User Registration](#📝-user-registration)
  - [🚪 User Login](#🚪-user-login)
  - [📝 Note Management](#📝-note-management)
    - [➕ Create New Note](#➕-create-new-note)
    - [📖 Retrieve a Note](#📖-retrieve-a-note)
    - [✏️ Update a Note](#✏️-update-a-note)
    - [🗑️ Delete a Note](#🗑️-delete-a-note)
    - [🤝 Sharing a Note](#🤝-sharing-a-note)
    - [🕰️ Get Note Version History](#🕰️-get-note-version-history)
- [🚀 Conclusion](#🚀-conclusion)
- [📧 Contact Developer](#📧-contact-developer)

## 📝 Introduction

The NeoFi Python Backend API is a powerful tool for building modern note-taking applications. It offers a seamless user experience with secure authentication, efficient note management, and detailed version history tracking.

## 🔒 Authentication

- Authentication is required for certain endpoints.
- Use the provided user credentials for testing or create a new user through the `/signup` endpoint.

## 📜 Setup Instructions

Before diving into the endpoints, let's set up the project.

### Prerequisites

- Python (version 3.7 or higher)
- Django (version 3.2 or higher)
- Postman (optional, for API testing)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory:**

   ```bash
   cd neoFi_project
   ```

3. **Set up a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install project dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Running the Application:**

   To run the application locally, execute the following command:

   ```bash
    python manage.py runserver
   ```

   You can include the information about running tests in the documentation under the "Setup Instructions" section. Here's where you can insert it:

## 🧪 Running Tests

To run the tests for the Django app, follow these steps:

1. **Run the tests using the manage.py command:**

   ```bash
   python manage.py test
   ```

   This command will run all the tests included in your Django project.

2. **Check the test results in the terminal output.**

   By following these steps, you can ensure that all tests for your Django app are executed, helping you maintain code quality and functionality.

## 🛠️ cURL Commands

<details>
  <summary>Click to expand cURL commands</summary>

Here are some cURL commands to interact with the API:

```bash
# User Registration
curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "email": "user@example.com", "password": "password123"}' http://localhost:8000/signup

# User Login
curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "password123"}' http://localhost:8000/login

# Create New Note
curl -X POST -H "Authorization: Bearer <authentication_token>" -H "Content-Type: application/json" -d '{"title": "New Note", "content": "This is a new note."}' http://localhost:8000/notes/create

# Retrieve a Note
curl -X GET -H "Authorization: Bearer <authentication_token>" http://localhost:8000/notes/{id}

# Update a Note
curl -X PUT -H "Authorization: Bearer <authentication_token>" -H "Content-Type: application/json" -d '{"title": "Updated title", "content": "Updated content of the note."}' http://localhost:8000/notes/{id}

# Delete a Note
curl -X DELETE -H "Authorization: Bearer <authentication_token>" http://localhost:8000/notes/{id}

# Sharing a Note
curl -X POST -H "Authorization: Bearer <authentication_token>" -H "Content-Type: application/json" -d '{"note_id": 1, "users": [2, 3]}' http://localhost:8000/notes/share

# Get Note Version History
curl -X GET -H "Authorization: Bearer <authentication_token>" http://localhost:8000/notes/version-history/{id}
```

</details>

## 🚀 Endpoints

### 📝 User Registration

```
POST /signup
```

Allows users to create an account by providing necessary information such as username, email, and password.

<!-- omit from toc -->#### Request Body

```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "password123"
}
```

<!-- omit from toc -->#### Response

- `201 Created`: User registration successful.
- `400 Bad Request`: Validation errors or username/email already taken.

### 🚪 User Login

```
POST /login
```

Allows users to log in to their account using their credentials (username/email and password).

<!-- omit from toc -->#### Request Body

```json
{
  "username": "example_user",
  "password": "password123"
}
```

<!-- omit from toc -->#### Response

- `200 OK`: Login successful, returns authentication token and user details.
- `401 Unauthorized`: Invalid credentials.

### 📝 Note Management

#### ➕ Create New Note

```
POST /notes/create
```

Allows authenticated users to create a new note.

<!-- omit from toc -->#### Request Body

```json
{
  "title": "New Note",
  "content": "This is a new note."
}
```

<!-- omit from toc -->#### Response

- `201 Created`: Note created successfully.
- `400 Bad Request`: Validation errors.

#### 📖 Retrieve a Note

```
GET /notes/{id}
```

Retrieves a note by its ID, accessible only to authenticated users.

<!-- omit from toc -->#### Response

- `200 OK`: Returns the note content.
- `404 Not Found`: Note not found or unauthorized access.

#### ✏️ Update a Note

```
PUT /notes/{id}
```

Allows authorized users to update a note by adding new sentences.

<!-- omit from toc -->#### Request Body

```json
{
  "title": "Updated title",
  "content": "Updated content of the note."
}
```

<!-- omit from toc -->#### Response

- `200 OK`: Note updated successfully.
- `404 Not Found`: Note not found or unauthorized access.

#### 🗑️ Delete a Note

```
DELETE /notes/{id}
```

Allows authorized users to delete a note.

<!-- omit from toc -->#### Response

- `204 No Content`: Note deleted successfully.
- `404 Not Found`: Note not found or unauthorized access.

#### 🤝 Sharing a Note

```
POST /notes/share
```

Shares a note with other users, allowing multiple users to view and edit the note.

<!-- omit from toc -->#### Request Body

```json
{
  "note_id": 1,
  "users": [2, 3] // User IDs to share the note with
}
```

<!-- omit from toc -->#### Response

- `200 OK`: Note shared successfully.
- `404 Not Found`: Note not found.

#### 🕰️ Get Note Version History

```
GET /notes/version-history/{id}
```

Retrieves the version history of a note, including all changes made since its creation.

<!-- omit from toc -->#### Response

- `200 OK`: Returns version history.
- `404 Not Found`: Note not found or unauthorized access.

## 🚀 Conclusion

This API provides essential functionalities for a note-taking application, including user management, note creation, sharing, and version history tracking.

Feel free to explore and test the endpoints using the provided documentation. If you encounter any issues or have any questions, please contact the developer.

---

## 📧 Contact Developer

For further inquiries or assistance, please contact:

**Developer**: Akash Kumar Chaubey

**Email**: akashchaubey443@gmail.com

[Resume](https://drive.google.com/file/d/1Ncd7BjxJrha9csqssebiVqNcCGmpt6JW/view?usp=sharing)

---

🔚
