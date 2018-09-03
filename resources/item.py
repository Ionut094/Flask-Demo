from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required

from models.item import Item


class ItemResource(Resource):

    @jwt_required
    def get(self, name):
        user = Item.find_by_name(name)
        if not user:
            return {'message': "User does not exist"}, 404
        return user.json()

    @fresh_jwt_required
    def post(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            return {'message': 'The item {} already exists'.format(name)}, 400
        item = Item(name, data['price'], data['store_id'])

        item.save_to_db()

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        item = Item.find_by_name(name)
        if not item:
            return {'message': 'The item {} was not found'.format(name)}, 404
        item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = request.get_json()
        item = Item(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = Item.find_all()
        if user_id:
            return {
                       'items': [item.json() for item in items]
                    }, 200
        return {
            'items': [item.name for item in items],
            'message': 'Login to view more data'
        }, 200
