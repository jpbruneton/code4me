
import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPACESHIP_SPEED = 5
BULLET_SPEED = -10
ALIEN_SPEED = 1
FPS = 60
INITIAL_LIVES = 3
BACKGROUND_SCROLL_SPEED = 1
SCORE_INCREMENT = 10

# Asset paths
SPACESHIP_IMAGE_PATH = 'spaceship.png'
BULLET_IMAGE_PATH = 'bullet.png'
ALIEN_IMAGE_PATH = 'alien.png'
BACKGROUND_IMAGE_PATH = 'background.jpg'
BACKGROUND_MUSIC_PATH = 'background.mp3'
SHOOT_SOUND_PATH = 'shoot.wav'
DESTROY_SOUND_PATH = 'destroy.wav'
GAME_OVER_SOUND_PATH = 'game_over.wav'
HIGH_SCORE_PATH = 'high_score.txt'

pygame.init()


class GameObject:
    def __init__(self, x, y, sprite, speed):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def draw(self, surface):
        """Draw game object on surface."""
        if self.sprite:
            surface.blit(self.sprite, (self.x, self.y))


class Spaceship(GameObject):
    def __init__(self, sprite, bullet_sprite, lives, speed):
        super().__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, sprite, speed)
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


class Bullet(GameObject):
    def move(self):
        """Move bullet upward."""
        self.y += self.speed


class Alien(GameObject):
    def __init__(self, x, y, sprite, speed=ALIEN_SPEED):
        super().__init__(x, y, sprite, speed)
        self.direction = 1

    def move(self, step_down=False):
        """Move the alien left/right and down if needed."""
        self.x += self.speed * self.direction
        if step_down:
            self.y += 30


class AlienManager:
    def __init__(self, alien_sprite):
        self.aliens = [Alien(x * 60, y * 50 + 50, alien_sprite) for x in range(10) for y in range(5)]
    
    def update_aliens(self):
        """Update aliens' position and check for direction change."""
        step_down = False
        if any(alien.x <= 0 for alien in self.aliens):
            self.change_direction(1)
            step_down = True
        elif any(alien.x + alien.sprite.get_width() >= SCREEN_WIDTH for alien in self.aliens):
            self.change_direction(-1)
            step_down = True

        for alien in self.aliens:
            alien.move(step_down)

    def change_direction(self, direction):
        """Change the direction of alien movement."""
        for alien in self.aliens:
            alien.direction = direction


class ScoreManager:
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

    def display_scores(self, surface):
        """Display the current and high scores."""
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        surface.blit(score_text, (10, 10))
        surface.blit(high_score_text, (10, 40))


class Background:
    def __init__(self, image):
        self.image = image
        self.y1 = 0
        self.y2 = -self.image.get_height()

    def scroll(self):
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
        self.spaceship = Spaceship(self.spaceship_sprite, self.bullet_sprite, INITIAL_LIVES, SPACESHIP_SPEED)
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
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw_elements()
            self.clock.tick(FPS)

    def handle_events(self):
        """Handle all input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right()
                elif event.key == pygame.K_SPACE:
                    self.bullets.append(self.spaceship.shoot())
                    self.shoot_sound.play()

    def update_game_state(self):
        """Update the game state for all elements."""
        self.background.scroll()

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        self.alien_manager.update_aliens()

        for bullet in self.bullets[:]:
            for alien in self.alien_manager.aliens[:]:
                if self.check_collision(bullet, alien):
                    self.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    self.destroy_sound.play()
                    self.score_manager.increase_score(SCORE_INCREMENT)
                    break

        if any(alien.y + alien.sprite.get_height() > self.spaceship.y for alien in self.alien_manager.aliens):
            self.game_over()

    def check_collision(self, bullet, alien):
        """Check collision between a bullet and an alien."""
        return alien.x < bullet.x < alien.x + alien.sprite.get_width() and \
               alien.y < bullet.y < alien.y + alien.sprite.get_height()

    def draw_elements(self):
        """Draw all game elements on the screen."""
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        for alien in self.alien_manager.aliens:
            alien.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.score_manager.display_scores(self.screen)
        pygame.display.flip()

    def game_over(self):
        """Handle game over state."""
        self.game_over_sound.play()
        self.score_manager.save_high_score()
        self.quit_game()

    def quit_game(self):
        """Quit the game safely."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()


