# Flight Booking Backend

A Flask REST API for a flight-booking workflow: authentication, flight discovery, bookings, and flight reviews. It is designed as the backend counterpart to the Angular flight-booking client in this account.

## What it demonstrates

- Flask blueprints for feature-oriented routing
- JWT-protected endpoints and token-blacklist support
- MongoDB-backed application data
- JSON API contracts with a Postman collection for manual exploration
- Separation of authentication, flights, users, and review concerns

## Architecture

```text
HTTP client
   │
Flask application (app.py)
   ├── auth blueprint
   ├── flights blueprint
   ├── users blueprint
   └── flight reviews blueprint
   │
MongoDB
```

The application factory/configuration is currently concentrated in `app.py`; feature routes live in `blueprints/`.

## Run locally

1. Create and activate a virtual environment.
2. Install the dependencies required by the imports in the project (Flask, Flask-CORS, Flask-PyMongo, PyJWT, and password-hashing support).
3. Create a local `.env` file—never commit it—with a strong `SECRET_KEY` and a MongoDB connection string.
4. Start the service:

```bash
python app.py
```

The existing app configuration listens on port 5001. Import `Flight_dataset.postman_collection.json` into Postman to explore the API manually.

## Configuration

Keep secrets outside version control. At minimum, configure:

```dotenv
SECRET_KEY=<long-random-secret>
MONGO_URI=mongodb://localhost:27017/flightbooking
```

Use unique values per environment and rotate a secret immediately if it is ever committed or shared.

## API surface

The repository currently exposes routes for registration/login, flight management, booking management, and flight reviews. Protected routes require an `Authorization: Bearer <token>` header. The Postman collection is the current request-level reference; formal OpenAPI documentation is a planned improvement.

## Validation and testing

The repository includes a CI smoke check that compiles the Python sources. It does **not** claim full automated coverage. The next engineering step is to introduce a Flask test application, disposable MongoDB fixture, and endpoint-level tests for authorization and validation paths.

## Engineering decisions and limitations

- MongoDB was selected for flexible document-oriented booking data.
- The checked-in JSON files are development/sample data, not a production persistence strategy.
- Python bytecode directories are currently present in history; the included ignore rules prevent new cache files from being added. Removing historic artifacts should be handled in a separate, carefully reviewed cleanup.
- Production deployment should use a WSGI server, environment-based configuration, request validation, rate limiting, and a managed database.

## Related project

- [Angular frontend](https://github.com/Csaf111/flightbooking_frontend)

## License

No license has been selected yet. Do not assume permission to reuse this code beyond GitHub's default terms.
