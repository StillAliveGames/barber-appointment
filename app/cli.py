import click
from flask.cli import with_appcontext
from app import db
from app.models import Role, Permission, User

@click.command('init-roles')
@with_appcontext
def init_roles():
    """Create default roles and permissions"""
    permissions = [
        'create_appointment', 'view_own_appointments', 'cancel_own_appointment',
        'view_all_appointments', 'edit_appointment', 'delete_appointment',
        'manage_users', 'manage_roles', 'manage_masters', 'manage_services'
    ]
    for perm_name in permissions:
        if not Permission.query.filter_by(name=perm_name).first():
            db.session.add(Permission(name=perm_name))
    db.session.commit()

    roles_data = {
        'client': ['create_appointment', 'view_own_appointments', 'cancel_own_appointment'],
        'master': ['view_own_appointments', 'edit_appointment'],
        'admin': permissions
    }
    for role_name, perms in roles_data.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
        for perm_name in perms:
            perm = Permission.query.filter_by(name=perm_name).first()
            if perm and perm not in role.permissions:
                role.permissions.append(perm)
    db.session.commit()
    print("Roles and permissions created.")

@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(email, password):
    """Create an admin user"""
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        print("Run init-roles first.")
        return
    user = User(username='admin', email=email)
    user.set_password(password)
    user.roles.append(admin_role)
    db.session.add(user)
    db.session.commit()
    print(f"Admin {email} created.")

def init_app(app):
    app.cli.add_command(init_roles)
    app.cli.add_command(create_admin)