from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
from os import path
from sqlalchemy.sql import text 
import stripe

login_manager= LoginManager()
db = SQLAlchemy()
DB_Name = "database.db"
# API-KEY = 'sk_test_51LxEOKFFl6SDYKySskA7EX31yodhMBrFddsIoMeHYTQKHZhgJ59UHbgp7rtJ9w7WFGFMiHAm0dDhh7hEogKhCJR500PzcRm9p9'

def create_app():
    app = Flask(__name__)
    stripe.api_key = 'sk_test_51LxEOKFFl6SDYKySskA7EX31yodhMBrFddsIoMeHYTQKHZhgJ59UHbgp7rtJ9w7WFGFMiHAm0dDhh7hEogKhCJR500PzcRm9p9'
    app.config['SECRET_KEY'] = 'kfhsjhfaflk'
    app.config['SQLALCHEMY_DATABASE_URI'] = F'sqlite:///{DB_Name}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')

    from .models import Admin,Order,OrderLine,Item

    create_database(app)

    login_manager.login_views = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def loud_user(id):
        return Admin.query.get(int(id))


    return app

    

def create_database(app):
    if not path.exists('website/'+DB_Name):
        db.create_all(app=app)
        
        sql_file = open('website/SQL.txt','r')

        # Create an empty command string
        sql_command = ''
        
        # Iterate over all lines in the sql file
        for line in sql_file:
            # Ignore commented lines
            if not line.startswith('--') and line.strip('\n'):
                # Append line to the command string
                sql_command += line.strip('\n')
        
                # If the command string ends with ';', it is a full statement
                if sql_command.endswith(';'):
                    # Try to execute statement and commit it
                    print(sql_command)
                    try:
                        sql = text(sql_command)
                        # db.engine.execute(sql)
                        db.session.execute(sql)
                        print("meaw")
                        db.session.commit()
        
                    # Assert in case of error
                    except:
                        print('Ops')
        
                    # Finally, clear command string
                    finally:
                        sql_command = ''




        print('Created Database')    