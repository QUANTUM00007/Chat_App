from flask import Flask
from extensions import mongo, login_manager
from bson.objectid import ObjectId, InvalidId
from models import User
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chat_db'

mongo.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
    except (InvalidId, TypeError):
        return None

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
