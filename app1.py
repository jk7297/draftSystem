#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, url_for, session, flash
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from main import get_recommendations

app = Flask(__name__)
app.secret_key = 'secret_key'  # TO-DO: Change this to a random secret key in production

# Load the data set
data = pd.read_csv('spotify_data/train.csv')
data = data.sample(frac=0.05, random_state=1)

# Normalize the data
def normalize_data(df):
    df_numeric = df.select_dtypes(include=[np.number])
    return (df_numeric - df_numeric.min()) / (df_numeric.max() - df_numeric.min())

norm_data = normalize_data(data)
cosine_similarity_df = pd.DataFrame(cosine_similarity(norm_data), index=data.index, columns=data.index)

# -----------------------  GENERATE A USER -------------------------

# Initialize user data
user_data = pd.DataFrame(columns=['user_id', 'user_name', 'user_email', 'user_password'])

# Function to generate a unique user ID
def generate_unique_user_id(user_data):
    while True:
        user_id = np.random.randint(100000, 999999)
        if user_id not in user_data['user_id'].values:
            return user_id

# Function to sign up a new user
def user_signup(user_data, user_name, user_email, user_password):
    user_id = generate_unique_user_id(user_data)
    new_user = pd.DataFrame({'user_id': [user_id], 'user_name': [user_name], 'user_email': [user_email], 'user_password': [user_password]})
    user_data = pd.concat([user_data, new_user], ignore_index=True)
    return user_data

# Function to log in a user
def user_login(user_data, user_email, user_password):
    user = user_data[(user_data['user_email'] == user_email) & (user_data['user_password'] == user_password)]
    return user if not user.empty else None

# ----------------------- USER LOGIN PROCEDURE -------------------------

@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return render_template('home.html')
        #return redirect(url_for('home'))
        #return f"Welcome {session['user_name']}!"  # Simple welcome message or redirect to a profile/dashboard page; profile.html
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_data
    # Check if the form was submitted
    if request.method == 'POST':
        # Retrieve user info
        user_email = request.form['email']
        user_password = request.form['password']
        user = user_login(user_data, user_email, user_password)
        # If authentication is succesful, store user info in a session
        if user is not None:
            session['user_id'] = user['user_id'].values[0]
            session['user_name'] = user['user_name'].values[0]
            # Redirect to homepage upon successful login
            return redirect(url_for('index'))
        else:
            flash('Invalid login credentials!')
    # Display the login page/form
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global user_data
    # Check if the registration form was submitted
    if request.method == 'POST':
        # Retrieve new user info
        user_name = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        # Register the new user
        user_data = user_signup(user_data, user_name, user_email, user_password)
        flash('Registration successful! Please login.')
        # After Registration, redirect the user to login
        return redirect(url_for('login'))
    # Display the registration form
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Clear user's session 
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.')
    # Redirect to login for a new session
    return redirect(url_for('login'))

# ----------------------- SONG RATING PROCEDURE -------------------------

# Initialize rating data
ratings_data = pd.DataFrame(columns=['user_id', 'song_index', 'rating'])

# Function to get 5 random songs
def get_random_songs(data, num_songs=5):
    return data.sample(n=num_songs)

def rate_song(user_id, song_index, rating, ratings_data):
    new_rating = pd.DataFrame({'user_id': [user_id], 'song_index': [song_index], 'rating': [rating]})
    ratings_data = pd.concat([ratings_data, new_rating], ignore_index=True)
    print("Song rated successfully!")
    return ratings_data

def search_song(song_name, data):
    search_results = data[data['name'].str.contains(song_name, case=False)]
    if search_results.empty:
        print("No matching songs found.")
    else:
        print("Matching songs found:")
        print(search_results[['name', ]])

@app.route('/rate_songs', methods=['GET', 'POST'])
def rate_songs():
    # Ensure that the user is logged in
    if 'user_id' not in session:
        flash("You need to login first!")
        return redirect(url_for('login'))
    # Handle the form submission for rating songs
    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('rating-'):
                song_index = int(key.split('-')[1])
                rating = int(value)
                # Update the global rating data
                global ratings_data
                ratings_data = rate_song(session['user_id'], song_index, rating, ratings_data)

        flash('Thank you for rating the songs!')
        # Redirect the user to display the songs recommended for them
        return redirect(url_for('show_recommendations'))
    
    # Get 5 random songs to display to collect ratings
    random_songs = get_random_songs(data)
    return render_template('rating.html', songs=random_songs)

@app.route('/show_recommendations')
def show_recommendations():
    if 'user_id' not in session:
        flash("Please login to view recommendations.")
        return redirect(url_for('login'))

    user_ratings = ratings_data[ratings_data['user_id'] == session['user_id']]
    if user_ratings.empty:
        return "You need to rate some songs first."

    # Find the top-rated song for simplicity
    top_rated_index = user_ratings.loc[user_ratings['rating'].idxmax(), 'song_index']
    top_rated_song = data.loc[top_rated_index, 'name']

    # Fetch recommendations
    recommendations = get_recommendations(top_rated_song, cosine_similarity_df, data)
    return render_template('recommendations.html', recommendations=recommendations, song_name=top_rated_song)

if __name__ == '__main__':
    app.run(debug=True)