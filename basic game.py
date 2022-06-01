from email.mime import image
import pygame
import button
import Song


#initialize pygame and set basics
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Song Rating")

#button images missing
left_image=pygame.image.load('Hintergrund.png').convert_alpha()

#deffinition and creation
done=False
fps=25
state="start" 
left_button = button.Button(100,200,left_image,0.1)
right_button = button.Button(200,200,left_image,0.1)

# color definition
cyan=(0,255,255)



while not done:
#screen color
    screen.fill(cyan)

#stop game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

#button controll
    if left_button.draw(screen):
	    print("1")
	
    if right_button.draw(screen):
	    print("2")
    
    pygame.display.update()
    


pygame.quit()