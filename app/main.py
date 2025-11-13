from fastapi import FastAPI
from app.routes.routes_sql import router as sql_router
from app.routes.routes_nosql import router as nosql_router
from app.sql.db_sql import Base, engine

# for creating sql tables
Base.metadata.create_all(bind=engine)

description = """
This project demonstrates a **full-stack authentication system** with both SQL and NoSQL backends.

### Features:

1. **SQL-Based API**:
   - Implements **session-based authentication**.
   - Sessions can be managed in-memory or with **Redis** for improved scalability. Server must be running on localhost:6379
   - Endpoints for **user registration**, **login**, and **protected resource access**.

2. **NoSQL-Based API**:
   - Implements **JWT (JSON Web Token) authentication**.
   - Users receive a JWT upon login which must be sent in the `Authorization: Bearer <token>` header to access protected endpoints.
   - Endpoints for **user registration**, **login**, and **retrieving user info** in Mongodb with default endpoint localhost:27017 .

3. **Security Enhancements**:
   - Passwords are securely hashed using **Argon2**.
   - Session tokens are securely generated and expire automatically.
   - JWTs are signed with **HS256** and include expiration for safety.

4. **Documentation**:
   - Interactive Swagger UI available at `/docs`.
   - ReDoc documentation available at `/redoc`.

### Usage:

- SQL API endpoints can optionally leverage Redis for session management.
- NoSQL API endpoints use JWT for stateless authentication.
- The project is designed for modularity, testability, and security best practices.
"""

app = FastAPI(
    title="JWT and Session",
    version="1.0",
    description=description,
    docs_url="/documentation",
    redoc_url=None
)

app.include_router(sql_router)
app.include_router(nosql_router)
