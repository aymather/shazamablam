from etc.ClientBase import ClientBase
import requests
import pandas as pd
import numpy as np
import time

db_string = 'postgresql+psycopg2://postgres:Wheninrome1;@database-1.couue7ynblpf.us-west-1.rds.amazonaws.com:5432/postgres'

client = ClientBase(db_string)

cities = pd.read_csv('./etc/cities.csv')

xdf = pd.DataFrame([[1234, 'doja'], [4321, 'justin']], columns=['artist_id', 'name'])

client.big_insert(xdf, 'shazamablam.artists')
print('Finished!')

# """
# Collect the data about all the different cities
# """

# def getArtistsFromTrack(track):
#     arr = []
#     if 'artists' in track:
#         for artist in track['artists']:
#             arr.append({
#                 'name': ' '.join(artist['alias'].split('-')),
#                 'artist_id': artist['id']
#             })
#     return arr

# city_ids = cities['city_id'].values

# tracks = []
# all_artists = []
# artist_songs_refs = []
# for idx, city_id in enumerate(city_ids):
    
#     print(f'{idx + 1} / {len(city_ids)} | City Id: {city_id}')
    
#     url = f'https://www.shazam.com/shazam/v3/en-US/US/web/-/tracks/ip-city-chart-{city_id}?pageSize=200&startFrom=0'
#     data = requests.get(url).json()['tracks']
    
#     for rank, track in enumerate(data):
#         tracks.append({
#             'song_id': track['key'],
#             'title': track['title'],
#             'subtitle': track['subtitle'],
#             'background': track['images']['background'] if ('images' in track) and ('background' in track['images']) else '',
#             'song_image': track['images']['coverart'] if ('images' in track) and ('coverart' in track['images']) else '',
#             'shazam_url': track['url'],
#             'explicit': track['hub']['explicit'],
#             'rank': rank + 1,
#             'city_id': city_id
#         })
#         all_artists = [ *all_artists, *getArtistsFromTrack(track) ]
        
#         if 'artists' in track:
            
#             for artist in track['artists']:
#                 artist_songs_refs.append({ 'song_id': track['key'], 'artist_id': artist['id'] })
    
#     time.sleep(1)
    
# all_artists = pd.DataFrame(all_artists).drop_duplicates(subset=['artist_id'])
# artist_songs_refs = pd.DataFrame(artist_songs_refs)
# tracks = pd.DataFrame(tracks)

# """
# First, we need to see if any artists aren't in the db yet so
# that they can act as references.
# """

# # Get the artists from the database
# string = """
#     select artist_id
#     from shazamablam.artists
#     where artist_id in :artist_ids
# """
# params = { 'artist_ids': tuple(all_artists['artist_id'].values)}
# existing_artists = client.execute(string, params)

# # Remove the artists that already exist from the list of all artists from this dataset
# insertable_artists = pd.merge(all_artists, existing_artists, on='artist_id', how='outer', indicator=True).query(' _merge == "left_only" ').drop(columns=['_merge']).reset_index(drop=True)
# client.big_insert(insertable_artists, 'shazamablam.artists')
# print(f'Inserted {len(insertable_artists)} new artists')

# """
# Next, we need to insert any new songs that do not yet exist
# in the db to act as references to the daily ranking values.
# """

# # Columns for meta info about songs
# song_cols = [
#     'song_id',
#     'title',
#     'subtitle',
#     'background',
#     'song_image',
#     'shazam_url',
#     'explicit'
# ]

# # Remove the duplicate songs from the total list
# songs = tracks.drop_duplicates(subset=['song_id']).reset_index(drop=True)[song_cols]

# # Get the current songs from the database
# string = """
#     select song_id
#     from shazamablam.songs
#     where song_id in :song_ids
# """
# params = { 'song_ids': tuple(songs['song_id'].values) }
# existing_songs = client.execute(string, params)

# # Remove the songs that already exist from the list of all songs from this dataset
# insertable_songs = pd.merge(songs, existing_songs, on='song_id', how='outer', indicator=True).query(' _merge == "left_only" ').drop(columns=['_merge']).reset_index(drop=True)
# client.big_insert(insertable_songs, 'shazamablam.songs')
# print(f'Inserted {len(insertable_songs)} new songs')

# """
# Now that we've got all the new artists, and the new songs, let's add the
# artist->song mappings in on the new songs that we've added.
# """

# # Song ids of the new songs we just inserted
# insertable_song_ids = insertable_songs['song_id'].values

# # Map items that we need to create because we just created the songs for them
# insertable_map = artist_songs_refs[artist_songs_refs['song_id'].isin(insertable_song_ids)].reset_index(drop=True)

# # Insert
# client.big_insert(insertable_map, 'shazamablam.artist_songs_refs')
# print(f'Inserted {len(insertable_map)} new map items')

# """
# Finally, we need to record the ranking values for the data for everything.
# """

# # Extract only the columns that we need from the track dataset
# # which is basically just everything we pulled from shazam
# records_cols = ['song_id', 'rank', 'city_id']
# records = tracks[records_cols].reset_index(drop=True)

# # Insert
# client.big_insert(records, 'shazamablam.records')
# print(f'Inserted {len(records)} new records')