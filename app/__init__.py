from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

# Import blueprints
from .blueprints.customers import customers
from .blueprints.rental_records import rental_records
from .blueprints.tractors import tractors

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable

# Register Blueprints
app.register_blueprint(customers, url_prefix='/customers')
app.register_blueprint(rental_records, url_prefix='/rental_records')
app.register_blueprint(tractors, url_prefix='/tractors')

from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)
