from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy

import datetime
app = Flask(__name__)

#This file contains the information for connecting to DB
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

#User/Retailer would contain multiple items.
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    items = db.relationship('Item', backref='users', lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

# This class would contain all the logs.
class ActivityLog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    variant_id =  db.Column(db.Integer)
    date_created = db.Column(db.DateTime,default= datetime.datetime.now)

    def __init__(self,user_id,action,item_id,variant_id):
        self.user_id = user_id
        self.action = action
        self.item_id = item_id
        self.variant_id = variant_id

    #start=20180624152917
    #end=20180625101910
    @app.route('/<start>/<end>')
    def timeline(start,end,user=None):
        return ActivityLog.timeline(start_date=start,end_date=end,user_id=user)


    @app.route('/<start>/<end>/<int:user>')
    def timeline_with_user(start,end,user):
        return ActivityLog.timeline(start_date=start,end_date=end,user_id=user)


    @classmethod
    def timeline(cls,start_date,end_date,user_id):
        start = datetime.datetime.strptime(start_date,'%Y%m%d%H%M%S')
        end = datetime.datetime.strptime(end_date,'%Y%m%d%H%M%S')
        actions = ["created","edited name of","edited brand of","edited category of","deleted","added","edited","deleted"]
        statement = []
        if user_id == None:
            results = ActivityLog.query.filter(start < ActivityLog.date_created).filter(end > ActivityLog.date_created).all()
        else:
            results = ActivityLog.query.filter(start < ActivityLog.date_created).filter(end > ActivityLog.date_created).filter(ActivityLog.user_id == user_id).all()
        for index,row in enumerate(results):
            #statement  = "User X edited Item's price"
            username = User.query.filter_by(id=row.user_id).first().name
            item_action = actions[row.action]
            item_name = Item.query.filter_by(id=row.item_id).first().name
            if row.variant_id != None:
              variant_name = Variant.query.filter_by(id=row.variant_id).first().name
              statement.append('' + str(username) + ' ' + str(item_action) + ' ' + str(item_name) + '\'s ' + str(variant_name) + '')
            else:
              statement.append('' + str(username) + ' ' + str(item_action) + ' ' + str(item_name) + '')
        return jsonify(statement)


# Item class should have methods to :
# Add Item and variant
# Remove Item and variant
# Modify Item and varaint
class Item(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(30))
     brand = db.Column(db.String(20))
     date_created = db.Column(db.DateTime, default= datetime.datetime.now)
     date_modified = db.Column(db.DateTime, default= datetime.datetime.now)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

     variants = db.relationship('Variant', backref='item', lazy='dynamic')

     def __init__(self,name,brand,user_id):
        self.name = name
        self.brand = brand
        self.user_id = user_id

     def __repr__(self):
        return '<Item %r>' %self.name


     @classmethod
     def AutoLog(cls,user_id,action,item_id,variant_id):
        new_log = ActivityLog(user_id=user_id,action=action,item_id=item_id,variant_id=variant_id)
        db.session.add(new_log)
        db.session.commit()

     @classmethod
     def add_item(cls,name,brand,user_id):
        new_item = Item(name=name,brand=brand,user_id=user_id)
        db.session.add(new_item)
        db.session.commit()
        Item.AutoLog(user_id=user_id, action=1,item_id=new_item.id,variant_id=None)

     def edit_item_name(self,new_item_name):
        self.name = new_item_name
        Item.AutoLog(user_id=self.user_id, action=2, item_id=self.id,variant_id=None)
        #Not making flush and commit a function to avoid any problems during unit testing.
        db.session.flush()
        db.session.commit()

     def edit_brand_name(self,brand_name):
        self.brand = brand_name
        Item.AutoLog(user_id=self.user_id, action=3, item_id=self.id,variant_id=None)
        db.session.flush()
        db.session.commit()

     def edit_category_name(self,category_name):
        self.category = category_name
        Item.AutoLog(user_id=self.user_id, action=4, item_id=self.id,variant_id=None)
        db.session.flush()
        db.session.commit()

     def remove_item(self):
        Item.query.filter_by(id=self.id).delete()
        Item.AutoLog(user_id=self.user_id, action=5, item_id=self.id,variant_id=None)
        db.session.flush()
        db.session.commit()

     def add_variant(self,name,value):
        new_var = Variant(name=name,value=value,item_id=self.id)
        db.session.add(new_var)
        db.session.commit()
        variant_id = Variant.query.filter_by(name=name).first().id
        Item.AutoLog(user_id=self.user_id, action=6, item_id=self.id,variant_id=variant_id)

     def edit_variant(self,name,new_value):
        variant_id = Variant.query.filter_by(name=name).filter_by(item_id=self.id).first().id
        Variant.query.filter_by(name=name).first().value = new_value
        db.session.flush()
        db.session.commit()
        Item.AutoLog(user_id=self.user_id, action=7, item_id=self.id,variant_id=variant_id)

     def remove_variant(self,variant_name):
        variant_rem = Variant.query.filter_by(name=variant_name).first()
        Item.AutoLog(user_id=self.user_id, action=8, item_id=self.id,variant_id=variant_rem.id)
        variant_rem.delete()
        db.session.flush()
        db.session.commit()


#Variant class would contain a constructor for object initialisation.
class Variant(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(20))
     value = db.Column(db.String(20))
     item_id = db.Column(db.Integer,db.ForeignKey('item.id'))

     def __init__(self,name,value,item_id):
        self.name = name
        self.value = value
        self.item_id = item_id

     def __repr__(self):
        return '<Variant %r>' %self.name


#db.Table('item_variants',
#   db.Column('item_id',db.Integer,db.ForeignKey('item.id')),
#   db.Column('variant_id',db.Integer,db.ForeignKey('variant.id')),
#   db.Column('date_created',db.DateTime, default= datetime.datetime.now)
#   )

if __name__ == '__main__':
    app.run()
