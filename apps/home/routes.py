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


def get_monthly_sales():
    monthly_sales = db.session.query(
        func.strftime('%Y-%m', SaleOrder.order_date).label('month'),
        func.sum(SaleOrder.total_amount).label('total_sales')
    ).group_by('month').order_by('month').all()

    months = [sale.month for sale in monthly_sales]
    monthly_totals = [sale.total_sales for sale in monthly_sales]
    return months, monthly_totals

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
    print(months, monthly_totals)
    return render_template('home/index.html', segment='index',
                           top_customers=top_customers, daily_sales=daily_sales,
                           employee_names=employee_names, daily_total=daily_total,
                           total_sales=total_sales, top_employees=top_employees,
                           top_products=top_products, months=months, monthly_totals=monthly_totals)


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
