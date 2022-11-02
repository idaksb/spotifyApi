import json
import spotipy
import webbrowser
class song_Play(object):
    clientID=None
    clientSecret =None
    redirectURI = 'https://www.startpage.com/' 
    username = "31me2zqygspuwl66hu4chskv7iky"
    spotifyObject = None
    def __init__(self, client_id, client_secret):
        self.clientID = client_id
        self.clientSecret = client_secret

    def oauth(self):
        print(2)
        oauth_object = spotipy.SpotifyOAuth(self.clientID,self.clientSecret,self.redirectURI)
        token_dict = oauth_object.get_access_token()
        token = token_dict['access_token']
        self.spotifyObject = spotipy.Spotify(auth=token)
        user = self.spotifyObject.current_user()
        print(json.dumps(user,sort_keys=True, indent=4))

    def play_Song(self,song_Name):
        print(1)
        self.oauth()
        # Get the Song Name.
        searchQuery = song_Name
        # Search for the Song.
        searchResults = self.spotifyObject.search(searchQuery,1,0,"track")
        print(searchResults)
        # Get required data from JSON response.
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
        webbrowser.open(song)

