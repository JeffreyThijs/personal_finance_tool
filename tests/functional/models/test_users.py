from app import db
from app.sqldb.models import User
from faker import Faker
from app.tools.helpers_classes import AttrDict

def test_login_page(test_client):
    response = test_client.get('/auth/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"New User?" in response.data
    assert b"Forgot Your Password?" in response.data
    
def test_valid_login_logout(test_client, init_database):

    # login
    response = test_client.post('/auth/login',
                                data=dict(username="test_user", password='test_password'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome test_user!" in response.data
    assert b"Overview" in response.data
    assert b"Tax" in response.data
    assert b"Prognosis" in response.data
    assert b"Current balance" in response.data
    assert b"logout" in response.data

    # logut
    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"New User?" in response.data
    assert b"Please log in to access this page." in response.data
    assert b"Overview" not in response.data
    assert b"Tax" not in response.data
    assert b"Prognosis" not in response.data
    assert b"Current balance" not in response.data
    assert b"login" in response.data

def test_invalid_login_logout(test_client, init_database):

    # login
    response = test_client.post('/auth/login',
                                data=dict(username="test_user", password='wrong'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
    assert b"New User?" in response.data
    assert b"login" in response.data
    assert b"Forgot Your Password?" in response.data

def test_valid_registration(test_client, init_database):
   
    # register
    response = test_client.post('/auth/register',
                                data=dict(username='KoolKat',
                                          email='jeffrey@pft.be',
                                          password='averygoodpassword',
                                          password2='averygoodpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"New User?" in response.data
    assert b"Forgot Your Password?" in response.data

    # login
    response = test_client.post('/auth/login',
                                data=dict(username="KoolKat", password='averygoodpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome KoolKat!" in response.data
    assert b"Please verifiy your email, check your email for instructions!"
    assert b"Overview" in response.data
    assert b"Tax" in response.data
    assert b"Prognosis" in response.data
    assert b"Current balance" in response.data
    assert b"logout" in response.data

    # logut
    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"New User?" in response.data
    assert b"Please log in to access this page." in response.data
    assert b"Overview" not in response.data
    assert b"Tax" not in response.data
    assert b"Prognosis" not in response.data
    assert b"Current balance" not in response.data
    assert b"login" in response.data

def test_invalid_registration(test_client, init_database):

    f = Faker()
    profile = AttrDict(f.profile())
   
    # register invalid password
    response = test_client.post('/auth/register',
                                data=dict(username=profile.username,
                                          email=profile.mail,
                                          password=f.password(),
                                          password2=f.password()),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Login" in response.data
    assert b"Username already used!" not in response.data
    assert b"Email already used!" not in response.data

    # register username already exists
    profile = AttrDict(f.profile())
    response = test_client.post('/auth/register',
                                data=dict(username='test_user',
                                          email=profile.mail,
                                          password=profile.job,
                                          password2=profile.job),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Login" in response.data
    assert b"Username already used!" in response.data
    assert b"Email already used!" not in response.data

    # register email already exists
    profile = AttrDict(f.profile())
    response = test_client.post('/auth/register',
                                data=dict(username=profile.username,
                                          email='test@test.test',
                                          password=profile.job,
                                          password2=profile.job),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Login" in response.data
    assert b"Username already used!" not in response.data
    assert b"Email already used!" in response.data

    # all cases
    response = test_client.post('/auth/register',
                                data=dict(username='test_user',
                                          email='test@test.test',
                                          password=f.password(),
                                          password2=f.password()),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Login" in response.data
    assert b"Username already used!" in response.data
    assert b"Email already used!" in response.data
