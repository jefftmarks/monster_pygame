import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    """Knight controlled by user"""

    def __init__(self):
        """Initialize the player"""
        super().__init__()
        self.image = pygame.image.load('assets/knight.png')
        self.rect = self.image.get_rect()
        self.reset()
        self.velocity = PLAYER_VELOCITY
        self.left_safe_zone = False

        self.catch_sound = pygame.mixer.Sound('assets/catch.wav')
        self.die_sound = pygame.mixer.Sound('assets/die.wav')
        self.warp_sound = pygame.mixer.Sound('assets/warp.wav')

    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
            if self.rect.top < WINDOW_HEIGHT - 100:
                self.left_safe_zone = True
        if keys[pygame.K_DOWN] and self.rect.bottom < self.determine_bottom_boundary():
            self.rect.y += self.velocity

    def determine_bottom_boundary(self):
        if self.left_safe_zone:
            return WINDOW_HEIGHT - 100
        else:
            return WINDOW_HEIGHT

    def warp(self):
        """Warp the player to safe zone"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.lives = PLAYER_STARTING_LIVES
        self.warps = PLAYER_STARTING_WARPS
        self.reset_position()
    
    def reset_position(self):
        self.left_safe_zone = False
        self.rect.centerx, self.rect.bottom = CENTER_X, WINDOW_HEIGHT