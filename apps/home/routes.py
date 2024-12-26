# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps import db
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.customer.models import Customer
from apps.sale.models import SaleOrder, OrderDetails
from apps.product.models import Products
from apps.employee.models import Employee
from sqlalchemy import func
from datetime import datetime, timedelta


def get_top_employee():
    top_employees = (
        db.session.query(
            Employee,
            func.sum(SaleOrder.total_amount).label('total_sales')
        )
        .join(SaleOrder, Employee.employee_id == SaleOrder.employee_id)
        .group_by(Employee.employee_id)
        .order_by(func.sum(SaleOrder.total_amount).desc())
        .limit(10)
        .all()
    )
    return top_employees


def get_top_products():
    top_products = (
        db.session.query(
            Products,
            func.sum(OrderDetails.quantity * OrderDetails.unit_price).label('total_sales')
        )
        .join(OrderDetails, Products.product_id == OrderDetails.product_id)
        .group_by(Products.product_id)
        .order_by(func.sum(OrderDetails.quantity * OrderDetails.unit_price).desc())
        .limit(10)
        .all()
    )
    return top_products


def get_today_qty():
    total_stock_qty_sold = db.session.query(
        func.sum(OrderDetails.quantity).label('total_stock_qty_sold')
    ).filter(func.strftime('%Y-%m-%d', SaleOrder.order_date) == func.strftime('%Y-%m-%d', func.now())).scalar()
    return total_stock_qty_sold


def get_today_sales():
    today = datetime.now().date()
    total_sales_today = db.session.query(
        func.sum(SaleOrder.total_amount).label('total_sales')
    ).filter(
        func.date(SaleOrder.order_date) == today
    ).scalar()
    return total_sales_today


def get_monthly_sales():
    monthly_sales = db.session.query(
        func.strftime('%Y-%m', SaleOrder.order_date).label('month'),
        func.sum(SaleOrder.total_amount).label('total_sales')
    ).group_by('month').order_by('month').all()

    months = [sale.month for sale in monthly_sales]
    monthly_totals = [sale.total_sales for sale in monthly_sales]
    return months, monthly_totals


def get_last_7_days_product_qty():
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=6)
    daily_product_qty = db.session.query(
        func.strftime('%Y-%m-%d', SaleOrder.order_date).label('date'),
        func.sum(OrderDetails.quantity).label('total_qty')
    ).join(SaleOrder, OrderDetails.order_id == SaleOrder.id).filter(
        SaleOrder.order_date.between(seven_days_ago, today)
    ).group_by('date').order_by('date').all()

    dates = [record.date for record in daily_product_qty]
    quantities = [record.total_qty for record in daily_product_qty]
    return dates, quantities


def get_monthly_order_quantities():
    monthly_order_quantities = db.session.query(
        func.strftime('%Y-%m', SaleOrder.order_date).label('month'),
        func.sum(OrderDetails.quantity).label('total_quantity')
    ).join(OrderDetails, SaleOrder.id == OrderDetails.order_id).group_by('month').order_by('month').all()

    months = [record.month for record in monthly_order_quantities]
    quantities = [record.total_quantity for record in monthly_order_quantities]
    return months, quantities

def get_last_7_days_employee_orders():
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=6)
    daily_employee_orders = db.session.query(
        func.strftime('%Y-%m-%d', SaleOrder.order_date).label('date'),
        Employee.name,
        func.count(SaleOrder.id).label('order_count')
    ).join(Employee, SaleOrder.employee_id == Employee.employee_id).filter(
        SaleOrder.order_date.between(seven_days_ago, today)
    ).group_by('date', Employee.name).order_by('date').all()

    data = {}
    for record in daily_employee_orders:
        if record.name not in data:
            data[record.name] = {'dates': [], 'order_counts': []}
        while len(data[record.name]['dates']) < (datetime.strptime(record.date, '%Y-%m-%d').date() - seven_days_ago).days:
            data[record.name]['dates'].append((seven_days_ago + timedelta(days=len(data[record.name]['dates']))).strftime('%Y-%m-%d'))
            data[record.name]['order_counts'].append(0)
        data[record.name]['dates'].append(record.date)
        data[record.name]['order_counts'].append(record.order_count)
    print(data)
    return data

@blueprint.route('/index')
@login_required
def index():
    top_customers = (
        db.session.query(
            Customer,
            func.sum(SaleOrder.total_amount).label('total_order_amount')
        )
        .join(SaleOrder, Customer.customer_id == SaleOrder.customer_id)
        .group_by(Customer.customer_id)
        .order_by(func.sum(SaleOrder.total_amount).desc())
        .limit(10)
        .all()
    )
    top_employees = get_top_employee()
    top_products = get_top_products()
    daily_sales = db.session.query(
        Employee.name,
        func.sum(SaleOrder.total_amount).label('total_sales')
    ).join(Employee, SaleOrder.employee_id == Employee.employee_id).group_by(Employee.name).all()
    employee_names = [sale.name for sale in daily_sales]
    daily_total = sum([sale.total_sales for sale in daily_sales])
    total_sales = [sale.total_sales for sale in daily_sales]
    months, monthly_totals = get_monthly_sales()
    total_stock_qty_sold_today = get_today_qty()
    dates, quantities = get_last_7_days_product_qty()
    shipment_months, shipment_quantities = get_monthly_order_quantities()
    total_sales_today = get_today_sales()
    employee_orders_data = get_last_7_days_employee_orders()
    return render_template('home/index.html', segment='index',
                           top_customers=top_customers, daily_sales=daily_sales,
                           employee_names=employee_names, daily_total=daily_total,
                           total_sales=total_sales, top_employees=top_employees,
                           top_products=top_products, months=months, monthly_totals=monthly_totals,
                           total_stock_qty_sold_today=total_stock_qty_sold_today,
                           dates=dates, quantities=quantities,
                           shipment_months=shipment_months, shipment_quantities=shipment_quantities,
                           total_sales_today=total_sales_today,
                           employee_orders_data=employee_orders_data)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
