from signal import pause
from webbrowser import BackgroundBrowser
import spotify
import button
import pygame
import image
from pygame.locals import *

class Song():
    x = None
    y = None    
    text= None
    image = None
    play_button = None
    api = None
    objekt_number = None
    play_status = True

    client_id="8e5ec3fce24c493e8fec09e90a061596"
    client_secret = "2de425668fec4d9ea44dbfb0f0d2c04d"

    def __init__(self,x,y,objekt_number):
        #pngs for button and songcover
        self.pause = pygame.image.load('paus.png').convert_alpha()
        self.play = pygame.image.load('play.png').convert_alpha()
        self.start = pygame.image.load('start.png').convert_alpha()
        self.background = pygame.image.load('background.png').convert_alpha()
        self.vote_png = self.pause

        self.x = x
        self.y = y
        self.objekt_number = objekt_number
        vote_width = self.vote_png.get_width()
        self.api = spotify.SpotifyAPI(self.client_id, self.client_secret)

        
        self.play_button=button.Button(x,y,self.play,0.5)
        self.vote = button.Button(x+206+0.25*vote_width,y+612,self.pause,0.5)
        self.text=self.font("start")
        self.album_image=image.image(x,y+50,0.8)
        self.background_image =image.image(x+50,y,1.0)

    def new_song(self,song_id):
        song = self.api.sort_track(song_id)
        song_liste = song.get(song_id)
        self.text = self.font(song_liste[0]+" von "+song_liste[1])
        image = song_liste[2]
        image = dict(image)
        url = image.get("url") 
        self.album_image.format_url(url,self.objekt_number)



    def draw(self,surface):
        self.surface=surface
        self.background_image.draw(surface,self.background)
        surface.blit(self.text,(self.x+50,self.y+15))
        album_image_var = pygame.image.load("song"+str(self.objekt_number)+".jpg").convert_alpha()
        self.album_image.draw(surface,album_image_var)



    def font(self,text):
        WHITE = (255,255,255)
        font = pygame.font.SysFont(None, 32)
        img = font.render(text, True, WHITE)
        return img
    
    #button controll
    def play_button_controll(self):
        if self.play_button.draw(self.surface):
            if self.play_status:
                self.play_status = False 
                self.play_button.change_image(self.pause)
            else:
                self.play_status = True 
                self.play_button.change_image(self.play)
    
    def vote_button_controll(self):
            return self.vote.draw(self.surface)
        