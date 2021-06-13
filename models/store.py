#import sqlite3
from FlaskApiProgramms.Section6.db import db


class StoreModel(db.Model):
    # for the purpose related to Sqlalchemy

    __tablename__ = 'stores'
    __table_args__ = {'extend_existing': True} #from stackoverflow for solving runtime error

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # items=db.relationship('ItemModel')
    items=db.relationship('ItemModel',lazy='dynamic')

    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]} #used when lazy = dynamic ( used when )
        # return {'name':self.name,'items':[item.json() for item in self.items]}

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
