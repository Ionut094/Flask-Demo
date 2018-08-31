from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import ItemList, ItemResource
from resources.store import StoreResource, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'AAJJJA-5556fsdvmkdfknkdvkjxn'
api = Api(app)


@app.before_first_request
def create_tables():
    from db import db
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
