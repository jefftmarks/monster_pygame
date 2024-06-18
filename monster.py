import pygame, random
from constants import *

class Monster(pygame.sprite.Sprite):
    """Enemy monster"""

    def __init__(self, x, y, type):
        """Initialize the monster"""
        super().__init__()
        self.type = type
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)

    def load_image(self):
        color = MONSTER_COLORS[self.type]
        return pygame.image.load(f'assets/{color}_monster.png')

    def update(self):
        """Update the monster"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # Bounce monster off edge of display
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = self.dx * -1
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy = self.dy * -1
        