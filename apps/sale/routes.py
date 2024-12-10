# apps/sale/routes.py

from apps.sale import blueprint
from flask import render_template, request, redirect, url_for
from apps.sale.models import SaleOrder
from apps.customer.models import Customer
from apps import db
from datetime import datetime

@blueprint.route('/')
def orders():
    orders = SaleOrder.query.all()
    print(orders)
    return render_template('sale/sale_order.html', orders=orders)

# @blueprint.route('/create', methods=['GET', 'POST'])
# def create_order():
#     if request.method == 'POST':
#         customer_name = request.form['customer_name']
#         order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
#         total_amount = request.form['total_amount']
#
#         new_order = SaleOrder(customer_name=customer_name, order_date=order_date, total_amount=total_amount)
#         db.session.add(new_order)
#         db.session.commit()
#
#         return redirect(url_for('sale_blueprint.orders'))
#
#     return render_template('sale/create_order.html')
#

@blueprint.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
        total_amount = request.form['total_amount']

        new_order = SaleOrder(customer_id=customer_id, order_date=order_date, total_amount=total_amount)
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('sale_blueprint.orders'))

    customers = Customer.query.all()
    return render_template('sale/create_order.html', customers=customers)