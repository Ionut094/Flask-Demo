from flask_restful import Resource
from flask import request

from models.user import User


class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if User.find_by_username(username):
            return {'error_message': 'User already exists'}, 400
        user = User(username, password)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201
