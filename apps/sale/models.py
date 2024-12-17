# apps/sale/models.py

from apps import db


class SaleOrder(db.Model):
    __tablename__ = 'sale_orders'

    id = db.Column(db.Integer, primary_key=True)
    # customer_name = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id', name='fk_sale_orders_customers'),
                            nullable=False)
    customer = db.relationship('Customer', backref=db.backref('sales', lazy=True))
    # order_details = db.relatiidonship('OrderDetails', backref='order_id', lazy=True)

    def __repr__(self):
        return f'<SaleOrder {self.id}>'


class OrderDetails(db.Model):
    __tablename__ = 'order_details'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sale_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    order = db.relationship('SaleOrder', backref=db.backref('order_details', lazy=True))
    product = db.relationship('Products', backref=db.backref('order_details', lazy=True))
