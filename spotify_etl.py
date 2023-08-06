import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import datetime
from airflow.models import Variable
import psycopg2

client_id = Variable.get("SPOTIFY_CLIENT_ID")
client_secret = Variable.get("SPOTIFY_CLIENT_SECRET")


def run_spotify_etl():

    # get the client id and secret from airflow variables
    client_id = Variable.get("SPOTIFY_CLIENT_ID")
    client_secret = Variable.get("SPOTIFY_CLIENT_SECRET")

    # setup the SpotifyClientCredentials object
    client_credentials_manager = SpotifyClientCredentials(
        client_id = client_id,
        client_secret = client_secret)

    # authenticate with spotify using the new access token
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # get top 50 tracks for the Global Top 50 playlist
    playlist_id = '37i9dQZEVXbMDoHDwVN2tF' # Global Top 50 playlist ID
    results = sp.playlist(playlist_id)

    # Create a list to hold track data
    tracks = []

    # Loop through each track in the playlist, retrieve track details and store in list
    for item in results['tracks']['items']:
        track_data = item['track']
        tracks.append(track_data)

    # Convert track data list into a DataFrame
    results_df = pd.json_normalize(tracks)

    # Drop unnecessary columns
    keep_cols = ['artists', 'explicit', 'id', 'name', 'popularity', 'album.id', 'album.name', 'album.release_date', 'album.total_tracks']
    results_df = results_df[keep_cols]

    # Now we need to extract data from columns that contain a list of dictionaries
    # Define a function to extract the data
    def extract_artist_data(artist_list):
        # extract name
        artist_name = artist_list[0]['name']
        # extract id
        artist_id = artist_list[0]['id']
        
        # build a series with name and id for each row
        return pd.Series([artist_name, artist_id])

    # Apply the function in a vectorised operation
    # New columns artist_name and artist_id to fill -> get the data from the artists column -> apply the function to artists column
    # Note that .apply performs the function on each row
    results_df[['artist_name', 'artist_id']] = results_df['artists'].apply(extract_artist_data)

    # Now we can drop the artists column
    results = results_df.drop(columns = 'artists')
    del results_df

    # New columns
    audiofeature_cols = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo']

    # Get list of all song ids for batch processing
    song_ids = results['id'].tolist()

    # Get audio features for all songs
    audio_features_list = sp.audio_features(tracks = song_ids)

    # Convert to dataframe for easy manipulation
    audio_features_df = pd.DataFrame(audio_features_list)

    # Drop unwanted columns
    audiofeature_cols.append('id')
    audio_features_df = audio_features_df[audiofeature_cols]

    # Join dataframes
    results = results.merge(audio_features_df, on='id', how='left')
    del audio_features_df

    # Create rank for songs based on the order they appear in the playlist
    results['rank'] = results.index + 1

    # Convert from float to int
    results['rank'] = results['rank'].astype(int)

    # Get current date
    current_date = datetime.datetime.now().date()

    # Save csv to s3 bucket
    results.to_csv(f's3://spotify-user-data/spotify_data_{current_date}.csv', index=False)

run_spotify_etl()
