# routes/home_routes.py
from flask import Blueprint, render_template, session
from auth_decorators import login_required
from models.role_model import Role

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    """Home page with dashboard and role-based features"""
    username = session.get('user_id', 'Guest')
    userrole = session.get('role', 'Guest')
    
    # Get user's permissions
    permissions = Role.get_permissions(userrole)
    
    return render_template('home.html', 
                         username=username, 
                         userrole=userrole,
                         permissions=permissions)