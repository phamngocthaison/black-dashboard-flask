# tests/test_product_routes.py

import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import LoginManager, UserMixin, login_user, FlaskLoginClient
from apps import create_app, db
from apps.product.models import Products
from apps.config import config_dict

get_config_mode = 'Testing'
try:
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')


class User(UserMixin):
    def __init__(self, id):
        self.id = id


class TestProductRoutes(TestCase):

    def create_app(self):
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
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.product = Products(name='Test Product', description='Test Description', price=10.0, stock=100)
        db.session.add(self.product)
        db.session.commit()
        self.user = User(id=1)
        login_user(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_product(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            product = Products.query.first()  # Query the product again within the session
            response = client.get('/products/product/{}'.format(product.product_id))
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['product_id'], product.product_id)
            self.assertEqual(data['name'], product.name)
            self.assertEqual(data['description'], product.description)
            self.assertEqual(data['price'], product.price)
            self.assertEqual(data['stock'], product.stock)


if __name__ == '__main__':
    unittest.main()