# routes/country_routes.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from models.country_model import Country
from auth_decorators import login_required, admin_required

country_bp = Blueprint('country', __name__)

@country_bp.route('/')
@login_required
def countries():
    """Display all countries"""
    all_countries = Country.get_all_countries()
    return render_template('countries.html', countries=all_countries)

@country_bp.route('/<int:country_id>')
@login_required
def country_profile(country_id):
    """Display detailed profile for a specific country"""
    country = Country.get_country_by_id(country_id)
    if country:
        mining_contribution = (country.mining_revenue_billion_usd / country.gdp_billion_usd) * 100
        return render_template('country_profile.html', 
                             country=country, 
                             mining_contribution=mining_contribution)
    else:
        flash('Country not found!', 'error')
        return redirect(url_for('country.countries'))

@country_bp.route('/<int:country_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_country(country_id):
    """Edit country data - ADMIN ONLY"""
    print(f"🔧 Edit country route called for ID: {country_id}")
    
    country = Country.get_country_by_id(country_id)
    
    if not country:
        flash('❌ Country not found!', 'error')
        return redirect(url_for('country.countries'))
    
    if request.method == 'POST':
        print("📝 Form submitted with data:", request.form)
        
        try:
            country_name = request.form.get('country_name', '').strip()
            gdp_str = request.form.get('gdp_billion_usd', '0')
            mining_revenue_str = request.form.get('mining_revenue_billion_usd', '0')
            key_projects = request.form.get('key_projects', '').strip()
            
            # Validate required fields
            if not country_name:
                flash('❌ Country name is required!', 'error')
                return render_template('edit_country.html', country=country)
            
            # Convert to float with error handling
            try:
                gdp = float(gdp_str)
            except ValueError:
                flash('❌ Please enter a valid number for GDP!', 'error')
                return render_template('edit_country.html', country=country)
            
            try:
                mining_revenue = float(mining_revenue_str)
            except ValueError:
                flash('❌ Please enter a valid number for Mining Revenue!', 'error')
                return render_template('edit_country.html', country=country)
            
            # Validate positive numbers
            if gdp < 0 or mining_revenue < 0:
                flash('❌ GDP and Mining Revenue must be positive numbers!', 'error')
                return render_template('edit_country.html', country=country)
            
            print(f"✅ Validated data - Name: {country_name}, GDP: {gdp}, Revenue: {mining_revenue}")
            
            # Update country data
            success = Country.update_country(country_id, country_name, gdp, mining_revenue, key_projects)
            
            if success:
                flash(f'✅ {country_name} data updated successfully!', 'success')
                # Update the displayed country object
                country.country_name = country_name
                country.gdp_billion_usd = gdp
                country.mining_revenue_billion_usd = mining_revenue
                country.key_projects = key_projects
            else:
                flash('❌ Failed to update country data in database!', 'error')
                
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            flash(f'❌ Unexpected error: {str(e)}', 'error')
    
    return render_template('edit_country.html', country=country)

@country_bp.route('/api/countries')
@login_required
def api_countries():
    """API endpoint to get all countries data"""
    countries = Country.get_all_countries()
    countries_data = []
    for country in countries:
        countries_data.append({
            'id': country.country_id,
            'name': country.country_name,
            'gdp': country.gdp_billion_usd,
            'mining_revenue': country.mining_revenue_billion_usd,
            'key_projects': country.key_projects,
            'contribution_percent': (country.mining_revenue_billion_usd / country.gdp_billion_usd) * 100
        })
    return jsonify(countries_data)

@country_bp.route('/api/countries/<int:country_id>')
@login_required
def api_country_profile(country_id):
    """API endpoint to get specific country data"""
    country = Country.get_country_by_id(country_id)
    if country:
        country_data = {
            'id': country.country_id,
            'name': country.country_name,
            'gdp': country.gdp_billion_usd,
            'mining_revenue': country.mining_revenue_billion_usd,
            'key_projects': country.key_projects,
            'contribution_percent': (country.mining_revenue_billion_usd / country.gdp_billion_usd) * 100
        }
        return jsonify(country_data)
    else:
        return jsonify({'error': 'Country not found'}), 404

# DEBUG AND TEST ROUTES
@country_bp.route('/debug')
@admin_required
def debug_countries():
    """Debug route to see country data"""
    countries = Country.get_all_countries()
    
    debug_info = []
    for country in countries:
        debug_info.append({
            'id': country.country_id,
            'name': country.country_name,
            'gdp': country.gdp_billion_usd,
            'revenue': country.mining_revenue_billion_usd,
            'projects': country.key_projects
        })
    
    # Return as HTML for easy viewing
    html_output = "<h1>Country Debug Info</h1>"
    for country in debug_info:
        html_output += f"""
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
            <h3>ID: {country['id']} - {country['name']}</h3>
            <p>GDP: ${country['gdp']}B | Revenue: ${country['revenue']}B</p>
            <p>Projects: {country['projects']}</p>
            <a href="/countries/{country['id']}/edit">Edit This Country</a>
        </div>
        """
    return html_output

@country_bp.route('/test-edit/<int:country_id>')
@admin_required
def test_edit(country_id):
    """Test if edit page loads"""
    country = Country.get_country_by_id(country_id)
    if country:
        return f"""
        <div style="padding: 20px; background: #e8f5e8; border: 2px solid green;">
            <h2>✅ Edit Test Successful!</h2>
            <p>Country: {country.country_name} (ID: {country.country_id})</p>
            <p>GDP: ${country.gdp_billion_usd}B</p>
            <p>Mining Revenue: ${country.mining_revenue_billion_usd}B</p>
            <a href="/countries/{country_id}/edit" style="background: blue; color: white; padding: 10px; text-decoration: none;">
                Go to Edit Page
            </a>
        </div>
        """
    else:
        return f"""
        <div style="padding: 20px; background: #ffe8e8; border: 2px solid red;">
            <h2>❌ Edit Test Failed!</h2>
            <p>Country with ID {country_id} not found in database.</p>
            <p>Available countries:</p>
            <ul>
        """ + ''.join([f"<li>ID: {c.country_id} - {c.country_name}</li>" for c in Country.get_all_countries()]) + """
            </ul>
        </div>
        """

@country_bp.route('/test-all-countries')
@login_required
def test_all_countries():
    """Test route to see all countries and their IDs"""
    countries = Country.get_all_countries()
    
    html = """
    <html>
    <head>
        <title>Country IDs Test</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .country { border: 1px solid #ddd; padding: 15px; margin: 10px; border-radius: 5px; }
            .country-id { font-weight: bold; color: #333; }
            .edit-link { background: #007bff; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>All Countries and Their IDs</h1>
    """
    
    for country in countries:
        html += f"""
        <div class="country">
            <span class="country-id">ID: {country.country_id}</span>
            <h3>{country.country_name}</h3>
            <p>GDP: ${country.gdp_billion_usd}B | Mining Revenue: ${country.mining_revenue_billion_usd}B</p>
            <a class="edit-link" href="/countries/{country.country_id}/edit">Edit This Country</a>
            <a class="edit-link" style="background: #28a745;" href="/countries/{country.country_id}">View Profile</a>
        </div>
        """
    
    html += "</body></html>"
    return html

# Health check route
@country_bp.route('/health')
def health_check():
    """Health check for country routes"""
    countries = Country.get_all_countries()
    return jsonify({
        'status': 'healthy',
        'total_countries': len(countries),
        'countries': [c.country_name for c in countries]
    })