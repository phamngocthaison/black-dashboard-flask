# apps/sale/models.py

from apps import db


class SaleOrder(db.Model):
    __tablename__ = 'sale_orders'

    id = db.Column(db.Integer, primary_key=True)
    # customer_name = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id', name='fk_sale_orders_customers'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('sales', lazy=True))

    def __repr__(self):
        return f'<SaleOrder {self.id}>'
