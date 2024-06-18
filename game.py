import pygame, random
from constants import *
from hud import *
from monster import Monster

class Game():
    """Controls gameplay"""

    def __init__(self, window, player, monsters):
        """Initialize game object"""
        self.running = True

        self.score = 0
        self.round = 0

        self.round_time = 0
        self.frame_count = 0

        self.window = window
        self.player = player
        self.monsters = monsters

        self.next_level_sound = pygame.mixer.Sound('assets/next_level.wav')

        self.render_text()
        self.hud = HUD(self.catch_text, self.score_text, self.lives_text, self.round_text,
                       self.time_text, self.warp_text)

        self.load_monster_images()

    def render_text(self):
        self.catch_text = Text("Current Catch")
        self.catch_text.rect.centerx, self.catch_text.rect.top = CENTER_X, 5

        self.score_text = UpdatableText("Score", self)
        self.score_text.rect.topleft = (5, 5)

        self.lives_text = UpdatableText("Lives", self.player)
        self.lives_text.rect.topleft = (5, 35)

        self.round_text = UpdatableText("Current Round", self, attr="round")
        self.round_text.rect.topleft = (5, 65)

        self.time_text = UpdatableText("Round Time", self, update_rect_after_re_render=True)
        self.time_text.rect.topright = (WINDOW_WIDTH - 10, 5)

        self.warp_text = UpdatableText("Warps", self.player)
        self.warp_text.rect.topright = (WINDOW_WIDTH - 10, 35)

    def load_monster_images(self):
        def load_image(color):
            return pygame.image.load(f'assets/{color}_monster.png')

        self.monster_images = [load_image(color) for color in MONSTER_COLORS]
        self.target_type = random.randint(0, 3)
        self.target_image = self.monster_images[self.target_type]
        self.target_rect = self.target_image.get_rect()
        self.target_rect.centerx, self.target_rect.top = CENTER_X, 30

    def update(self):
        """Update game object"""
        # Update round time
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        # Update HUD
        self.update_hud()

        # Check for collisions
        self.check_collisions()

    def update_hud(self):
        self.hud.update()
        self.time_text.rect.topright = (WINDOW_WIDTH - 10, 5)

    def draw(self):
        """Draw the HUD and assets to display"""
        self.hud.draw(self.window)

        rgb = getattr(Colors, MONSTER_COLORS[self.target_type].upper())
        pygame.draw.rect(self.window, rgb, (CENTER_X - 32, 30, 64, 64), 2)
        pygame.draw.rect(self.window, rgb, (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)

        self.window.blit(self.target_image, self.target_rect)

    def check_collisions(self):
        """Check for collisions between player and monsters"""
        # Check for collision between player and individual monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monsters)

        # Collision detected
        if collided_monster:
            # Caught correct monster
            if collided_monster.type == self.target_type:
                self.score += 100 * self.round
                # Remove monster
                collided_monster.remove(self.monsters)
                self.player.catch_sound.play()
                if (self.monsters):
                    # There are more monsters to catch
                    self.choose_new_target()
                else:
                    # Round is complete
                    self.start_new_round()
            else:
                # Caught wrong monster
                self.player.die_sound.play()
                self.player.lives -= 1
                self.player.reset_position()
                # Check for game over
                if self.player.lives <= 0:
                    self.pause_game()
                    self.reset_game()
                    
    def start_new_round(self):
        """Populate board with new monsters"""
        # Reset player
        self.player.reset_position()
        
        # Provide score bonus
        self.score += int(10_000 * self.round / (1 + self.round_time))

        # Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round += 1
        if self.round > 1:
            self.player.warps += 1

        # Remove monsters
        self.clear_monsters()

        # Add monsters to monster group 
        self.generate_new_monsters()

        # Choose new target
        self.choose_new_target()

        self.next_level_sound.play()

    
    def clear_monsters(self):
        """Remove remaining monsters"""
        for monster in self.monsters:
            self.monsters.remove(monster)
        
    def generate_new_monsters(self):
        """Add monsters to monster group"""
        def generate_monster(color):
            x, y = random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164)
            return Monster(x, y, color)
        
        for _ in range(self.round):
            new_monsters = [generate_monster(color) for color in range(len(MONSTER_COLORS))]            
            self.monsters.add(new_monsters)

    def choose_new_target(self):
        """Choose new target monster for the player"""
        target_monster = random.choice(self.monsters.sprites())
        self.target_type = target_monster.type
        self.target_image = target_monster.image

    def pause_game(self):
        """Pause the game"""
        main_text = Text(f"Final Score: {str(self.score)}")
        main_text.rect.center = (CENTER_X, CENTER_Y)

        sub_text = Text("Press any key to continue")
        sub_text.rect.center = (CENTER_X, CENTER_Y + 64)

        self.window.fill(Colors.BLACK)

        self.window.blit(main_text.text, main_text.rect)
        self.window.blit(sub_text.text, sub_text.rect)

        pygame.display.update()

        # Pause game
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    paused = False
                if event.type == pygame.QUIT:
                    paused = False
                    self.running = False

    def reset_game(self):
        """Reset the game"""
        self.score = 0
        self.round = 0
        self.player.reset()
        self.start_new_round()

