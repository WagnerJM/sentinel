from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
        create_access_token, 
        get_jwt_identity, 
        jwt_required,
        get_raw_jwt
        )

from app.api.user.models import User, UserSchema
from app.security import TokenBlacklist


class UserLoginApi(Resource):
    def post(self):
        response = {}
        data = data.get_json()
        user = User.find_by_username(username=data['username'])

        if user and user.check_pw(user._password, data['password']):
            response['token'] = create_access_token(
                    identity=str(user.id), fresh=True)
            response['status'] = "OK"
            response['msg'] = "Du wurdest erfolgreich eingeloggt."
            return response, 200
        else:
            response['status'] = "ERROR"
            response['msg'] = "Username und/oder Passwort falsch."
            return response, 401

        

class UserLogoutApi(Resource):
    
    @jwt_required
    def post(self):
        
        jti = get_raw_jwt()['jti']
        token = TokenBlacklist(jti=jti)
        token.save()
        
        return {
            "status": "OK",
            "msg": "User wurde erfolgreich ausgeloggt."
            }, 200
        

class AdminUserListApi(Resource):
    
    @jwt_required
    def get(self):
        response = {}
        user = User.find_by_id(get_jwt_identity())
        if not user.admin:
            response['status'] = "ERROR"
            response['msg'] = "No admin rights"
            return response, 403
        else:
            schema = UserSchema(many=True)
            users = User.get_all()
            return schema.dump(users).data, 200
            
        

    @jwt_required
    def post(self):
        response = {}
        user = User.find_by_id(get_jwt_identity())
        if not user.admin:
            response['status'] = "ERROR"
            response['msg'] = "No admin rights"
            return response, 403
        else:
            schema = UserSchema()
            result = schema.load(request.json)
            if not result.errors:
                if User.find_by_username(username=result.data['username']):
                    response["status"] = "ERROR"
                    response["msg"] = "Username existiert bereits"
                    return response, 400
                else:
                    data = request.get_json()
                    user = User(**data)
                    user.save()
                    response['status'] = "OK"
                    response['msg'] = "User wurde angelegt"
                    return response, 201
            else:
                response['status'] = "ERROR"
                response['msg'] = result.errors
                return response, 300
                    
