# apps/employee/routes.py

from flask import request, jsonify, render_template, redirect, url_for, flash
from apps import db
from apps.employee.models import Employee
from apps.employee import blueprint
from datetime import datetime

employee_blueprint = blueprint


@employee_blueprint.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return render_template('employee/employee_list.html', employees=employees)


@employee_blueprint.route('/employee', methods=['POST'])
def create_employee():
    data = request.form
    new_employee = Employee(
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        position=data['position'],
        hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
    )
    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for('employee_blueprint.get_employees'))


@blueprint.route('/<int:employee_id>/', methods=['GET'])
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee/edit_employee.html', employee=employee)


@blueprint.route('/<int:employee_id>/edit', methods=['POST'])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee.name = request.form['name']
    employee.phone = request.form['phone']
    employee.email = request.form['email']
    employee.position = request.form['position']
    employee.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()  # Convert to date object
    db.session.commit()
    flash('Employee updated successfully', 'success')
    return redirect(url_for('employee_blueprint.get_employees'))


@employee_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.__repr__())


@employee_blueprint.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204
