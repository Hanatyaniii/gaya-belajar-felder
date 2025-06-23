from flask_bcrypt import generate_password_hash
from app import app, db  
from models import Users  

def create_admin():
    admin_username = 'admin'
    admin_email = 'admin@gmail.com'
    admin_password = generate_password_hash('admin123')
    new_admin = Users(username=admin_username, email=admin_email, password=admin_password, is_admin=True)
    with app.app_context():
        db.session.add(new_admin)
        db.session.commit()
        print('Admin user created.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
