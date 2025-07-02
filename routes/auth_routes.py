from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import mongo 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists.')
            return redirect('/register')

        user_id = mongo.db.users.insert_one({'username': username, 'password': password})
        user = User({'_id': user_id, 'username': username})
        login_user(user)
        return redirect('/')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username =request.form['username']
        password = request.form['password']
        user_data = mongo.db.users.find_one({'username': username})

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
