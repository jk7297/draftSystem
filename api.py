#!/usr/bin/env python3
# api.py
import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
from main import calculate_similarity

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)

    if result.status_code != 200:
        print(f"Failed to fetch token: {result.status_code}")
        print(result.text)
        return None

    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_playlist_tracks(token, playlist_id):
    """ Fetch tracks from the specified playlist. """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    response = get(url, headers=headers)
    if response.status_code == 200:
        tracks = response.json()['items']
        return [item['track'] for item in tracks if item.get('track')] 
    else:
        print(f"Failed to fetch tracks: {response.status_code}")
        return []
    
def fetch_song_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    response = get(url, headers=headers)
    return response.json()

def get_recommendations(track_id, num_recommendations=5):
    token = get_token()
    features = fetch_song_features(token, track_id)
    # This is a placeholder function that should calculate similarity based on features
    similar_tracks = calculate_similarity(features, num_recommendations)
    return similar_tracks

token = get_token()
result = search_for_artist(token, "Billie")
artist_id = result["id"]
songs = get_songs_by_artists(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

# playlist_id = '37i9dQZEVXbMDoHDwVN2tF'
# trending_songs = get_playlist_tracks(token, playlist_id)

# for i, s in enumerate(trending_songs):
#     print(f"{i + 1}. {s['name']}")