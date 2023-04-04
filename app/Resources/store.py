from flask_restful import Resource, reqparse
from app.Model.store_model import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="price can't be empty")
    parser.add_argument("store_id", type=int, required=True, help="Store_id can't be blank")

    def get(self, name):
        store =StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "store already exist".format(name)}

        store = StoreModel()
        try:
            store.save_to_db()
        except:
            return {"message": "an error occurred with creating the store"}
        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "store deleted"}

class StoreList(Resource):
    def get(self):
        return{"stores": StoreModel.get_all_stores()}