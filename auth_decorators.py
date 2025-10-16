# auth_decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect('/login')  # Use direct path instead of url_for
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect('/login')  # Use direct path
        
        # For now, allow any logged-in user to access admin
        # You can enhance this later to check specific admin roles
        return f(*args, **kwargs)
    return decorated_function