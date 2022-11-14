from flask import Blueprint,render_template,redirect,url_for,request,flash
from . import login_manager,db
from werkzeug.security import generate_password_hash , check_password_hash
from .models import Admin,Order,OrderLine,Item
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        Apass = request.form.get('typePasswordX')

        admin = Admin.query.filter_by(Password=Apass).first()

        if admin :
            flash('Logged successfully', category='success')
            login_user(admin,remember=True)
            return redirect(url_for('views.admin'))
        else :
            flash('wrong password', category='error') 
      
    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.mainHome'))    

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

