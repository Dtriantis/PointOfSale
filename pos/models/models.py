from sqlalchemy import PickleType
from sqlalchemy.orm import validates
from . import db

#######################
### Menu Item Model ###
#######################

class MenuItem(db.Model):
    __tablename__ = 'menuItems'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable=False)

    #########################################
    ### Methods for Model Bussiness logic ###
    #########################################

    def json(self):
        return {'id': self.id, 'description': self.description,
        'quantity': self.quantity, 'price': self.price, }

    def addMenuItem(_description, _quantity, _price):
        new_item = MenuItem(description=_description, quantity=_quantity, price=_price)
        db.session.add(new_item)
        db.session.commit()

    def getAllItems():
        return [MenuItem.json(item) for item in MenuItem.query.all()]

    def getMenuItem(_id):
        return [MenuItem.json(MenuItem.query.filter_by(id=_id).first())]

    def updateMenuItem(_id, _description, _quantity, _price):

        item_to_update = MenuItem.query.filter_by(id=_id).first()
        item_to_update.description = _description
        item_to_update.quantity = _quantity
        item_to_update.price = _price
        db.session.commit()

    def deleteMenuItem(_id):
        item = MenuItem.query.filter_by(id=_id).first()
        if item:
                MenuItem.query.filter_by(id=_id).delete()
                db.session.commit()
        else:
            raise AssertionError('Item not found') 

    ###############################
    ### Menu Item DB Validation ###
    ###############################

    @validates('price')
    def validatePrice(self, key, price):
        if not price:
            raise AssertionError('No Price was provided for the Item')
        try:
            val = int(price)
        except ValueError:
            raise AssertionError('Price must be a positive number') 
        if price < 1:
            raise AssertionError('Price must be a positive number') 
        return price

    @validates('description') 
    def validatePrice(self, key, description):
        if not description:
            raise AssertionError('No Name description was provided for the Item')
        if MenuItem.query.filter(MenuItem.description == MenuItem).first():
            raise AssertionError('Name description is already in use')
        if len(description) < 1 or len(description) > 100:
            raise AssertionError('Name must be between 1 and 100 characters') 
        return description

    @validates('quantity') 
    def validatePrice(self, key, quantity):
        try:
            val = int(quantity)
        except ValueError:
            raise AssertionError('Quantity must be a positive number') 
        if quantity < 0:
            raise AssertionError('Quantity must be a positive number') 
        return quantity

###################
### Order Model ###
###################

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    itemList = db.Column(PickleType)
    price = db.Column(db.Integer, nullable=False)

    #########################################
    ### Methods for Model Bussiness logic ###
    #########################################

    def json(self):
        return {'id': self.id, 'itemList': self.itemList,
         'description': self.description, 'price': self.price}

    def addOrder(_description, _itemList):

        # Calculate order price
        orderPrice = 0
        for i in range(len(_itemList)):
            oldItem = MenuItem.query.filter_by(id=_itemList[i]['id']).first()
            orderPrice = orderPrice +  _itemList[i]['quantity']*oldItem.price
        
        # Create order
        new_item = Order(description=_description, itemList=_itemList, price=orderPrice)
        if _itemList:
            # Update item's available quantities and order price
            for i in range(len(_itemList)):
                oldItem = MenuItem.query.filter_by(id=_itemList[i]['id']).first()
                newQuantity = oldItem.quantity - _itemList[i]['quantity']
                MenuItem.updateMenuItem(oldItem.id, oldItem.description , newQuantity, oldItem.price)

        db.session.add(new_item)
        db.session.commit()
        return new_item.id

    def getAllOrders():
        return [Order.json(item) for item in Order.query.all()]

    def deleteOrder(_id):
        item = Order.query.filter_by(id=_id).first()
        if item:
                Order.query.filter_by(id=_id).delete()
                db.session.commit()
        else:
            raise AssertionError('Order not found') 

    ###########################
    ### Order DB Validation ###
    ###########################

    @validates('description') 
    def validatePrice(self, key, description):
        if not description:
            raise AssertionError('No description was provided for the Order')
        if len(description) < 1 or len(description) > 200:
            raise AssertionError('Name must be between 1 and 200 characters') 
        return description

    @validates('itemList') 
    def validatePrice(self, key, itemList):
        if not itemList:
            raise AssertionError('Order has to contain at least 1 Item from the menu')
        for i in range(len(itemList)):
            try:
                menuitem = MenuItem.query.filter_by(id=itemList[i]['id']).first()
            except NameError:
                raise AssertionError('Item with Id ' + id + 'does not exist in order to fullfill the order')
            if(menuitem.quantity < itemList[i]['quantity']):
                raise AssertionError('There is not enough '+ menuitem.description +' available to complete this order')
        return itemList