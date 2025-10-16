# models/user_model.py
import csv
import os

USER_FILE = 'users.csv'

def init_user_file():
    """Initialize with your original structure"""
    if not os.path.exists(USER_FILE):
        # Create file with your original structure
        with open(USER_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['UserID', 'Username', 'PasswordHash', 'RoleID', 'Email'])
            writer.writerow([1, 'admin01', 'hash123', 1, 'admin@miningapp.com'])
            writer.writerow([2, 'investor01', 'hash456', 2, 'invest@miningapp.com'])
            writer.writerow([3, 'research01', 'hash789', 3, 'research@univ.edu'])
        print("✅ Created users.csv with your original structure")
    else:
        print("✅ users.csv exists with your data")

def get_user(username):
    """Get user by Username (capital U)"""
    if not os.path.exists(USER_FILE):
        return None
    
    with open(USER_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username:  # Capital U
                return row
    return None

def create_user(username, password, role_id=3):
    """Create a new user - using your structure"""
    if get_user(username):
        return False
    
    # Get next UserID
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            reader = csv.DictReader(file)
            users = list(reader)
    
    next_id = len(users) + 1
    
    with open(USER_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([next_id, username, password, role_id, f'{username}@miningapp.com'])
    return True

def get_user_role(username):
    """Get user's role object - using RoleID (capital R)"""
    user = get_user(username)
    if user and 'RoleID' in user:  # Capital R
        from models.role_model import Role
        try:
            return Role.get_role_by_id(int(user['RoleID']))
        except:
            return None
    return None