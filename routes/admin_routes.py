# routes/admin_routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from auth_decorators import admin_required
import csv
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@admin_required
def admin_panel():
    """Admin dashboard - ONLY Administrators"""
    # Count users
    user_count = 0
    if os.path.exists('users.csv'):
        with open('users.csv', 'r') as file:
            reader = csv.DictReader(file)
            user_count = sum(1 for row in reader)
    
    # Count countries
    from models.country_model import Country
    countries = Country.get_all_countries()
    country_count = len(countries)
    
    return render_template('admin_panel.html', 
                         user_count=user_count, 
                         country_count=country_count)

@admin_bp.route('/users')
@admin_required
def manage_users():
    """Manage users - ONLY Administrators"""
    users = []
    if os.path.exists('users.csv'):
        with open('users.csv', 'r') as file:
            reader = csv.DictReader(file)
            users = list(reader)
    
    from models.role_model import Role
    roles = Role.get_all_roles()
    
    return render_template('manage_users.html', users=users, roles=roles)

@admin_bp.route('/data')
@admin_required
def data_management():
    """Data management - ONLY Administrators"""
    from models.country_model import Country
    countries = Country.get_all_countries()
    
    return render_template('data_management.html', countries=countries)