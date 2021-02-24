def test_root(client):
    """Ping the root endpoint."""
    response = client.get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Server is running...'
