import pygame, random
from constants import *

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

clock = pygame.time.Clock

# Main game loop
runnung = True
while running:
    for event in pygame.event.get():
        # If player quits
        if event.type == pygame.QUIT:
            running = False

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End game
pygame.quit()

