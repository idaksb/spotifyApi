import pygame
import urllib.request


class image():
    def __init__(self,x,y,scale):
        self.x=x
        self.y=y
        self.scale=scale


    def draw(self,surface,image):
        self.width = image.get_width()
        self.height = image.get_height()
        album_image = pygame.transform.scale(image, (int(self.width * self.scale), int(self.height * self.scale)))
        self.rect = album_image.get_rect()
        self.rect.topleft = (self.x, self.y)
        surface.blit(album_image, (self.rect.x, self.rect.y))
    
    def format_url(self,image,type):
        f = open("song"+str(type)+".jpg",'wb')
        f.write(urllib.request.urlopen(image).read())
        f.close()