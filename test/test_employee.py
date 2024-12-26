# tests/test_employee_routes.py

import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import LoginManager, UserMixin, login_user, FlaskLoginClient
from apps import create_app, db
from apps.employee.models import Employee
from apps.config import config_dict
from datetime import datetime

get_config_mode = 'Testing'
try:
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')


class User(UserMixin):
    def __init__(self, id):
        self.id = id


class TestEmployeeRoutes(TestCase):

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
        self.employee = Employee(name='Test Employee', position='Tester', phone='123-456-7890', email='test@test.com',
                                 hire_date=datetime.strptime('2024-01-01', '%Y-%m-%d').date())
        db.session.add(self.employee)
        db.session.commit()
        self.user = User(id=1)
        login_user(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_employee(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            employee = Employee.query.first()  # Query the employee again within the session
            response = client.get('/employee/employees')
            self.assertEqual(response.status_code, 200)
            data = response.data
            self.assertIn(b'Test Employee', data)
            self.assertIn(b'Tester', data)
            self.assertIn(b'123-456-7890', data)
            self.assertIn(b'test@test.com', data)

    def test_create_employee(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            response = client.post('/employee/employee', data=dict(
                name='New Employee', position='Developer', phone='123-456-7890', email='test@dev.com',
                hire_date='2024-01-01'
            ))
            self.assertEqual(response.status_code, 302)
            employee = Employee.query.filter_by(name='New Employee').first()
            self.assertIsNotNone(employee)
            self.assertEqual(employee.position, 'Developer')
            self.assertEqual(employee.phone, '123-456-7890')
            self.assertEqual(employee.email, 'test@dev.com')

    def test_update_employee(self):
        user = User(id=1)
        with self.app.test_client(user=user) as client:
            employee = Employee.query.first()
            response = client.post(f'/employee/{employee.employee_id}/edit', data=dict(
                name='Updated Employee', position='Senior Developer', phone='123-456-7890',
                email='update@email.com', hire_date='2024-01-01'
            ))
            self.assertEqual(response.status_code, 302)
            updated_employee = Employee.query.get(employee.employee_id)
            self.assertEqual(updated_employee.name, 'Updated Employee')
            self.assertEqual(updated_employee.position, 'Senior Developer')
            self.assertEqual(updated_employee.phone, '123-456-7890')
            self.assertEqual(updated_employee.email, 'update@email.com')


if __name__ == '__main__':
    unittest.main()
