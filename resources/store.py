from flask_restful import Resource
from FlaskApiProgramms.Section6.models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"Message":"A store with name '{}' not exists.".format(name)},400

    def post(self,name):
        if StoreModel.find_by_name(name):
            print(1)
            return {"Message":"A store with same name already created!"}

        store=StoreModel(name)
        print(2)
        try:
            print(3)
            store.save_to_db()
        except:
            return {"messge":"An error occurred while creating the store"},500
        return store.json(),201

    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message ':"Deleted successfully!"}
        return {"message":"No store found for this name"}


class StoreList(Resource):
    def get(self):
        return {"Stores":[store.json() for store in StoreModel.query.all()]}