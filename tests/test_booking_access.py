import jwt

import globalaccess


def auth_header(username, admin=False):
    token = jwt.encode({'user': username, 'admin': admin, 'jti': f'{username}-token'}, globalaccess.SECRET_KEY, algorithm='HS256')
    return {'x-access-token': token}


def test_customer_can_only_read_own_booking(client, database):
    database.bookings.insert_many([
        {'_id': 'alice-booking', 'user_id': 'alice', 'flight_number': 'AB123'},
        {'_id': 'bob-booking', 'user_id': 'bob', 'flight_number': 'CD456'},
    ])

    response = client.get('/bookings', headers=auth_header('alice'))

    assert response.status_code == 200
    assert response.get_json() == [{'_id': 'alice-booking', 'user_id': 'alice', 'flight_number': 'AB123'}]


def test_customer_cannot_delete_someone_elses_booking(client, database):
    database.bookings.insert_one({'_id': 'bob-booking', 'user_id': 'bob', 'flight_number': 'CD456'})

    response = client.delete('/bookings/bob-booking', headers=auth_header('alice'))

    assert response.status_code == 404
    assert database.bookings.find_one({'_id': 'bob-booking'}) is not None


def test_admin_can_read_all_bookings(client, database):
    database.bookings.insert_many([
        {'_id': 'alice-booking', 'user_id': 'alice'},
        {'_id': 'bob-booking', 'user_id': 'bob'},
    ])

    response = client.get('/bookings', headers=auth_header('admin', admin=True))

    assert response.status_code == 200
    assert {booking['_id'] for booking in response.get_json()} == {'alice-booking', 'bob-booking'}
