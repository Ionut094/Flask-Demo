from flask_restful import Resource

from models.store import Store


class StoreResource(Resource):
    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {'message': 'Store not found'}, 401

    def post(self, name):
        if Store.find_by_name(name):
            return {'message': 'Store with name {} already exists'.format(name)}, 400

        store = Store(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store'}, 500
        return store.json(), 201

    def delete(self, name):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return [store.json() for store in Store.query.all()]
