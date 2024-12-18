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
from apps.sale.models import SaleOrder
from sqlalchemy import func

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
    daily_sales = db.session.query(
        SaleOrder.employee_id,
        func.sum(SaleOrder.total_amount).label('total_sales')
    ).group_by(SaleOrder.employee_id).all()
    employee_ids = [sale.employee_id for sale in daily_sales]
    daily_total = sum([sale.total_sales for sale in daily_sales])
    total_sales = [sale.total_sales for sale in daily_sales]
    return render_template('home/index.html', segment='index',
                           top_customers=top_customers, daily_sales=daily_sales,
                           employee_ids=employee_ids, daily_total=daily_total,
                           total_sales=total_sales)


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
