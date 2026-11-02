# Flight Booking Backend

A Flask and MongoDB API for flight search, reservation management, reviews, and role-aware administration. It is designed to support the companion Angular frontend while keeping customer booking data separated by account.

## What it demonstrates

- JWT authentication with short-lived, revocable tokens
- bcrypt password hashing
- Customer-only access to bookings; administrators can view and manage all bookings
- Flight search and status management
- API regression tests using an in-memory MongoDB substitute
- GitHub Actions continuous integration

## Prerequisites

- Python 3.10+
- MongoDB (for local application use)

## Local setup

```bash
git clone https://github.com/Csaf111/flightbooking_backend.git
cd flightbooking_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set the values from `.env.example` in your shell (or your preferred local environment loader). Generate a strong value for `FLIGHT_BOOKING_SECRET_KEY`; never commit it. The application fails fast if the variable is missing, rather than falling back to a source-controlled secret.

```bash
export FLIGHT_BOOKING_SECRET_KEY='replace-with-a-long-random-secret'
export MONGO_URI='mongodb://localhost:27017'
export CORS_ALLOWED_ORIGINS='http://localhost:4200'
python app.py
```

The API listens on `http://127.0.0.1:5001` by default.

## Authentication and access model

Register at `POST /register` or log in at `POST /login`. Send the returned token as an `x-access-token` request header to protected endpoints.

| Resource | Customer | Administrator |
| --- | --- | --- |
| Own booking | Read, update, delete | Read, update, delete |
| Other customer booking | Not accessible | Read, update, delete |
| User directory | Not accessible | Read |
| Flight status | Not accessible | Update |

Tokens include a unique identifier (`jti`). `GET /logout` records that identifier so the token cannot be reused without persisting the bearer token itself.

## Core endpoints

| Method | Endpoint | Authentication | Purpose |
| --- | --- | --- | --- |
| POST | `/register` | No | Create an account |
| POST | `/login` | No | Obtain a JWT |
| GET | `/flights` | No | Search flights |
| GET | `/flights/:flight_number` | No | Retrieve flight details |
| POST | `/bookings` | Yes | Create a booking for the authenticated user |
| GET | `/bookings` | Yes | List the caller's bookings (or all for an admin) |
| GET/PUT/DELETE | `/bookings/:booking_id` | Yes | Manage an accessible booking |
| PUT | `/flights/:flight_number/status` | Admin | Update flight status |

## Quality checks

```bash
pytest
```

The test suite uses `mongomock`; it does not require a running MongoDB instance. Pull requests and pushes to `main` run the same command in GitHub Actions.

## Security notes

- Do not set `FLASK_DEBUG=1` outside local development.
- Restrict `CORS_ALLOWED_ORIGINS` to the deployed frontend origin(s).
- Rotate any secret that was previously committed, even if the file was later removed.
- Production deployments should use a managed MongoDB instance and an environment-specific secret manager.
