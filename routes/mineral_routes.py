# routes/mineral_routes.py
from flask import Blueprint, render_template
from auth_decorators import login_required
import csv
import os

minerals_bp = Blueprint('minerals', __name__)

@minerals_bp.route('/')
@login_required
def index():
    """Display minerals data"""
    minerals = []
    
    # Read minerals from CSV
    if os.path.exists('minerals.csv'):
        with open('minerals.csv', 'r') as file:
            reader = csv.DictReader(file)
            minerals = list(reader)
    
    return render_template('minerals.html', minerals=minerals)
