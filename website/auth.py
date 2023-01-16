from flask import Blueprint,render_template,redirect,url_for,request,flash, current_app
from . import login_manager,db
# from werkzeug.security import generate_password_hash , check_password_hash
from .models import Admin,Order,OrderLine,Item
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        Apass = request.form.get('typePasswordX')

        admin = Admin.query.filter_by(Password=Apass).first()
        
        flash(f'in line 16, {admin}', category='warn') 
        
        print(f'\n\n\nLINE16 {admin}')
        current_app.logger.error(f'LINE16 -- {admin}')

        if admin :
            flash('Logged successfully', category='success')
            out = login_user(admin,remember=True)
            flash(f'in line 21, {out}', category='warn') 
            current_app.logger.error(f'LINE25 -- {out}')
            return render_template("login.html",user=current_user)


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
    flash('unauthorized','error')
    return redirect(url_for('auth.login'))

