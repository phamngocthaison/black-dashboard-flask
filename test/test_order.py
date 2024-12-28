import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import LoginManager, UserMixin, login_user, FlaskLoginClient
from apps import create_app, db
from apps.sale.models import SaleOrder, OrderDetails
from apps.customer.models import Customer
from apps.employee.models import Employee
from apps.product.models import Products
from apps.config import config_dict
from datetime import datetime


class User(UserMixin):
    def __init__(self, id):
        self.id = id


class TestOrderRoutes(TestCase):

    def create_app(self):
        app_config = config_dict['Testing']
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
        self.customer = Customer(name='Test Customer', phone='123-456-7890', email='test@example.com',
                                 address='123 Main St')
        self.employee = Employee(name='Test Employee', position='Tester', phone='555-123-4567',
                                 email='test.employee@example.com',
                                 hire_date=datetime.strptime('2023-01-01', '%Y-%m-%d').date())
        self.product = Products(name='Test Product', description='Test Description', price=100.0, stock=50)
        db.session.add(self.customer)
        db.session.add(self.employee)
        db.session.add(self.product)
        db.session.commit()
        db.session.refresh(self.customer)  # Ensure the instance is bound to the session
        db.session.refresh(self.employee)  # Ensure the instance is bound to the session
        db.session.refresh(self.product)  # Ensure the instance is bound to the session
        self.user = User(id=1)
        login_user(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_order(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            response = client.post('/sale/create_order', data=dict(
                customer_id=self.customer.customer_id,
                employee_id=self.employee.employee_id,
                order_date=datetime.now().date(),
                total_amount=500.0,
                product_id=[self.product.product_id],
                quantity=[5],
                unit_price=[100.0]
            ))
            self.assertEqual(response.status_code, 302)
            order = SaleOrder.query.filter_by(customer_id=self.customer.customer_id).first()
            self.assertIsNotNone(order)
            self.assertEqual(order.total_amount, 500.0)
            order_detail = OrderDetails.query.filter_by(order_id=order.id).first()
            self.assertIsNotNone(order_detail)
            self.assertEqual(order_detail.quantity, 5)
            self.assertEqual(order_detail.unit_price, 100.0)

    def test_get_order(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            order = SaleOrder(customer_id=self.customer.customer_id, employee_id=self.employee.employee_id,
                              order_date=datetime.now().date(), total_amount=500.0)
            db.session.add(order)
            db.session.commit()
            response = client.get(f'/sale/')
            self.assertEqual(response.status_code, 200)
            data = response.data
            self.assertIn(b'Test Customer', data)
            self.assertIn(b'Test Employee', data)
            self.assertIn(b'500.0', data)

    def test_view_order(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            order = SaleOrder(customer_id=self.customer.customer_id, employee_id=self.employee.employee_id,
                              order_date=datetime.now().date(), total_amount=500.0)
            db.session.add(order)
            db.session.commit()
            response = client.get(f'/sale/order/{order.id}')
            self.assertEqual(response.status_code, 200)
            data = response.data
            self.assertIn(b'Test Customer', data)
            self.assertIn(b'Test Employee', data)
            self.assertIn(b'500.0', data)


if __name__ == '__main__':
    unittest.main()
