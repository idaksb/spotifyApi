from curses import KEY_BACKSPACE, KEY_DOWN
from typing import Dict
import pygame
import button
import song
from pygame.locals import *
import spotify
import operator
import random
import time
#import 

def font(text):
        WHITE = (255,255,255)
        font = pygame.font.SysFont(None, 72)
        img = font.render(text, True, WHITE)
        return img


#initialize pygame and set basics
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Song Rating")

#deffinition and creation
done=False
fps=25
state="start"

song1 = song.Song(200,100,1)
song1.draw(screen)
song2 = song.Song(1208,100,2)
song2.draw(screen)

client_id="8e5ec3fce24c493e8fec09e90a061596"
client_secret = "2de425668fec4d9ea44dbfb0f0d2c04d"
spotify_api = spotify.SpotifyAPI(client_id,client_secret)

buttton_image = pygame.image.load('paus.png').convert_alpha()
#image grösse einstellen
evaluation_button = button.Button(870,540,buttton_image,0.8)
# color definition
cyan=(0,255,255)
white=(255,255,255)

state = "playlist"
playlist_search_input = ''
text = "Playlist Name eingeben (bitte nicht mit einer Zahl beginnen)"
font = pygame.font.SysFont(None, 48)
img = font.render(playlist_search_input, True, white)

rect = img.get_rect()
rect.topleft = (800,500)
cursor = Rect(rect.topright, (3, rect.height))

while state == "playlist":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = "quit"
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(playlist_search_input)>0:
                    playlist_search_input = playlist_search_input[:-1]
            else:
                playlist_search_input += event.unicode
            img = font.render(playlist_search_input, True, white)
            rect.size=img.get_size()
            cursor.topleft = rect.topright
            if event.key == pygame.K_RETURN:
                state = "game"
    
    überschrift = font.render(text, True, white)
    screen.fill(cyan)
    screen.blit(img, rect)
    screen.blit(überschrift,(500,450))
    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, white, cursor)

    pygame.display.update()




#add playlist input
print(playlist_search_input[:-1])
if playlist_search_input[0] == "1" and "2" and "3" and "4" and "5" and "6" and "7" and "8" and "9" and "0":
    playlist_id=playlist_search_input
else:
    search = spotify_api.search(query=playlist_search_input)
    playlist_id=spotify_api.sort_search(search)


playlist = spotify_api.get_playlist(playlist_id)
track_liste = spotify_api.sort_playlist(playlist)
rating_liste = {}
for i in track_liste:
    rating_liste.update({i:0})
votes = len(track_liste)-1



vote_state = False

song_nr = random.randint(0,len(track_liste)-1)
song1.new_song(track_liste[song_nr])
song_id1 = track_liste[song_nr]
del track_liste[song_nr]


song_nr = random.randint(0,len(track_liste)-1)
song2.new_song(track_liste[song_nr])
song_id2 = track_liste[song_nr]
del track_liste[song_nr]




while state == "game":
    #screen color
    screen.fill(cyan)

    #stop game
    vote_state = False 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state= "quit"
    if evaluation_button.draw(screen):
        state="evaluation"
    
    

    song1.play_button_controll()
    song1.draw(screen)
    song2.play_button_controll()
    song2.draw(screen)
    if votes>1:

        
        if song1.vote_button_controll():
            rating_liste[song_id1] = rating_liste.get(song_id1)+1
            vote_state = True
            votes = votes -1
    
    
        if song2.vote_button_controll():
            vote_state = True
            rating_liste[song_id2] = rating_liste.get(song_id2)+1
            song_id1 = song_id2
            song1.new_song(song_id2)
            votes = votes -1

        if vote_state:
            song_nr = random.randint(0,len(track_liste)-1)
            song2.new_song(track_liste[song_nr])
            song_id2 = track_liste[song_nr]
            del track_liste[song_nr]
            vote_state = False
    
    elif votes==1:
        if song1.vote_button_controll():
            rating_liste[song_id1] = rating_liste.get(song_id1)+1
            votes = votes -1
    
    
        if song2.vote_button_controll():
            rating_liste[song_id2] = rating_liste.get(song_id2)+1
            votes = votes -1

    else:
        state = "end"


    
    pygame.display.update()
    
while state == "end":
    song1.draw(screen)
    song2.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state= "quit" 
    if evaluation_button.draw(screen):
        state="evaluation"
    pygame.display.update()

if state == "evaluation":
    sortedDict = sorted(rating_liste.items(), key=operator.itemgetter(1))
    lenght=len(sortedDict)
    lenght = lenght - 10
    if lenght > 1:
        for i in range (0,lenght):
            del sortedDict[0]
    screen.fill(cyan)
    pygame.display.flip()
    pos=0

    for key,value in sortedDict:
        pos =pos+1
        track = spotify_api.sort_track(key)
        track_liste = track.get(key)
        text = song1.font(track_liste[0]+" "+str(value))
        screen.blit(text,(600,850-75*pos))
        
while state == "evaluation":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state= "quit" 
    pygame.display.update()

pygame.quit()