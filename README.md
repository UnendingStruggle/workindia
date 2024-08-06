# Flask Shorts API

## Overview

This project is a Flask-based API for managing and interacting with "shorts". It includes endpoints for user registration, login, creating shorts, viewing a feed of shorts, and filtering/searching shorts.

## Features

- User registration and login
- Create, read, and manage shorts
- Filter and search shorts by various criteria
- Admin protection with API key authentication

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add your secret key and any other environment variables:

    ```
    FLASK_SECRET_KEY=your_flask_secret_key
    ```

5. **Run the application:**

    ```bash
    python app.py
    ```

## API Endpoints

### User Registration

- **Endpoint:** `/api/signup`
- **Method:** `POST`
- **Description:** Register a new user.

  **Request Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com"
  }
