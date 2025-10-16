# app.py
from flask import Flask, url_for
from config import SECRET_KEY
from models.user_model import init_user_file
from routes.auth_routes import auth_bp
from routes.home_routes import home_bp
from routes.mineral_routes import minerals_bp
from routes.stats_routes import stats_bp
from routes.map_routes import map_bp
from routes.country_routes import country_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize data files
init_user_file()
# Remove the Country.init_countries_file() line since we're using hardcoded data

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(minerals_bp, url_prefix="/minerals")
app.register_blueprint(stats_bp, url_prefix="/stats")
app.register_blueprint(map_bp, url_prefix="/map")
app.register_blueprint(country_bp, url_prefix="/countries")
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)