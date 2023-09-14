from flask import Flask
from flask_mysqldb import MySQL

# from app import yourPyFileName
# from app import login,admin,logout
# from app import temporaryIndex

mysql = MySQL()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = 'group1-project1'

    # Configure mysql database
    app.config['MYSQL_HOST'] = 'JinkelaP.mysql.pythonanywhere-services.com'
    app.config['MYSQL_USER'] = 'JinkelaP'
    app.config['MYSQL_PASSWORD'] = 'vivian602'
    app.config['MYSQL_DB'] = 'JinkelaP$swimmingpool'

    app.config['MYSQL_PORT'] = 3306
    
    mysql.init_app(app) 

    from . import login,logout, temporaryIndex, adminDashboardFunc, instructorDashboardFunc, reg, memberDashboardFunc,addManyMembers,someFunctions
    # import the Blueprints
    app.register_blueprint(login.bp)
    app.register_blueprint(reg.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(temporaryIndex.bp)
    app.register_blueprint(adminDashboardFunc.bp)
    app.register_blueprint(memberDashboardFunc.bp)
    app.register_blueprint(instructorDashboardFunc.bp)
    app.register_blueprint(addManyMembers.bp)
    app.register_blueprint(someFunctions.bp)


    return app