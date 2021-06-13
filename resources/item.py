from flask_jwt import jwt_required
import sqlite3
from flask_restful import Resource, reqparse

from FlaskApiProgramms.Section6.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item should belong to one store!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "This item is not present in the list"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'],data['store_id']) #ITemModel Object

        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item."},500
        return item.json()

#---------------------------------------------------------------------------before sql sqlalchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "Insert into items VALUES(?,?)"
        # cursor.execute(query, (item.name, item.price))
        # connection.commit()
        # connection.close()
        # return item.json(), 201
#--------------------------------------------------------------------------------------------
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message":"Deleted Sucessfully!!!"}
        return {"message": "Item -> {} is not available in the data base".format(name)}

# ---------------------------------------------------------------------------before sql sqlalchemy
        # if item:
        #     connection = sqlite3.connect('data.db')
        #     cursor = connection.cursor()
        #
        #     query = "DELETE from items where name=?"
        #     cursor.execute(query, (name,))
        #
        #     connection.commit()
        #     connection.close()
        #     return {"Message": "The item name -> {} has been deleted".format(name)}
        # return {"message": "Item -> {} is not available in the data base".format(name)}
# --------------------------------------------------------------------------------------------
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item=ItemModel(name,data['price'],data['store_id'])
        else:
            item.price=data['price']
            item.store_id=data['store_id']
        item.save_to_db()
        return item.json()


#--------------------------------------------------------------------------------------------
        # if ItemModel.find_by_name(name):
        #     item.update()
        #     return item.json()
        # else:
        #     item.insert()
        #     return item.json()


class ItemList(Resource):
    def get(self):
        #peraferable ----> bcoz more read able# return {'items': [item.json() for item in ItemModel.query.all()]}  # here, we are using the list comprehension for itereating throug all the items in db and return in json
        return {'items':list(map(lambda x:x.json(),ItemModel.query.all()))}  # here, we are using the Lambda function to iterate all over to the items of database

        #---------------------------------------------------------------------------
        # connection = sqlite3.connect("data.db")
        # cursur = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursur.execute(query)
        #
        # items = []
        #
        # for row in result:
        #     # str="{ name={} price={} }".format(row[0],row[1])
        #     items.append({"name": row[1], 'price': row[2]})
        # connection.close()
        #
        # return items
