from flask import Blueprint,render_template,redirect,url_for,request,flash, current_app, jsonify
from . import login_manager,db
# from werkzeug.security import generate_password_hash , check_password_hash
from .models import Admin,Order,OrderLine,Item
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET'])
def login():
    return render_template("login.html")


@auth.route('/login_submission',methods=['POST'])
def login_submission():
    Apass = request.form.get('typePasswordX')

    admin = Admin.query.filter_by(Password=Apass).first()

    if admin :
        flash('Logged successfully', category='success')
        out = login_user(admin,remember=True)
        flash(f'in line 21, {out}', category='warn') 
        current_app.logger.error(f'LINE25 -- Loggin{out}')
        try:
            print("meshan allah")
            return redirect(url_for('views.admin'), code=302)

            # return render_template("login.html",user=current_user)
        except:
            flash(f'in line 29 render error, {out}', category='warn') 
            
    flash(f'incorrect password', category='error') 
            
    
            
    return redirect(url_for('auth.login'), code=302)



@auth.route('/test_login')
def test_login():
    return jsonify({
        "current_user": str(current_user),
        "is_authenticated": current_user.is_authenticated
    })


@auth.route('/test_login_required')
@login_required
def test_login_required():
    return jsonify({
        "current_users": str(current_user),
        "is_authenticated": current_user.is_authenticated
    })
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.mainHome'))    

@login_manager.unauthorized_handler
def unauthorized():
    flash('unauthorized','error')
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(id):
    
    current_app.logger.error(f">>>>> LOADING UER ID: {id}")
    
    user = Admin.query.get(int(id))
    
    current_app.logger.error(f">>>>> USER: {user}")
    
    return user
