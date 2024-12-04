# Homework-10
# Event Manager API

Welcome to the Event Manager API project! This application is a robust and secure REST API designed to manage users and events, featuring JWT-based OAuth2 authentication. 
## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Documentation](#documentation)
- [Collaborative Development](#collaborative-development)
- [Reflection and Learning](#reflection-and-learning)
- [License](#license)


---

## Getting Started

### Setup Instructions

Follow the steps below to set up the project on your local machine:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/event-manager-api.git
   cd event-manager-api
2. **Set up the environment**
   - Copy the `.env.sample` file to `.env`:
     ```bash
     cp .env.sample .env
     ```
   - Update the `.env` file with your database and email service credentials.

3. **Start the application with Docker**
   ```bash
   docker-compose up --build

4. **Access the API documentation**
   - Open [http://localhost/docs](http://localhost/docs) to explore the API endpoints using Swagger UI.
  

## API Endpoints

### Authentication
- **POST** `/auth/login` - User login with email and password.
- **POST** `/auth/register` - Register a new user.
- **POST** `/auth/verify-email` - Verify email with a token.

### User Management
- **GET** `/users/me` - Get current user profile.
- **PUT** `/users/me` - Update current user profile.
- **POST** `/users/reset-password` - Reset user password.

### Admin Operations
- **GET** `/users` - List all users (Admin only).
- **DELETE** `/users/{id}` - Delete a user (Admin only).
## Testing

### Running Tests

This project includes a comprehensive suite of unit and integration tests.

1. **Run the tests using `pytest`:**
   ```bash
   pytest --maxfail=1 --disable-warnings
2. **Check test coverage:**
   ```bash
   pytest --cov=app
3. **Test cases include:**
   - Validation for user schemas.
   - Service-layer logic tests.
   - Edge cases for login, registration, and profile updates.

## Documentation

### Internal Documentation
- Swagger UI is available at [http://localhost/docs](http://localhost/docs).
- Code-level documentation includes:
  - **Models:** Defined in `app/models/user_model.py`.
  - **Schemas:** Located in `app/schemas/user_schemas.py`.
  - **Services:** Business logic in `app/services/user_service.py`.

### External Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io)
## Collaborative Development

### Git Workflow

1. **Branches:**
   - Use feature branches for development (e.g., `feature/username-validation`).
   - Use `main` for stable production-ready code.

2. **Pull Requests:**
   - Submit a pull request for code reviews before merging.

3. **Issue Tracking:**
   - Enable GitHub Issues to log and manage tasks.
   - Create issues for bugs, features, and enhancements.

### Best Practices

- Use meaningful commit messages.
- Run tests before committing.
- Keep branches updated with `main`.
## Technical Skills

This assignment was a deep dive into designing and working with REST APIs using FastAPI. The following skills were strengthened:

1. **Validation and Security:**
   - Implementing robust username and password validation to prevent security vulnerabilities and ensure data integrity.
   - Hashing sensitive data like passwords using industry-standard techniques.

2. **Test-Driven Development:**
   - Writing unit tests, integration tests, and edge-case tests using `pytest`.
   - Leveraging test coverage tools to ensure over 90% coverage, which improved the reliability and maintainability of the code.

3. **Debugging and Problem-Solving:**
   - Debugging critical issues like OAuth token generation and profile updates.
   - Interpreting error messages and using stack traces to identify and resolve root causes efficiently.

---

## Collaborative Processes

1. **Git and GitHub Workflow:**
   - Learned to work with branches, pull requests, and code reviews, following collaborative development best practices.
   - Enabled issue tracking to manage and prioritize tasks systematically.

2. **Documentation:**
   - Improved project documentation, ensuring that it reflects the current state of the software and is accessible to new contributors.
   - Added meaningful commit messages and linked closed issues to improve traceability.

---

## Challenges and Solutions

- **Challenge 1:** Ensuring the compatibility of validation logic across models, schemas, and services.
  - **Solution:** This was resolved by carefully integrating Pydantic validators and SQLAlchemy constraints.
  
- **Challenge 2:** Maintaining a clean Git workflow.
  - **Solution:** By adhering to branch-based development and resolving merge conflicts early, this was addressed.

---

## Insights Gained

The assignment reinforced the importance of:

- Thorough testing to prevent regressions and ensure code quality.
- Collaboration tools like GitHub for effective teamwork.
- Clear documentation for seamless onboarding and knowledge sharing.

This experience has significantly enhanced my ability to design, develop, and collaborate on real-world software projects.

