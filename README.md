### To do: 
JK (DevOps): 
1. Implement the deployment using spotify api + Flask 
- Look at this: https://github.com/hereismari/spotify-flask

SAH (MLOps): 
1. Integrate new features of lyrics into the dataset



# Spotify Rec Sys

This repository contains code for a music recommendation system using a content-based filtering approach, with the potential to incorporate user data and collaborative filtering techniques. Here's an overview of the project and how to use it:

#### Objective:
- Utilize song features to recommend similar songs based on content-based filtering techniques.
- Enable dynamic recommendations by incorporating user data.
- Explore hybrid models combining content-based and collaborative filtering methods for enhanced recommendations.

#### Data:
- The dataset used for this project is stored in `spotify_data/train.csv`, you can access it through the spotify challenge. I have attached the dataset as well.
- The data consists of song features and metadata.

#### Preprocessing:
- The data preprocessing steps include:
  - Normalizing the numerical features using min-max normalization.
  - Handling missing values.
  - Identifying and dropping highly correlated features.
  - Exploring clustering for unsupervised learning.

#### Recommendation:
- Computing cosine similarity between songs based on their features.
- Implementing collaborative filtering with cosine similarity.
- Providing recommendations based on user interactions and preferences.

#### User Interaction:
- Creating user profiles for personalized recommendations.
- Allowing users to sign up and log in.
- Enabling users to rate recommended songs and search for specific songs.

#### Usage:
- Run the provided scripts in a Python environment.
- Modify parameters and functions as needed for customization.
- Explore different recommendation strategies and user interactions.

#### Spotify API implementation - work in progress

- app.js file interacts with Spotify's Web API to manage music data and user preferences. 
- It begins by establishing authorization with a token, then uses async functions to fetch a user's top tracks and generate music recommendations. 
- These tracks are utilized to create and manage a Spotify playlist directly through the API, demonstrating the use of endpoints for fetching user details, creating playlists, and modifying playlist contents. 
- The script also includes an example of embedding a Spotify playlist into a web page using an iframe, enhancing user interaction by allowing direct music playback within the site. 
- Finally, it manages navigation flow with a redirection to a callback URL, typically used in authentication processes.


#### Note:
- This project is a work in progress and may be subject to updates and improvements.
- Feedback and contributions are welcome.

### Contributors:
- Syed Ali Haider
- Jasmeen Kaur
- Anasse Bari
