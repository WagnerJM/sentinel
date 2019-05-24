import pytest
import requests

baseUrl = "http://localhost:5001/api/v1"

register_user = {
    "username": "register_user",
    "password": "testpw2134",
    "email": "testemail@test.de"
    }
token = ""

headers = {'content-type': 'application/json'}



def test_login():
    resource = "/login"
    url = baseUrl + resource
    
    login_user = {
    "username": "register_user",
    "password": "testpw2134"
    }
    
    r = requests.post(url, json=login_user, headers=headers)
    token = r.json['token']
    
    assert r.status_code == 200
    assert r.json['status'] == "OK"
    assert r.json['msg'] == "Du wurdest erfolgreich eingeloggt."
    assert r.json != ""
    
def test_logout():
    resource = "/logout"
    url = baseUrl + resource
    if token not "":
        headers['Authorization'] = "Bearer {}".format(token)
        r = requests.post(url, headers=headers)
        del headers['Authorization']
        
        assert r.status_code == 200
        assert r.json['status'] == "OK"
        assert r.json['msg'] == "User wurde erfolgreich ausgeloggt."
        
    else:
        r = requests.post(url, headers=headers)
        assert r.status_code == 401
        assert r.json['description'] == 'Request does not contain an access 
                                        \ token.'
        assert r.json['error'] == 'authorization required'

    
    
def test_get_user_data():
    pass

def test_admin_register_user():
    
    resource = "/login"
    url = baseUrl + resource
    
    admin_user = { "username": "admin", "password": "admin"}
    
    r = requests.post(url, json=admin_user, headers=headers)
    headers['Authorization'] = "Bearer {}".format(r.json['token'])
    
    resource = "/register"
    url = baseUrl + resource

    r = requests.post(url, json=register_user, headers=headers)
    
    resource = "/logout"
    url = baseUrl + resource
    
    logout = requests.post(url, headers=headers)
    
    del headers['Authorization']
    
    assert r.status_code == 201
    assert r.json['status'] == "OK"
    assert r.json['msg'] == "User wurde erfolgreich angelegt."
 
