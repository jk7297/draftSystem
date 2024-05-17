# from flask import Flask, request, render_template, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy
# import os

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define a User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# # Create the database 
# @app.before_first_request
# def create_tables():
#     db.create_all()

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         user_name = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         new_user = User(user_name=user_name, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful! Please login.')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# # TO-DO: Additional routes to interact with the database
# if __name__ == '__main__':
#     app.run(debug=True)
