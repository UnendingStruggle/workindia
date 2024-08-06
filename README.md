Flask API for Shorts Management
Overview
This Flask application provides an API for managing "shorts" data. It includes functionalities for user signup, login, creating shorts, retrieving shorts, and filtering shorts. The API endpoints are protected with API keys and require authorization tokens for access.

Setup
Prerequisites
Python: Ensure Python 3.12+ is installed.
Dependencies: Install the required Python packages listed in requirements.txt.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Database Setup:

Ensure you have a database set up and configured correctly. The database schema should include tables for Users and Shorts.

Configuration:

Update constants.py with your own PASSWORD_SALT and FLASK_SECRET_KEY.
Ensure the SECRET_KEY used for encryption is set in app.config.
API Endpoints
1. User Signup
Endpoint: /api/signup
Method: POST
Description: Register a new user.
Request Body:

json
Copy code
{
  "username": "new_user",
  "password": "password",
  "email": "user@example.com"
}
Response:

json
Copy code
{
  "status": "Account successfully created",
  "status_code": 200,
  "user_id": 1
}
2. User Login
Endpoint: /api/login
Method: POST
Description: Authenticate a user and return an access token.
Request Body:

json
Copy code
{
  "username": "existing_user",
  "password": "password"
}
Response:

json
Copy code
{
  "status": "Login Successful",
  "status_code": 200,
  "user_id": 1,
  "access_token": "your_generated_api_key"
}
3. Create Short
Endpoint: /api/shorts/create
Method: POST
Description: Create a new short entry.
Request Body:

json
Copy code
{
  "category": "news",
  "title": "Breaking News",
  "author": "Author Name",
  "publish_date": "2023-01-01T16:00:00Z",
  "content": "Content of the short.",
  "actual_content_link": "http://example.com",
  "image": "",
  "votes": {
    "upvote": 0,
    "downvote": 0
  }
}
Response:

json
Copy code
{
  "status": "Short added Successfully",
  "short_id": 1,
  "status_code": 200
}
4. Get Shorts Feed
Endpoint: /api/shorts/feed
Method: GET
Description: Retrieve all shorts, sorted by publish date and upvotes.
Response:

json
Copy code
[
  {
    "short_id": 1,
    "category": "news",
    "title": "Breaking News",
    "author": "Author Name",
    "publish_date": "2023-01-01T16:00:00Z",
    "content": "Content of the short.",
    "actual_content_link": "http://example.com",
    "image": "",
    "votes": {
      "upvote": 0,
      "downvote": 0
    }
  }
]
5. Filter Shorts
Endpoint: /api/shorts/filter
Method: GET
Description: Retrieve shorts based on filtering and search criteria.
Parameters:

filter (JSON encoded): { "category": "news", "publish_date": "2023-01-01T16:00:00Z", "upvote": 10 }
search (JSON encoded): { "title": "abc", "keyword": "def", "author": "Pranav" }
Response:

json
Copy code
[
  {
    "short_id": 1,
    "category": "news",
    "title": "Breaking News",
    "author": "Author Name",
    "publish_date": "2023-01-01T16:00:00Z",
    "content": "Content of the short.",
    "actual_content_link": "http://example.com",
    "image": "",
    "votes": {
      "upvote": 10,
      "downvote": 0
    }
  }
]
Error Response:

json
Copy code
{
  "status": "No short matches your search criteria",
  "status_code": 400
}
Security
API Key Protection: Admin API endpoints are protected with an API key. Ensure the correct API key is used in the Authorization header for requests.
Authorization Token: Required for filtering capabilities. Send the token received from the login endpoint in the Authorization header.
Running the Application
To run the Flask application:

bash
Copy code
python app.py
The application will be available at http://127.0.0.1:5000.
