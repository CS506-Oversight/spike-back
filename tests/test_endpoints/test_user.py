import json


def test_create_user(client):
    """Test the user creating endpoint."""
    payload = {
        'username': 'customer',
        'password': 'test',
        'phone': '3195406789',
        'address': '123 ave',
        'email': 'customer@gmail.com',
        'type': 'customer'
    }

    response = client.post('/create_user', data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json == {
        'message': 'User added with id: customer.',
        'status': 'Success'
    }


def test_get_user(client):
    """Test the get user endpoint."""
    response = client.get('/get_user/admin')

    assert response.status_code == 200
    assert response.json == {
        'address': '123 ave',
        'email': 'admin@gmail.com',
        'phone': '3195406789',
        'type': 'admin',
        'username': 'admin'
    }


def test_delete_user(client):
    """Test the delete user endpoint."""
    response = client.delete('/delete_user/tmehmen2')

    assert response.status_code == 200
    assert response.json == {
        'message': 'User with username tmehmen2 has been deleted.',
        'status': 'Success'
    }


def test_check_pass(client):
    """Test the user authentication endpoint."""
    payload = {
        'username': 'admin',
        'password': 'test'
    }

    response = client.post('/check_pass', data=json.dumps(payload))

    assert response.status_code == 200
    assert response.json == {
        'address': '123 ave',
        'email': 'admin@gmail.com',
        'phone': '3195406789',
        'type': 'admin',
        'username': 'admin'
    }
