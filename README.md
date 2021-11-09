# Point of Sale App

## Simple Python Flask web application simulating a Point of Sale system

The POS system has the following capabilities:

* Retrieves a menu of all the items in the POS.
* Adds a new item to the menu
* Updates an item by ID
* Deletes an item by ID
* Creates a new order.

An item has:

* Description
* Price
* Quantity
* Id

An order has:

* List of item IDs, with a quantity for each item
* Payment amount
* Order note

### Installation

Clone this repository
```
git clone https://github.com/Dtriantis/PointOfSale.git
```

Create a virtual Enviroment
```
virtualenv -p python3 env
source env/bin/activate 
```

Install the required packages
```
pip install requirements.txt
```

Run project
```
python pos/run.py
```
Navigate to http://localhost:5000/docs in order to launch Swagger UI