#Starting from importing pygame
import pygame

#Intializing the pygame
pygame.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

# To set the screen height and width
screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH))
# pygame.display.set_caption("Background Example")

# Load the background image
background_image = pygame.image.load("background.png").convert()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_image, (0, 0))

    pygame.display.flip()

pygame.quit()
