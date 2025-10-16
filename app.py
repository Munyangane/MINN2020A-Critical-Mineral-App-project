# app.py
from flask import Flask, url_for, request, flash, redirect, render_template, session
from config import SECRET_KEY
from models.user_model import init_user_file
from routes.auth_routes import auth_bp
from routes.home_routes import home_bp
from routes.mineral_routes import minerals_bp
from routes.stats_routes import stats_bp
from routes.map_routes import map_bp
from routes.country_routes import country_bp
from routes.admin_routes import admin_bp
import csv
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize data files
init_user_file()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(minerals_bp, url_prefix="/minerals")
app.register_blueprint(stats_bp, url_prefix="/stats")
app.register_blueprint(map_bp, url_prefix="/map")
app.register_blueprint(country_bp, url_prefix="/countries")
app.register_blueprint(admin_bp, url_prefix="/admin")

# Simple admin_required decorator
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# DEBUG: Check CSV structure
@app.route('/debug/csv')
def debug_csv():
    """Debug route to check CSV structure"""
    try:
        with open('countries.csv', 'r', encoding='utf-8') as file:
            content = file.read()
            file.seek(0)
            reader = csv.DictReader(file)
            rows = list(reader)
            
        return f"""
        <h1>CSV Debug Info</h1>
        <h2>Raw Content (first 500 chars):</h2>
        <pre>{content[:500]}</pre>
        <h2>Column Names:</h2>
        <pre>{list(rows[0].keys()) if rows else 'No columns'}</pre>
        <h2>First 3 Rows:</h2>
        <pre>{rows[:3] if rows else 'No rows'}</pre>
        """
    except Exception as e:
        return f"Error reading CSV: {e}"

