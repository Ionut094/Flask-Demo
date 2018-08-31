from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required

from models.item import Item


class ItemResource(Resource):

    @jwt_required()
    def get(self, name):
        return Item.find_by_name(name).json()

    def post(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            return {'message': 'The item {} already exists'.format(name)}, 400
        item = Item(name, data['price'], data['store_id'])

        item.save_to_db()

        return item.json(), 201

    def delete(self, name):
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

    def get(self):
        return [item.json() for item in Item.query.all()]
