
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

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

class GameObject:
    """Base class for all objects in the game."""
    def __init__(self, x, y, sprite, speed):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def draw(self, surface):
        if self.sprite:
            surface.blit(self.sprite, (self.x, self.y))

class MovableObject(GameObject):
    """Base class for all movable game objects."""
    def __init__(self, x, y, sprite, speed):
        super().__init__(x, y, sprite, speed)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

class Spaceship(MovableObject):
    def __init__(self, sprite, bullet_sprite, lives):
        super().__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, sprite, SPACESHIP_SPEED)
        self.bullet_sprite = bullet_sprite
        self.lives = lives

    def move_left(self):
        """Move the spaceship left."""
        self.x = max(self.x - self.speed, 0)

    def move_right(self):
        """Move the spaceship right."""
        self.x = min(self.x + self.speed, SCREEN_WIDTH - self.sprite.get_width())

    def shoot(self):
        """Shoot a bullet from the spaceship."""
        return Bullet(self.x + self.sprite.get_width() // 2, self.y, self.bullet_sprite)

class Bullet(MovableObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, BULLET_SPEED)

    def update(self):
        """Move bullet upward."""
        self.move(0, 1)

class Alien(MovableObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, ALIEN_SPEED)
        self.direction = 1

    def update(self, step_down=False):
        """Move the alien left/right and down if needed."""
        self.move(self.direction, 0)
        if step_down:
            self.move(0, 30)

class AlienManager:
    """Handles alien creation, movement, and interaction."""
    def __init__(self, alien_sprite):
        self.alien_sprite = alien_sprite
        self.reset()

    def reset(self):
        """Initialize or reset aliens."""
        self.aliens = [Alien(x * 60, y * 50 + 50, self.alien_sprite) for x in range(10) for y in range(5)]

    def update(self):
        """Update aliens' position and check for direction change."""
        step_down = False
        if any(a.x <= 0 for a in self.aliens):
            self.reverse_direction(True)
        elif any(a.x + a.sprite.get_width() >= SCREEN_WIDTH for a in self.aliens):
            self.reverse_direction(True)

        for alien in self.aliens:
            alien.update(step_down)

    def reverse_direction(self, step_down):
        """Reverse direction and step down if necessary."""
        for alien in self.aliens:
            alien.direction *= -1
            if step_down:
                alien.update(True)

class ScoreManager:
    """Manages game score and high score."""
    def __init__(self, font):
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = font

    def load_high_score(self):
        """Load the high score from file."""
        try:
            with open(HIGH_SCORE_PATH, 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        """Save the high score to file."""
        with open(HIGH_SCORE_PATH, 'w') as file:
            file.write(str(self.high_score))

    def increase_score(self, value):
        """Increase the score and update the high score if necessary."""
        self.score += value
        if self.score > self.high_score:
            self.high_score = self.score

    def display(self, surface):
        """Display the current and high scores."""
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        surface.blit(high_score_text, (10, 40))

class Background:
    """Handles scrolling background."""
    def __init__(self, image):
        self.image = image
        self.y1 = 0
        self.y2 = -self.image.get_height()

    def update(self):
        """Scroll the background continuously."""
        self.y1 += BACKGROUND_SCROLL_SPEED
        self.y2 += BACKGROUND_SCROLL_SPEED
        if self.y1 >= SCREEN_HEIGHT:
            self.y1 = self.y2 - self.image.get_height()
        if self.y2 >= SCREEN_HEIGHT:
            self.y2 = self.y1 - self.image.get_height()

    def draw(self, surface):
        """Draw the scrolling backgrounds."""
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))

class Game:
    """Main class to run the Space Invaders game."""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Invaders')
        self.clock = pygame.time.Clock()

        # Load images
        self.spaceship_sprite = pygame.image.load(SPACESHIP_IMAGE_PATH).convert_alpha()
        self.bullet_sprite = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        self.alien_sprite = pygame.image.load(ALIEN_IMAGE_PATH).convert_alpha()
        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()

        # Initialize game objects
        self.spaceship = Spaceship(self.spaceship_sprite, self.bullet_sprite, INITIAL_LIVES)
        self.alien_manager = AlienManager(self.alien_sprite)
        self.bullets = []
        self.background = Background(self.background_image)

        # Initialize score manager
        self.font = pygame.font.Font(None, 36)
        self.score_manager = ScoreManager(self.font)

        # Load sounds
        self.shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
        self.destroy_sound = pygame.mixer.Sound(DESTROY_SOUND_PATH)
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_PATH)
        pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.play(-1)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        """Handle all input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right()
                elif event.key == pygame.K_SPACE:
                    self.bullets.append(self.spaceship.shoot())
                    self.shoot_sound.play()
        return True

    def update(self):
        """Update the game state for all elements."""
        self.background.update()
        self.bullets = [b for b in self.bullets if b.update() or b.y >= 0]

        self.alien_manager.update()

        for bullet in self.bullets[:]:
            for alien in self.alien_manager.aliens[:]:
                if self.check_collision(bullet, alien):
                    self.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    self.destroy_sound.play()
                    self.score_manager.increase_score(SCORE_INCREMENT)
                    break

        if any(alien.y + alien.sprite.get_height() > self.spaceship.y for alien in self.alien_manager.aliens):
            self.trigger_game_over()

    def check_collision(self, bullet, alien):
        """Check collision between a bullet and an alien."""
        return alien.x < bullet.x < alien.x + alien.sprite.get_width() and \
               alien.y < bullet.y < alien.y + alien.sprite.get_height()

    def draw(self):
        """Draw all game elements on the screen."""
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        for alien in self.alien_manager.aliens:
            alien.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.score_manager.display(self.screen)
        pygame.display.flip()

    def trigger_game_over(self):
        """Handle game over state."""
        self.game_over_sound.play()
        self.score_manager.save_high_score()
        self.quit()

    def quit(self):
        """Quit the game safely."""
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()


