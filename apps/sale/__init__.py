# apps/sale/__init__.py

from flask import Blueprint

blueprint = Blueprint(
    'sale_blueprint',
    __name__,
    url_prefix='/sale'
)