#!/usr/bin/env python3
# app.py - USING SPOTIFY API

from flask import Flask, request, render_template, redirect, url_for, session, flash
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# from main import get_recommendations
from api import get_token, search_for_artist, get_songs_by_artists, get_playlist_tracks, get_recommendations, fetch_song_features

app = Flask(__name__)
app.secret_key = 'secret_key'  # TO-DO: Change this to a random secret key in production

# -----------------------  GENERATE A USER -------------------------

# TO-DO: UPDATE TO PERMANANT DATABASE

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

# TO-DO: UPDATE TO PERMANANT DATABASE

@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return render_template('home.html')
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

def rate_song(user_id, spotify_track_id, rating, ratings_data):
    new_rating = pd.DataFrame({'user_id': [user_id], 'spotify_track_id': [spotify_track_id], 'rating': [rating]})
    ratings_data = pd.concat([ratings_data, new_rating], ignore_index=True)
    return ratings_data

@app.route('/rate_songs', methods=['GET', 'POST'])
def rate_songs():
    if 'user_id' not in session:
        flash("You need to login first!")
        return redirect(url_for('login'))

    token = get_token()
    # token = session.get('spotify_token')
    # if not token:
    #     flash("Spotify authentication needed.")
    #     return redirect(url_for('login'))

    if request.method == 'POST':
       # Handle rating submission
        for key, value in request.form.items():
            if key.startswith('rating-'):
                song_index = key.split('-')[1]
                rating = int(value)
                # Update the global rating data
                global ratings_data
                ratings_data = rate_song(session['user_id'], song_index, rating, ratings_data)

        flash('Thank you for rating the songs!')
        # Redirect the user to display the songs recommended for them
        return redirect(url_for('show_recommendations'))

    # Spotify playlist ID for a trending playlist like Global Top 50
    playlist_id = '37i9dQZEVXbMDoHDwVN2tF'
    trending_songs = get_playlist_tracks(token, playlist_id)

    # Limit to the top 10 songs
    top_tracks = trending_songs[:10]

    return render_template('rating.html', songs=top_tracks)

@app.route('/show_recommendations')
def show_recommendations():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login to view recommendations.")
        return redirect(url_for('login'))

    # Fetch user's highest rated song or a random one for demo purposes
    top_rated_song = ratings_data[ratings_data['user_id'] == user_id].sort_values(by='rating', ascending=False).iloc[0]['spotify_track_id']
    # TO-DO: need to update either get_recommendations or get metadata from spotify API
    recommendations = get_recommendations(top_rated_song, 5)
    songs_info = [fetch_song_features(get_token(), track_id) for track_id in recommendations]

    return render_template('recommendations.html', songs=songs_info)

# ----------------------- SEARCHING PROCEDURE -------------------------

# BUGGY: need to implement search results display page + update functionality
def search_song(song_name, artist_name, data):
    search_results = data[data['name'].str.contains(song_name, case=False) & (data['artists'].str.contains(artist_name, case=False))]
    if search_results.empty:
        print("No matching songs found.")
    else:
        print("Matching songs found:")
        print(search_results[['name', ]])
    
# @app.route('/search_page')
# def search_page():
#     return render_template('search_page.html')

@app.route('/search_page', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        song_name = request.form['song_name']
        artist_name = request.form['artist_name']
        token = get_token()
        # Assuming artist_name is used for search; modify as needed for songs
        artist_info = search_for_artist(token, artist_name)
        if artist_info:
            artist_id = artist_info['id']
            songs = get_songs_by_artists(token, artist_id)
            return render_template('search_results.html', songs=songs, artist_name=artist_name)
        else:
            flash('No results found.')
            return render_template('search_page.html', error='No results found.')
    return render_template('search_page.html')

# def search_results():
#     song_name = request.form['song_name']
#     artist_name = request.form['artist_name']
#     # To-do: search logic for API
#     results = search_song(song_name, artist_name, data)
#     # To-do: display search results
#     return render_template('search_page.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)


