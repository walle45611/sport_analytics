from flask import Flask  # ✅ 這一行不能少
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
 # 確保這行存在，並且路徑正確

# 下面這些不動
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.training import training_bp
    from app.routes.main import main_bp
    from app.routes.coach import coach_bp
    from app.routes.evaluation import evaluation_bp  # ✅ 新增評估表單
    
    


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(training_bp, url_prefix='/training')
    app.register_blueprint(main_bp)
    app.register_blueprint(coach_bp, url_prefix='/coach')
    app.register_blueprint(evaluation_bp, url_prefix='/evaluation')
   


    return app
