# FastAPI Authentication System – Report

## 1. Overview

This project implements an authentication system using **FastAPI** with both **SQL (PostgreSQL)** and **NoSQL (MongoDB)** backends.  
The system supports **user registration, login, token-based authentication, and session management**.

---

## 2. Project Structure

- Module4_Project/
- ├── app/
- │   ├── main.py
- |   ├──routes
- |   |   ├── routes_sql.py
- |   |   ├── routes_nosql.py
- |   ├──model
- |   |   ├──models.py
- |   ├──schema
- |   |   ├──schemas.py
- |   ├──sql
- |   |   ├──db_sql.py
- |   |   ├──crud_sql.py
- |   ├──nosql
- |   |   ├──db_nosql.py
- |   |   ├──crud_nosql.py
- ├── redis-server.exe
- ├── requirements.txt

---

## 3. Implementation Choices

- **FastAPI Framework**: Chosen for its modern async capabilities and built-in OpenAPI documentation.
- **Pydantic Models**: Used for input validation and data serialization, ensuring type safety.
- **SQL (PostgreSQL)**: Managed via SQLAlchemy ORM to handle relational data.
- **NoSQL (MongoDB)**: Used to demonstrate flexibility with document-based storage.
- **Password Hashing**:  
  - Switched from **bcrypt** to **argon2** for better security and to avoid manual password truncation.
  - Argon2 provides memory-hard resistance against GPU attacks.
- **JWT Authentication**:  
  - JSON Web Tokens (JWT) implemented with `python-jose` for stateless authentication.  
  - Tokens expire after 30 minutes for security.
- **Session Management (SQL)**:  
  - Implemented Redis for temporary session storage, using UUID tokens with 1-hour expiry.
- **Dependency Injection**:  
  - Used `Depends()` for injecting authentication logic (`routes`), improving modularity and testability.
- **Swagger UI (Docs)**:  
  - Built-in documentation at `/documentation` provides testing endpoints for login and registration.  

---

## 4. Challenges Encountered

- **JWT Validation in Swagger**:  
  Swagger’s “Authorize” button does not validate tokens automatically.  
  This was resolved by adding a `/token/check` endpoint for manual validation.
  
- **Password Length Issue with bcrypt**:  
  Initially bcrypt required manual truncation to 72 characters.  
  Solved by switching to **Argon2**, removing the need for truncation.
  
- **Cross-Database Logic**:  
  Managing both SQL and NoSQL logic required modular structure (`crud_sql` and `crud_nosql`).
  
- **Redis Integration**:  
  Ensured Redis sessions expire automatically to avoid memory leaks.

---

## 5. Key Features

- ✅ Dual-database authentication (SQL + NoSQL)
- 🔐 Secure password hashing with Argon2
- 🧩 JWT-based access tokens
- ⏱️ Token expiry handling
- 📚 Auto-generated API docs with Swagger
- 🔁 Redis-backed session system for SQL side
- ⚙️ Dependency injection for reusable authentication logic

---




## 6. Conclusion

The project demonstrates a complete authentication flow across both relational and non-relational databases, emphasizing **security, modular design, and maintainability**.  
It leverages FastAPI’s core features to build a scalable, production-ready authentication system.
