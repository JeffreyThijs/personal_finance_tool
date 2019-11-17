def test_new_user(test_users):
    new_user = test_users(amount=1)[0]
    assert new_user.id != None
    assert new_user.username == 'test_user'
    assert new_user.email == 'test@test.test'
    assert new_user.password != 'test_password'
    assert new_user.check_password('test_password')
    assert not new_user.check_password('password')
    
def test_setting_password(test_users):
    new_user = test_users(amount=1)[0]
    new_user.password = 'MyNewPassword'
    assert new_user.password_hash != 'MyNewPassword'
    assert new_user.check_password('MyNewPassword')
    assert not new_user.check_password('MyNewPassword2')
    assert not new_user.check_password('test_password')