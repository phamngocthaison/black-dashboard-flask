# apps/customer/routes.py

from flask import request, jsonify
from flask import render_template, request, redirect, url_for, flash
from apps import db
from apps.customer.models import Customer
from apps.customer import blueprint

customer_blueprint = blueprint


@customer_blueprint.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return render_template('customer/customer_list.html', customers=customers)


@customer_blueprint.route('/customer/<int:customer_id>/edit', methods=['GET'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('customer/edit_customer.html', customer=customer)


@customer_blueprint.route('/customer/<int:customer_id>/edit', methods=['POST'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer.name = request.form['name']
    customer.phone = request.form['phone']
    customer.email = request.form['email']
    db.session.commit()
    flash('Customer updated successfully', 'success')
    return redirect(url_for('customer_blueprint.get_customers'))


@customer_blueprint.route('/customer', methods=['POST'])
def create_customer():
    data = request.form
    new_customer = Customer(
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        address=data['address']
    )
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('customer_blueprint.get_customers'))


@customer_blueprint.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.__repr__())


@customer_blueprint.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204
