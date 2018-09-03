from flask_restful import Resource
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity,
                                jwt_required, get_raw_jwt)

from models.user import User
from blacklist import BLACKLIST


class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        is_admin = data.get('is_admin', False)

        if User.find_by_username(username):
            return {'error_message': 'User already exists'}, 400
        user = User(username, password, is_admin)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201


class UserResource(Resource):

    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.find_by_username(username)
        if user and user.password == password:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials'}, 401


class UserLogoutResource(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}


class TokenRefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(current_user, fresh=False)

        return {
            'access_token': new_token
        }, 200
