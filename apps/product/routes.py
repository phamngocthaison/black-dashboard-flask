# apps/product/routes.py

from flask import request, jsonify, render_template, redirect, url_for, flash
from apps import db
from apps.product.models import Products
from apps.product import blueprint

product_blueprint = blueprint


@product_blueprint.route('/products', methods=['GET'])
def get_products():
    products = Products.query.all()
    return render_template('product/product_list.html', products=products)


@product_blueprint.route('/product', methods=['POST'])
def create_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    stock = int(request.form['stock'])

    new_product = Products(name=name, description=description, price=price, stock=stock)
    db.session.add(new_product)
    db.session.commit()
    flash('Product created successfully!', 'success')
    return redirect(url_for('product_blueprint.get_products'))


@product_blueprint.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.get_or_404(product_id)
    return jsonify(product.__repr__())


@product_blueprint.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Products.query.get_or_404(product_id)
    product.name = data['name']
    product.description = data['description']
    product.price = float(data['price'])
    product.stock = int(data['stock'])
    db.session.commit()
    return jsonify(product.__repr__())


@product_blueprint.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
