import pytest

from app.api.user.models import User, UserSchema

user = {
    "username": "test_user",
    "password": "testpassword2345",
    "email": "test@test.de"
    }

def test_user_schema():
    schema = UserSchema()

    result = schema.load(user)
    assert result.errors == '{}'
   
   
def test_create_user():
    

    schema = UserSchema()
    
    result = schema.load(user)
    if result.errors == '{}':
        user = User(username, password, email)
        user.save()

        saved_user = User.find_by_username(username=user['username'])
    
        assert user['username'] == saved_user.username
        assert user['email'] == saved_user.email

def test_User_find_by_username():
     
    user = User.find_by_username(username=user['username'])
    
    assert user['username'] == saved_user.username
    assert user['email'] == saved_user.email
