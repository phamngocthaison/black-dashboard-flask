
from apps import db
from apps.sale.models import SaleOrder

class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    @property
    def total_order_amount(self):
        total = db.session.query(db.func.sum(SaleOrder.total_amount)).filter(SaleOrder.customer_id == self.customer_id).scalar()
        return total if total else 0.0

    def __repr__(self):
        return f'<Customer {self.name}>'