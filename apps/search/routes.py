# apps/search/routes.py

from flask import Blueprint, request, render_template
from apps.employee.models import Employee
from apps.customer.models import Customer
from apps.product.models import Products
from apps.search import search_blueprint as blueprint


@blueprint.route('/search', methods=['GET'])
def universal_search():
    query = request.args.get('query')
    employees = Employee.query.filter(Employee.name.ilike(f'%{query}%')).all()
    customers = Customer.query.filter(Customer.name.ilike(f'%{query}%')).all()
    products = Products.query.filter(Products.name.ilike(f'%{query}%')).all()
    return render_template('search/results.html', query=query, employees=employees, customers=customers,
                           products=products)
