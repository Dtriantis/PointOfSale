from os import error
from models.models import *
from flask import jsonify, request, Response, Blueprint, render_template
 
order = Blueprint('order', __name__)

# Home
@order.route('/', methods=['GET'])
def gethome():
    return Response("You are HOME", status=200, mimetype='application/json')

@order.route('/docs')
def get_docs():
    print('opening docs')
    return render_template('swaggerui.html')

# Endpoint to get all items of the menu
@order.route('/menuItems', methods=['GET'])
def getMenuItems():
    menu = MenuItem.getAllItems()
    if not menu:
        return Response("No items found on the Menu", status=400, mimetype='application/json')
    else:
        return jsonify({'Menu': menu})

# Endpoint to get menu item by id
@order.route('/menuItems/<int:id>', methods=['GET'])
def getMenuItem(id):
    item = MenuItem.getMenuItem(id)
    if not item:
        return Response("Menu Item with id: "+id+" was not found", status=400, mimetype='application/json')
    else:
        return jsonify(item)

# Endpoint to add menu item
@order.route('/menuItems', methods=['POST'])
def addMenuItem():
    request_data = request.get_json()

    if request_data is not None:
        try:
            MenuItem.addMenuItem(request_data["description"], request_data["quantity"],request_data["price"])
            response = Response("Menu Item added", 201, mimetype='application/json')
            return response
        except AssertionError as e:
            return Response('{}'.format(str(e)), status=400, mimetype='application/json')
        except Exception as e:
            return Response("Internal Issue", status=500, mimetype='application/json')
    else:
        response = Response("Failed to add Menu Item / Couldnt receive data", status=418, mimetype='application/json')
        return response

# Endpoint to update a menu item
@order.route('/menuItems/<int:id>', methods=['PUT'])
def updateMenuItem(id):
    request_data = request.get_json()
    try:
        MenuItem.updateMenuItem(id, request_data['description'], request_data['quantity'],request_data['price'])
    except AssertionError as e:
        return Response('{}'.format(str(e)), status=400, mimetype='application/json')
    response = Response("Menu Item Updated", status=200, mimetype='application/json')
    return response

# Endpoint to delete menu item
@order.route('/menuItems/<int:id>', methods=['DELETE'])
def removeMenuItem(id):
    MenuItem.deleteMenuItem(id)
    response = Response("Menu Item Deleted", status=200, mimetype='application/json')
    return response

# Endpoint to add New Order
@order.route('/addOrder', methods=['POST'])
def addNewOrder():
    request_data = request.get_json()
    if request_data is not None:
        Order.addOrder(request_data["description"], request_data["itemList"])
        response = Response("Order added", 201, mimetype='application/json')
        return response
    else:
        response = Response("Failed to add Order / couldnt receive data", status=418, mimetype='application/json')
        return response

# Endpoint to get all Orders
@order.route('/getOrders', methods=['GET'])
def getOrders():
    return jsonify({'Orders': Order.getAllOrders()})
