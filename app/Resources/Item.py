from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt, get_jwt_identity)

from app.Model.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="price cannot be empty!")
    parser.add_argument("store_id", type=int, required=True, help="store_id cannot be null!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return{"message": "Item Not Found"}


    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        try:
            item.save_to_db()
        except:
            return {"message": "an error occurred inserting the item"}
        return item.json()


    @jwt_required()
    def delete(self, name):
        claims =get_jwt()
        print(claims)
        if not claims["is_admin"]:
            return {"message": "admin privilege required"}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item delete"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.price = data["price"]
            except:
                return{"message": "An error occurred updating the item"}
            else:
                try:
                    item =ItemModel(name, data['price'], data['store_id'])
                except:
                    return {"message": "An error occurred inserting the item"}

            item.save_to_db()
            return item.json()



class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        #print(1)
        user_id = get_jwt_identity()
        #print(2)
        items = ItemModel.get_all_items()
        if user_id:
            return{"items": items}
        return {"items": [item["name"] for item in items],
                "message": "More data available if you log in"}