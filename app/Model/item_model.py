from ..config import database_path
from ..db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("UserModel")



    def __init__(self, name, price, store_id, users_id):
        self.name = name
        self.price = price
        self.store_id = store_id
        self.users_id = users_id




    def json(self):
        return {"id": self.id,
                "name": self.name,
                "price": self.price,
                "store_id": self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_all_items(cls):
        return[x.json() for x in cls.query.all()]