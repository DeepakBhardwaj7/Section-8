#import sqlite3
from db import db


class ItemModel(db.Model):
    # for the purpose related to Sqlalchemy
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True} #This is included for surpassing the run time error

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.String(80))

    store_id=db.Column(db.Integer,db.ForeignKey('stores.id'))
    store=db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name=name
        self.price=price
        self.store_id=store_id

    def json(self):
        return {'name':self.name,"price":self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()     #(filer_by(name=name,id=id.....)     #"SELECT * from items where name=name LIMIT 1" but here is a query builder to iterate easily

        #----------------------------------------without sqlalchmy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * from items where name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return cls(*row).json()
        # ----------------------------------------without sqlalchmy

    def save_to_db(self):  #use to update the value inside the database
        db.session.add(self)  # session-> is a collection of objects
        db.session.commit()

    def delete_from_db(self):  #use to delete the particular object
        db.session.delete(self)
        db.session.commit()

#-----------------------------------------------------------------The above method does both the things easily so we don't really need the saperatly 2 method for update & delete

    # def insert(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "INSERT INTO items VALUES(?,?)"
    #     cursor.execute(query, (self.name, self.price,))
    #
    #     connection.commit()
    #     connection.close()
    #
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name,))
    #
    #     connection.commit()
    #     connection.close()
