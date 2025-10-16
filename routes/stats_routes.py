# routes/stats_routes.py
from flask import Blueprint, render_template, jsonify
from auth_decorators import login_required
from models.country_model import Country

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/')
@login_required  # Only login required for now
def stats_dashboard():
    """Display production statistics"""
    countries = Country.get_all_countries()
    
    total_gdp = sum(country.gdp_billion_usd for country in countries)
    total_mining_revenue = sum(country.mining_revenue_billion_usd for country in countries)
    avg_contribution = (total_mining_revenue / total_gdp) * 100 if total_gdp > 0 else 0
    
    stats = {
        'total_countries': len(countries),
        'total_gdp': total_gdp,
        'total_mining_revenue': total_mining_revenue,
        'avg_contribution': avg_contribution
    }
    
    return render_template('stats.html', countries=countries, stats=stats)

@stats_bp.route('/api/production-data')
@login_required  # Only login required for now
def production_data():
    """API endpoint for production data"""
    countries = Country.get_all_countries()
    
    data = {
        'countries': [country.country_name for country in countries],
        'mining_revenue': [country.mining_revenue_billion_usd for country in countries],
        'gdp': [country.gdp_billion_usd for country in countries]
    }
    
    return jsonify(data)