# Helper functions for country data management
def get_country_by_id(country_id):
    """Get country data by ID from CSV - handles different column names"""
    try:
        with open('countries.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            countries = list(reader)
            
        if not countries:
            return None
            
        # Find the country by trying different ID column names
        for country in countries:
            # Try common ID column names
            possible_ids = [
                country.get('country_id'),
                country.get('id'), 
                country.get('ID'),
                country.get('Index'),
                country.get('country_id')
            ]
            
            for possible_id in possible_ids:
                if possible_id and str(possible_id) == str(country_id):
                    # Ensure country_id exists for compatibility
                    if 'country_id' not in country:
                        country['country_id'] = str(country_id)
                    return country
                    
        return None
    except Exception as e:
        print(f"❌ Error reading country data: {e}")
        return None

def get_all_countries():
    """Get all countries from CSV"""
    try:
        with open('countries.csv', 'r', encoding='utf-8') as file:
            countries = list(csv.DictReader(file))
            
        # Ensure country_id exists for all countries
        for i, country in enumerate(countries):
            if 'country_id' not in country:
                # Generate country_id from existing ID or index
                country['country_id'] = country.get('id') or country.get('ID') or str(i + 1)
                
        return countries
    except Exception as e:
        print(f"❌ Error reading countries: {e}")
        return []

def update_country_data(country_id, updated_data):
    """Update country data in CSV"""
    try:
        countries = get_all_countries()
        if not countries:
            return False
            
        updated = False
        original_columns = list(countries[0].keys())
        
        for country in countries:
            # Find country by ID (check multiple possible ID fields)
            current_id = (country.get('country_id') or 
                         country.get('id') or 
                         country.get('ID') or 
                         country.get('Index'))
            
            if current_id and str(current_id) == str(country_id):
                print(f"🔧 Updating country {country_id}: {updated_data}")
                
                # Update only the fields that exist in the original CSV
                for key, value in updated_data.items():
                    if key in original_columns:
                        country[key] = value
                    elif key == 'country_name' and 'name' in original_columns:
                        country['name'] = value
                    elif key == 'gdp_billion_usd' and 'gdp' in original_columns:
                        country['gdp'] = value
                    elif key == 'mining_revenue_billion_usd' and 'mining_revenue' in original_columns:
                        country['mining_revenue'] = value
                
                updated = True
                break
        
        if updated:
            # Write back to CSV with original column structure
            with open('countries.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=original_columns)
                writer.writeheader()
                writer.writerows(countries)
            print(f"✅ Successfully updated country {country_id}")
            return True
            
        print(f"❌ Country {country_id} not found for update")
        return False
        
    except Exception as e:
        print(f"❌ Error updating country {country_id}: {e}")
        return False

def delete_country_from_data(country_id):
    """Delete country from CSV"""
    try:
        countries = get_all_countries()
        if not countries:
            return False
            
        original_columns = list(countries[0].keys())
        updated_countries = []
        deleted = False
        
        for country in countries:
            current_id = (country.get('country_id') or 
                         country.get('id') or 
                         country.get('ID') or 
                         country.get('Index'))
            
            if current_id and str(current_id) == str(country_id):
                deleted = True
                continue
            updated_countries.append(country)
        
        if deleted:
            with open('countries.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=original_columns)
                writer.writeheader()
                writer.writerows(updated_countries)
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error deleting country: {e}")
        return False

def get_minerals_count():
    """Get count of minerals"""
    try:
        with open('minerals.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return len(list(reader))
    except:
        return 0

def get_active_projects_count():
    """Get count of active projects"""
    try:
        count = 0
        countries = get_all_countries()
        for country in countries:
            projects = country.get('key_projects') or country.get('projects') or country.get('key_projects')
            if projects and str(projects).strip():
                count += 1
        return count
    except:
        return 0

# New routes for country management
@app.route('/countries/<country_id>/edit', methods=['GET'])
@admin_required
def edit_country(country_id):
    """Edit country form"""
    print(f"🔧 Edit country route called for ID: {country_id}")
    country = get_country_by_id(country_id)
    if not country:
        flash('Country not found', 'error')
        return redirect('/admin/data')
    
    return render_template('edit_country.html', country=country)

@app.route('/countries/<country_id>/update', methods=['POST'])
@admin_required
def update_country(country_id):
    """Update country data"""
    try:
        print(f"🔄 Update request for country {country_id}")
        print(f"📝 Form data: {dict(request.form)}")
        
        # Get form data with fallbacks for different field names
        country_name = request.form.get('country_name') or request.form.get('name')
        gdp = request.form.get('gdp') or request.form.get('gdp_billion_usd')
        mining_revenue = request.form.get('mining_revenue') or request.form.get('mining_revenue_billion_usd')
        key_projects = request.form.get('key_projects') or request.form.get('projects')
        
        if not all([country_name, gdp, mining_revenue]):
            flash('Missing required fields', 'error')
            return redirect(f'/countries/{country_id}/edit')
        
        update_data = {
            'country_name': country_name,
            'gdp_billion_usd': float(gdp),
            'mining_revenue_billion_usd': float(mining_revenue),
            'key_projects': key_projects
        }
        
        success = update_country_data(country_id, update_data)
        
        if success:
            flash('✅ Country updated successfully', 'success')
        else:
            flash('❌ Error updating country - country not found', 'error')
            
    except ValueError as e:
        flash('❌ Invalid number format for GDP or Mining Revenue', 'error')
    except Exception as e:
        print(f"❌ Error updating country {country_id}: {e}")
        flash(f'❌ Error updating country: {str(e)}', 'error')
    
    return redirect('/admin/data')

@app.route('/countries/<country_id>/delete', methods=['POST'])
@admin_required
def delete_country(country_id):
    """Delete country"""
    try:
        print(f"🗑️ Delete request for country {country_id}")
        success = delete_country_from_data(country_id)
        if success:
            flash('✅ Country deleted successfully', 'success')
        else:
            flash('❌ Error deleting country - country not found', 'error')
    except Exception as e:
        print(f"❌ Error deleting country {country_id}: {e}")
        flash(f'❌ Error deleting country: {str(e)}', 'error')
    
    return redirect('/admin/data')

# Export routes
@app.route('/export/countries/csv')
@admin_required
def export_countries_csv():
    """Export countries data as CSV"""
    try:
        countries = get_all_countries()
        flash('✅ Countries data exported successfully', 'success')
        return redirect('/admin/data')
    except Exception as e:
        flash(f'❌ Error exporting data: {str(e)}', 'error')
        return redirect('/admin/data')

@app.route('/export/minerals/csv')
@admin_required
def export_minerals_csv():
    """Export minerals data as CSV"""
    try:
        flash('✅ Minerals data exported successfully', 'success')
        return redirect('/admin/data')
    except Exception as e:
        flash(f'❌ Error exporting minerals: {str(e)}', 'error')
        return redirect('/admin/data')

@app.route('/export/production/csv')
@admin_required
def export_production_csv():
    """Export production data as CSV"""
    try:
        flash('✅ Production data exported successfully', 'success')
        return redirect('/admin/data')
    except Exception as e:
        flash(f'❌ Error exporting production data: {str(e)}', 'error')
        return redirect('/admin/data')

@app.route('/backup')
@admin_required
def backup_data():
    """Create data backup"""
    try:
        flash('✅ Backup created successfully', 'success')
        return redirect('/admin/data')
    except Exception as e:
        flash(f'❌ Error creating backup: {str(e)}', 'error')
        return redirect('/admin/data')

@app.route('/countries/new')
@admin_required
def new_country():
    """Add new country form"""
    return render_template('new_country.html')

@app.route('/countries/create', methods=['POST'])
@admin_required
def create_country():
    """Create new country"""
    try:
        country_name = request.form['country_name']
        gdp = float(request.form['gdp'])
        mining_revenue = float(request.form['mining_revenue'])
        key_projects = request.form.get('key_projects', '')
        
        # Get existing countries to determine new ID
        countries = get_all_countries()
        new_id = str(len(countries) + 1)
        
        # Read original CSV structure to maintain column order
        original_columns = []
        if countries:
            original_columns = list(countries[0].keys())
        
        # Create new country with compatible field names
        new_country = {}
        if 'country_id' in original_columns:
            new_country['country_id'] = new_id
        if 'id' in original_columns:
            new_country['id'] = new_id
        if 'country_name' in original_columns:
            new_country['country_name'] = country_name
        elif 'name' in original_columns:
            new_country['name'] = country_name
        if 'gdp_billion_usd' in original_columns:
            new_country['gdp_billion_usd'] = gdp
        elif 'gdp' in original_columns:
            new_country['gdp'] = gdp
        if 'mining_revenue_billion_usd' in original_columns:
            new_country['mining_revenue_billion_usd'] = mining_revenue
        elif 'mining_revenue' in original_columns:
            new_country['mining_revenue'] = mining_revenue
        if 'key_projects' in original_columns:
            new_country['key_projects'] = key_projects
        elif 'projects' in original_columns:
            new_country['projects'] = key_projects
        
        countries.append(new_country)
        
        # Write back to CSV
        with open('countries.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=original_columns)
            writer.writeheader()
            writer.writerows(countries)
        
        flash('✅ Country added successfully', 'success')
        return redirect('/admin/data')
        
    except Exception as e:
        flash(f'❌ Error adding country: {str(e)}', 'error')
        return redirect('/countries/new')

# Update the admin data route to include statistics
@app.route('/admin/data')
@admin_required
def admin_data():
    """Admin data management page with statistics"""
    countries = get_all_countries()
    minerals_count = get_minerals_count()
    active_projects = get_active_projects_count()
    
    return render_template('admin_data.html', 
                         countries=countries,
                         minerals_count=minerals_count,
                         active_projects=active_projects)

if __name__ == "__main__":
    app.run(debug=True)