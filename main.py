#Siia tuleb kood, mis käivitab kogu mängu
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('bakam2ng')
mang_tootab = True
while mang_tootab:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mang_tootab = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
pygame.quit()
