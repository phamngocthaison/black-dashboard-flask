# apps/customer/routes.py

from flask import request, jsonify
from flask import render_template, request, redirect, url_for
from apps import db
from apps.customer.models import Customer
from apps.customer import blueprint

customer_blueprint = blueprint

@customer_blueprint.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return render_template('customer/customer_list.html', customers=customers)

@customer_blueprint.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.__repr__())

@customer_blueprint.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        address=data['address']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.__repr__()), 201

@customer_blueprint.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    customer.name = data['name']
    customer.phone = data['phone']
    customer.email = data['email']
    customer.address = data['address']
    db.session.commit()
    return jsonify(customer.__repr__())

@customer_blueprint.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204