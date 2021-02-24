def test_root(app):
    """Ping the root endpoint."""
    response = app.get('/')

    assert response.ok
    assert response.data == 'Server is running...'
