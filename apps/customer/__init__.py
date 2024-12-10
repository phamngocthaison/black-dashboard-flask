# apps/sale/__init__.py

from flask import Blueprint

blueprint = Blueprint(
    'customer_blueprint',
    __name__,
    url_prefix='/customer'
)