# tests/test_customer_routes.py

import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import LoginManager, UserMixin
from flask_login import login_user
from flask_login import FlaskLoginClient
from apps import create_app, db
from apps.customer.models import Customer
from apps.config import config_dict

get_config_mode = 'Testing'
try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')


class User(UserMixin):
    def __init__(self, id):
        self.id = id


class TestCustomerRoutes(TestCase):

    def create_app(self):
        # Set up the Flask application for testing
        app = create_app(app_config)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.test_client_class = FlaskLoginClient
        self.login_manager = LoginManager()
        self.login_manager.init_app(app)
        self.login_manager.user_loader(self.load_user)
        return app

    def load_user(self, user_id):
        return User(user_id)

    def setUp(self):
        # Set up the database
        db.create_all()
        # Add a sample customer
        customer = Customer(name='John Doe', phone='123-456-7890', email='john.doe@example.com', address='123 Main St')
        db.session.add(customer)
        db.session.commit()
        self.user = User(id=1)
        login_user(self.user)

    def tearDown(self):
        # Tear down the database
        db.session.remove()
        db.drop_all()

    def test_get_customers(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            # This request has user 1 already logged in!
            response = client.get('/customer/customers')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'John Doe', response.data)

    def test_add_customers(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            # This request has user 1 already logged in!
            response = client.post('/customer/customer',
                                   data=dict(name='Jane Doe', phone='123-456-7890', email='jane.doe@test.com',
                                             address='123 Main St'))
            self.assertEqual(response.status_code, 302)
            response = client.get('/customer/customers')
            self.assertIn(b'Jane Doe', response.data)


if __name__ == '__main__':
    unittest.main()
