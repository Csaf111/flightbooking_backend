import os
import sys
from pathlib import Path

import mongomock
import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault('FLIGHT_BOOKING_SECRET_KEY', 'test-secret-for-local-regression-tests-12345')

import globalaccess  # noqa: E402
from app import app  # noqa: E402
from blueprints.auth import auth  # noqa: E402
from blueprints.flights import flights  # noqa: E402
from blueprints.users import users  # noqa: E402
import decorators  # noqa: E402


@pytest.fixture(autouse=True)
def database(monkeypatch):
    client = mongomock.MongoClient()
    monkeypatch.setattr(globalaccess, 'db', client.flight_booking)
    monkeypatch.setattr(auth, 'blacklist', client.flight_booking.blacklist)
    monkeypatch.setattr(auth, 'users', client.flight_booking.users)
    monkeypatch.setattr(decorators, 'blacklist', client.flight_booking.blacklist)
    monkeypatch.setattr(flights, 'flights', client.flight_booking.flights)
    monkeypatch.setattr(flights, 'bookings', client.flight_booking.bookings)
    monkeypatch.setattr(users, 'globalaccess', globalaccess)
    yield client.flight_booking


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client
