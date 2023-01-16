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
    # app.config['SQLALCHEMY_DATABASE_URI'] = F'sqlite:///{DB_Name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = F'mysql+pymysql://root:N48wbaP5GGnNbdCH@mysql-94y3-4t9e.cy68rase44d2.us-west-2.rds.amazonaws.com:3306/KababDB'
    # app.config['SERVER_NAME'] = 'www.kfaddiction.com'
    # app.config['DOMAIN_NAME'] = 'www.kfaddiction.com'
    
    app.config['SESSION_COOKIE_DOMAIN'] = 'kfaddiction.com'


    db.init_app(app)
    
    import logging
    gunicorn_logger = logging.getLogger('gunicorn.access')
    
    app.logger.handlers.extend(gunicorn_logger)

    app.logger.setLevel(logging.DEBUG)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')

    from .models import Admin,Order,OrderLine,Item

    # create_database(app, db)
    # create_local_database(app, db)


    # InitilDataBase()

    login_manager.login_views = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def loud_user(id):
        return Admin.query.get(int(id))


    return app

    
def create_local_database(app, db):
    if not path.exists('website/'+DB_Name):
        with app.app_context():
            db.create_all()
        print('Created Database')  

def create_database(app, db):
    # if not path.exists('website/'+DB_Name):
    with app.app_context():
        db.create_all()
    print('Created Database')  

# def InitilDataBase():
#     sql_command = 'INSERT INTO admin VALUES(1,"admin");'

#     try:
#         sql = text(sql_command)
#         # db.engine.execute(sql)
#         print(sql)
#         db.session.execute(sql)
#         db.session.commit()
#     # Assert in case of error
#     except Exception as e:
#         print (str(e),"oooooooooooooooooooooooooo")

    # sql_file = open('website/SQL.txt','r')

    # # Create an empty command string
    # sql_command = ''
    
    # # Iterate over all lines in the sql file
    # for line in sql_file:
    #     # Ignore commented lines
    #     if not line.startswith('--') and line.strip('\n'):
    #         # Append line to the command string
    #         sql_command += line.strip('\n')
    
    #         # If the command string ends with ';', it is a full statement
    #         if sql_command.endswith(';'):
    #             # Try to execute statement and commit it
    #             print(sql_command)
    #             try:
    #                 sql = text(sql_command)
    #                 # db.engine.execute(sql)
    #                 db.session.execute(sql)
    #                 print("meaw")
    #                 db.session.commit()
    
    #             # Assert in case of error
    #             except:
    #                 print('Ops')
    
    #             # Finally, clear command string
    #             finally:
    #                 sql_command = ''          