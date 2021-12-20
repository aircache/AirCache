# Import base packages
from flask import current_app as app
# Import blueprints
from ..proxy import proxy
# Append blueprints
app.register_blueprint(proxy)
