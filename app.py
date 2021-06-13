from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item,ItemList
from db import db
from resources.store import Store,StoreList

from security import auth, identity
'''

flow for authentication :-

/auth endpoint directly call the JWT constructor and then call the auth function and return the "JWT" token

after that whenever we call any endpoint who has the decorator @JWtrequried then it will get the identity by using payload
method first do the next processing. OKAY!! now gaining the concept
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db' #sqlite can be mysql ,oracle or anything and sqlalchemy still works postgresql
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.config['SQLALCHMY_TRACK_MODIFICATION']=False
app.secret_key = 'jose'
api = Api(app)

#used to create the database table automatically
# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWT(app, auth, identity)

items = []

#all resource are in present in resource directory
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/reg')

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
#     db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
