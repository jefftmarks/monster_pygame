import pygame, random
from constants import *
from player import Player
from monster import Monster
from game import Game

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

clock = pygame.time.Clock()

# Create main assets
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
monster_group = pygame.sprite.Group()

game = Game(window, player, monster_group)
game.start_new_round()

# Main game loop
while game.running:
    for event in pygame.event.get():
        # If player quits
        if event.type == pygame.QUIT:
            game.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.warp()

    # Fill display
    window.fill(Colors.BLACK)

    # Update and draw sprite groups
    player_group.update()
    player_group.draw(window)

    monster_group.update()
    monster_group.draw(window)

    game.update()
    game.draw()

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End game
pygame.quit()

