# models/role_model.py
class Role:
    def __init__(self, role_id, role_name, permissions):
        self.role_id = role_id
        self.role_name = role_name
        self.permissions = permissions
    
    @classmethod
    def get_all_roles(cls):
        roles_data = [
            (1, "Administrator", "Full access (manage users, edit/delete data)"),
            (2, "Investor", "View country profiles, charts, exports, production"),
            (3, "Researcher", "View/export mineral & country data, add insights")
        ]
        
        roles = []
        for data in roles_data:
            role = cls(*data)
            roles.append(role)
        
        return roles
    
    @classmethod
    def get_role_by_id(cls, role_id):
        roles = cls.get_all_roles()
        for role in roles:
            if role.role_id == role_id:
                return role
        return None
    
    @classmethod
    def get_permissions(cls, role_name):
        roles = cls.get_all_roles()
        for role in roles:
            if role.role_name == role_name:
                return role.permissions
        return "No permissions"