# apps/sale/routes.py

from apps.sale import blueprint
from flask import render_template, request, redirect, url_for
from apps.sale.models import SaleOrder, OrderDetails
from apps.product.models import Products
from apps.customer.models import Customer
from apps.employee.models import Employee
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

# @blueprint.route('/create_order', methods=['GET', 'POST'])
# def create_order():
#     if request.method == 'POST':
#         customer_id = request.form['customer_id']
#         order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
#         total_amount = request.form['total_amount']
#
#         new_order = SaleOrder(customer_id=customer_id, order_date=order_date, total_amount=total_amount)
#         db.session.add(new_order)
#         db.session.commit()
#
#         return redirect(url_for('sale_blueprint.orders'))
#
#     customers = Customer.query.all()
#     return render_template('sale/create_order.html', customers=customers)

@blueprint.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        employee_id = request.form['employee_id']
        order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()

        # Handle order details
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        unit_prices = request.form.getlist('unit_price')

        total_amount = 0
        for quantity, unit_price in zip(quantities, unit_prices):
            total_amount += int(quantity) * float(unit_price)

        new_order = SaleOrder(customer_id=customer_id, order_date=order_date, total_amount=total_amount, employee_id=employee_id)
        db.session.add(new_order)
        db.session.commit()

        for product_id, quantity, unit_price in zip(product_ids, quantities, unit_prices):
            order_detail = OrderDetails(
                order_id=new_order.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price,
            )
            db.session.add(order_detail)

        db.session.commit()

        return redirect(url_for('sale_blueprint.orders'))

    customers = Customer.query.all()
    products = Products.query.all()
    employees = Employee.query.all()
    return render_template('sale/create_order.html', customers=customers, products=products, employees=employees)


@blueprint.route('/order/<int:order_id>')
def view_order(order_id):
    order = SaleOrder.query.get_or_404(order_id)
    order_details = OrderDetails.query.filter_by(order_id=order_id).all()
    return render_template('sale/view_order.html', order=order, order_details=order_details)
