# auth_decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.auth_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.auth_login'))
        
        if session.get('role') != 'Administrator':
            flash('Administrator access required for this page.', 'error')
            return redirect(url_for('home.home'))
        
        return f(*args, **kwargs)
    return decorated_function

# For now, remove investor_required and researcher_required to test basic functionality