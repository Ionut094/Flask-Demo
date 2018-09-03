from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserResource, UserLogin, TokenRefreshResource, UserLogoutResource
from resources.item import ItemList, ItemResource
from resources.store import StoreResource, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'AAJJJA-5556fsdvmkdfknkdvkjxn'
api = Api(app)


@app.before_first_request
def create_tables():
    from db import db
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    from models.user import User
    if User.find_by_id(identity).is_admin:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'JWT Token has expired'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(token):
    return token['jti'] in BLACKLIST


api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutResource, '/logout')
api.add_resource(TokenRefreshResource, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
