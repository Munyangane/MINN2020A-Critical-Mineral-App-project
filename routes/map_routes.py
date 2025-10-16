# routes/map_routes.py
from flask import Blueprint, render_template
from auth_decorators import login_required
from models.country_model import Country

map_bp = Blueprint('map', __name__)

@map_bp.route('/')
@login_required  # Only login required for now
def map_dashboard():
    """Display mineral map with country data"""
    countries = Country.get_all_countries()
    
    # Prepare data for the map
    map_data = []
    for country in countries:
        map_data.append({
            'name': country.country_name,
            'mining_revenue': country.mining_revenue_billion_usd,
            'gdp': country.gdp_billion_usd,
            'key_projects': country.key_projects,
            'contribution_percent': (country.mining_revenue_billion_usd / country.gdp_billion_usd) * 100
        })
    
    return render_template('maps.html', countries=map_data)