
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import datetime
from urllib.parse import urlencode

import requests


# In[14]:


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    track_dict={}
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
        
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_playlist(self, _id):
        return self.get_resource(_id, resource_type='playlists')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def get_tracks(self, _id):
        return self.get_resource(_id, resource_type='tracks')
    
    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist' ):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

    def play_track(self,track_id):
        pass

    def stop_track(self):
        headers = self.get_resource_header()
        requests.get("https://api.spotify.com/v1/31me2zqygspuwl66hu4chskv7iky/player/pause",headers=headers)
        pass

    def start_track(self):
        headers = self.get_resource_header()
        requests.get("https://api.spotify.com/v1/31me2zqygspuwl66hu4chskv7iky/player/play",headers=headers)
        pass

    def sort(self, sort_term, search_term):
        sort_term = dict(sort_term)
        return sort_term.get(search_term)

    def sort_playlist(self, playlist):
        tracks_ids = []

        playlist = self.sort(playlist,"tracks")
        playlist = self.sort(playlist,"items")

        for i in range(0,len(playlist)):
            playlist_sorted = playlist[i]
            playlist_sorted = self.sort(playlist_sorted,"track")
            tracks_ids = tracks_ids + [1]
            tracks_ids[i] = self.sort(playlist_sorted,"id")

        return tracks_ids

    def sort_track(self,track_id):
        track=self.get_tracks(track_id)

        track_name = self.sort(track,"name")

        track_artist = self.sort(track,"artists")
        track_artist = track_artist[0]
        track_artist = self.sort(track_artist,"name")

        track_image = self.sort(track,"album")
        track_image = self.sort(track_image,"images")
        track_image = track_image[0]
        track_image= dict(track_image)

        track_liste = [track_name,track_artist,track_image]

        self.track_dict.update({track_id:track_liste})
        return self.track_dict

client_id="8e5ec3fce24c493e8fec09e90a061596"
client_secret = "2de425668fec4d9ea44dbfb0f0d2c04d"

spotify = SpotifyAPI(client_id, client_secret)



#playlist = spotify.get_playlist("3cEYpjA9oz9GiPac4AsH4n")
#spotify.sort_track("4rzfv0JLZfVhOhbSQ8o5jZ")
#print(spotify.sort_playlist(playlist))
#spotify.stop_track
