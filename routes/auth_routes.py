# routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import get_user, create_user
from models.role_model import Role

# Blueprint definition MUST come first
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form.get('role_id', 3)
        
        if create_user(username, password, role_id):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.auth_login'))
        else:
            flash('Username already exists!', 'error')
    
    roles = Role.get_all_roles()
    return render_template('register.html', roles=roles)

@auth_bp.route('/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user(username)
        if user and user['PasswordHash'] == password:
            session['user_id'] = username
            user_role = Role.get_role_by_id(int(user['RoleID']))
            session['role'] = user_role.role_name if user_role else 'Researcher'
            
            # DEBUG: Print login info
            print(f"✅ LOGIN SUCCESS: {username} as {session['role']}")
            
            flash('Login successful!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def auth_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.auth_login'))