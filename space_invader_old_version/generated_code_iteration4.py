
import pygame
import sys
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SPACESHIP_SPEED = 5
BULLET_SPEED = -10
ALIEN_SPEED = 1
FPS = 60
INITIAL_LIVES = 3
BACKGROUND_SCROLL_SPEED = 1
SCORE_INCREMENT = 10

# Asset paths
ASSETS_PATH = 'assets/'
SPACESHIP_IMAGE_PATH = ASSETS_PATH + 'spaceship.png'
BULLET_IMAGE_PATH = ASSETS_PATH + 'bullet.png'
ALIEN_IMAGE_PATH = ASSETS_PATH + 'alien.png'
BACKGROUND_IMAGE_PATH = ASSETS_PATH + 'background.jpg'
BACKGROUND_MUSIC_PATH = ASSETS_PATH + 'background.mp3'
SHOOT_SOUND_PATH = ASSETS_PATH + 'shoot.wav'
DESTROY_SOUND_PATH = ASSETS_PATH + 'destroy.wav'
GAME_OVER_SOUND_PATH = ASSETS_PATH + 'game_over.wav'
HIGH_SCORE_PATH = ASSETS_PATH + 'high_score.txt'

def initialize():
    """Initial setup for pygame and configurations."""
    pygame.init()
    pygame.display.set_caption('Space Invaders')

class GameObject:
    """Base class for all game objects."""
    def __init__(self, x, y, sprite):
        self.x, self.y, self.sprite = x, y, sprite

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

class MovableObject(GameObject):
    """Base class for movable game objects."""
    def __init__(self, x, y, sprite, speed):
        super().__init__(x, y, sprite)
        self.speed = speed

    def move(self, dx=0, dy=0):
        self.x += dx * self.speed
        self.y += dy * self.speed

class Spaceship(MovableObject):
    """Player's spaceship."""
    def __init__(self, sprite, bullet_sprite):
        super().__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, sprite, SPACESHIP_SPEED)
        self.bullet_sprite = bullet_sprite
        self.lives = INITIAL_LIVES

    def move_left(self):
        self.x = max(self.x - self.speed, 0)

    def move_right(self):
        self.x = min(self.x + self.speed, SCREEN_WIDTH - self.sprite.get_width())

    def shoot(self):
        return Bullet(self.x + self.sprite.get_width() // 2, self.y, self.bullet_sprite)

class Bullet(MovableObject):
    """Represents a bullet shot by the spaceship."""
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, BULLET_SPEED)

    def update(self):
        """Move bullet upwards."""
        self.y += self.speed

class Alien(MovableObject):
    """Represents an alien."""
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, ALIEN_SPEED)
        self.direction = 1

    def update(self, step_down=False):
        self.move(self.direction, 0)
        if step_down:
            self.move(0, 30)

class AlienManager:
    """Manages the movement and state of aliens."""
    def __init__(self, alien_sprite):
        self.alien_sprite = alien_sprite
        self.aliens = []
        self.reset()

    def reset(self):
        self.aliens = [Alien(x * 60, y * 50 + 50, self.alien_sprite) for x in range(10) for y in range(5)]

    def update(self):
        step_down = False
        if any(alien.x <= 0 for alien in self.aliens) or any(alien.x + alien.sprite.get_width() >= SCREEN_WIDTH for alien in self.aliens):
            self.reverse_direction(True)

        for alien in self.aliens:
            alien.update(step_down)

    def reverse_direction(self, step_down):
        for alien in self.aliens:
            alien.direction *= -1
            if step_down:
                alien.update(step_down)

class ScoreManager:
    """Handles score tracking and high score persistence."""
    def __init__(self, font):
        self.font, self.score = font, 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_PATH, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open(HIGH_SCORE_PATH, 'w') as file:
            file.write(str(self.high_score))

    def increase_score(self, value):
        self.score += value
        if self.score > self.high_score:
            self.high_score = self.score

    def display(self, surface):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        surface.blit(high_score_text, (10, 40))

class Background:
    """Handles the background scrolling effect."""
    def __init__(self, image):
        self.image = image
        self.y1, self.y2 = 0, -self.image.get_height()

    def update(self):
        self.y1 += BACKGROUND_SCROLL_SPEED
        self.y2 += BACKGROUND_SCROLL_SPEED
        if self.y1 >= SCREEN_HEIGHT:
            self.y1 = self.y2 - self.image.get_height()
        if self.y2 >= SCREEN_HEIGHT:
            self.y2 = self.y1 - self.image.get_height()

    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))

class Game:
    """The main game class handling the game loop and state."""
    def __init__(self):
        initialize()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Load resources
        self.spaceship_sprite = pygame.image.load(SPACESHIP_IMAGE_PATH).convert_alpha()
        self.bullet_sprite = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        self.alien_sprite = pygame.image.load(ALIEN_IMAGE_PATH).convert_alpha()
        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()

        # Game Objects
        self.spaceship = Spaceship(self.spaceship_sprite, self.bullet_sprite)
        self.alien_manager = AlienManager(self.alien_sprite)
        self.bullets = []
        self.background = Background(self.background_image)

        # Score Manager
        self.font = pygame.font.Font(None, 36)
        self.score_manager = ScoreManager(self.font)

        # Load sounds
        self.shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
        self.destroy_sound = pygame.mixer.Sound(DESTROY_SOUND_PATH)
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_PATH)
        pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.play(-1)

    def run(self):
        """The primary game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right()
                elif event.key == pygame.K_SPACE:
                    bullet = self.spaceship.shoot()
                    self.bullets.append(bullet)
                    self.shoot_sound.play()
        return True

    def update(self):
        """Update the state of game objects."""
        self.background.update()
        self.bullets = [b for b in self.bullets if b.y + b.sprite.get_height() > 0]
        for bullet in self.bullets:
            bullet.update()

        self.alien_manager.update()

        self.check_collisions()

        if any(alien.y + alien.sprite.get_height() >= self.spaceship.y for alien in self.alien_manager.aliens):
            self.trigger_game_over()

    def check_collisions(self):
        for bullet in self.bullets.copy():
            for alien in self.alien_manager.aliens.copy():
                if self.check_collision(bullet, alien):
                    self.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    self.destroy_sound.play()
                    self.score_manager.increase_score(SCORE_INCREMENT)

    def check_collision(self, bullet, alien):
        """Check if a bullet collides with an alien."""
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.sprite.get_width(), bullet.sprite.get_height())
        alien_rect = pygame.Rect(alien.x, alien.y, alien.sprite.get_width(), alien.sprite.get_height())
        return bullet_rect.colliderect(alien_rect)

    def draw(self):
        """Render all game elements."""
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        for alien in self.alien_manager.aliens:
            alien.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.score_manager.display(self.screen)
        pygame.display.flip()

    def trigger_game_over(self):
        """Actions to perform when game is over."""
        self.game_over_sound.play()
        self.score_manager.save_high_score()
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()


