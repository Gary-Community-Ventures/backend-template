# Backend Template

This repo is a template for a Flask backend with Supabase as the database.
It also uses Clerk for authentication and Sentry for error tracking.

## Setup

1. Copy `.env.example` to `.env` and populate the required values:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon/public key
   - `CLERK_SECRET_KEY` - Your Clerk secret key
   - `SENTRY_DSN` - Your Sentry DSN (optional)

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   make install
   ```

3. Run the development server:
   ```bash
   make run
   ```

## Examples

Examples of routes can be found under the `app/routes` path. In `app/routes/main.py` you will find
standard non-authenticated routes that can be used for testing. In `app/routes/auth.py` you will find examples
of authenticated routes with used the auth decorators. It is easiest to test these if you have a working
Clerk frontend.

## Supabase Usage

The Supabase client is initialized in `app/__init__.py` and accessible via `current_app.supabase_client`.

### Defining Tables

Define your tables in `app/supabase/tables.py`:

```python
from app.supabase.columns import Column, datetime_column
from app.supabase.tables import Table

class User(Table):
    TABLE_NAME = "user"

    CLERK_ID = Column("clerk_id")
    EMAIL = Column("email")
    NAME = Column("name")
    CREATED_AT = Column("created_at", datetime_column)
```

### Querying Data

```python
from flask import current_app
from app.supabase import cols, unwrap_or_abort
from app.supabase.tables import User

# Select all users
result = User.query().select("*").execute()
users = unwrap_or_abort(result)

# Select specific columns
result = User.query().select(cols(User.EMAIL, User.NAME)).execute()

# Select by ID
result = User.select_by_id(cols(User.EMAIL, User.NAME), user_id).execute()
user = unwrap_or_abort(result)

# Filter and query
result = User.query().select("*").eq(User.EMAIL, "test@example.com").execute()
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make run` | Run development server |
| `make prod` | Run with Gunicorn |
| `make format` | Format code with Black |
| `make lint` | Lint code with Flake8 |
| `make test` | Run tests |
| `make test-cov` | Run tests with coverage |
| `make clean` | Remove cached files |
