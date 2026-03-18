def test_user_password(app):
    user = User(username='test', email='test@test.com')
    user.set_password('secret')
    assert user.check_password('secret')
    assert not user.check_password('wrong')