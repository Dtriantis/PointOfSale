import unittest
from app import create_app
from models import db

app = create_app()

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UnitTest.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
        
    # executed after each test
    def tearDown(self):
        pass
    
    ### tests ###

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_item_crud(self):
        response = self.addMenuItemHelper('pizza', 5, 10)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(b'Menu Item added', response.data)

        response = self.updateMenuItemHelper('pizza', 10, 20)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'Menu Item Updated', response.data)

        response = self.getMenuItemHelper(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'[{"description":"pizza","id":1,"price":20,"quantity":10}]\n', response.data)

        response = self.deleteMenuItemHelper(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'Menu Item Deleted', response.data)


    ### helpers ###

    def addMenuItemHelper(self, description, quantity, price):
        return self.app.post(
        '/menuItems',
        json = {"description": description, "quantity": quantity, "price": price},
        follow_redirects=True)
    
    def updateMenuItemHelper(self, description, quantity, price):
        return self.app.put(
        '/menuItems/1',
        json = {"description": description, "quantity": quantity, "price": price},
        follow_redirects=True)
        
    def getMenuItemHelper(self, id):
        return self.app.get(
        '/menuItems/'+str(id),
        follow_redirects=True)
            
    def deleteMenuItemHelper(self, id):
        return self.app.delete(
        '/menuItems/'+str(id),
        follow_redirects=True)
    
if __name__ == "__main__":
    unittest.main()