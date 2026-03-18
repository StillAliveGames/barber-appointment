def test_login(client, app):
    with app.app_context():
        user = User(username='test', email='test@test.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'pass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Вход выполнен' in response.data