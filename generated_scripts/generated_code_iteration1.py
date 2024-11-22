Creating a Space Invaders game from scratch in Python without using a game development framework is quite complex. While this is a simplified version, it aims to highlight how you might organize your code to achieve the goal using standard Python libraries. It focuses more on conceptual organization than on specific implementations of all features. Here, I'll refine the previous implementation and integrate the components more logically.

```python
import time
import random

class Spaceship:
    def __init__(self, start_position):
        self.position = start_position

    def move(self, direction: str) -> None:
        if direction == 'left':
            self.position = max(0, self.position - 1)
        elif direction == 'right':
            self.position = min(self.position + 1, 100)  # Assume 100 is right edge

    def shoot(self) -> 'Bullet':
        return Bullet(self.position)

    def display(self) -> None:
        # Display spaceship at its current position
        pass

class Alien:
    def __init__(self, position, speed):
        self.position = position
        self.is_alive = True
        self.speed = speed

    def move(self) -> None:
        if self.is_alive:
            self.position += self.speed

    def display(self) -> None:
        if self.is_alive:
            # Display alien at its current position
            pass

class Bullet:
    def __init__(self, start_position):
        self.position = start_position
        self.is_active = True

    def move(self) -> None:
        if self.is_active:
            self.position += 1  # Move bullet upward

    def display(self) -> None:
        if self.is_active:
            # Display bullet at its current position
            pass

class GraphicsRenderer:
    def render_game_objects(self, spaceship, aliens, bullets):
        # Implement rendering of game objects on the screen using a suitable graphics library
        spaceship.display()
        for alien in aliens:
            alien.display()
        for bullet in bullets:
            bullet.display()

class SoundManager:
    def __init__(self, shoot_sound: str, destroy_sound: str, game_over_sound: str, background_music: str):
        # Initialize sound assets
        pass

    def play_sound(self, sound: str) -> None:
        # Implement sound playing logic here using a suitable library
        pass

    def play_background_music(self) -> None:
        # Implement background music playing logic here using a suitable library
        pass

    def stop_music(self) -> None:
        pass

class Game:
    def __init__(self):
        self.spaceship = Spaceship(start_position=50)  # Assume starting at position 50
        self.aliens = [Alien((i * 10), 1) for i in range(10)]  # Example alien positions
        self.bullets = []
        self.score = 0
        self.high_score = self.load_high_score('highscore.txt')
        self.lives = 3
        self.level = 1
        self.is_running = False
        self.background_position = (0, 0)
        self.graphics_renderer = GraphicsRenderer()
        self.sound_manager = SoundManager('shoot.wav', 'destroy.wav', 'game_over.wav', 'background_music.mp3')

    def run(self) -> None:
        self.is_running = True
        self.sound_manager.play_background_music()
        while self.is_running:
            self.handle_user_input('')  # Placeholder for actual input
            self.main_game_loop()

    def main_game_loop(self) -> None:
        while self.is_running:
            # Update game logic
            self.update_positions()
            self.detect_collisions()
            self.graphics_renderer.render_game_objects(self.spaceship, self.aliens, self.bullets)
            self.scroll_background()
            self.display_hud_and_scoreboard()
            self.check_game_over()
            time.sleep(0.016)  # 60 FPS

    def update_positions(self) -> None:
        for alien in self.aliens:
            alien.move()

        for bullet in self.bullets:
            bullet.move()

    def detect_collisions(self) -> None:
        for bullet in self.bullets:
            for alien in self.aliens:
                if bullet.position == alien.position:
                    bullet.is_active = False
                    alien.is_alive = False
                    self.score += 10
                    self.sound_manager.play_sound("destroy")

    def handle_user_input(self, input_key: str) -> None:
        if input_key == 'left':
            self.spaceship.move('left')
        elif input_key == 'right':
            self.spaceship.move('right')
        elif input_key == 'shoot':
            bullet = self.spaceship.shoot()
            self.bullets.append(bullet)
            self.sound_manager.play_sound("shoot")
        elif input_key == 'pause':
            self.is_running = False
            self.sound_manager.stop_music()
        elif input_key == 'quit':
            self.is_running = False

    def scroll_background(self) -> None:
        # Implement scrolling mechanics for the background image
        pass

    def display_hud_and_scoreboard(self) -> None:
        # Implement displaying the score, high score, lives, level, and number of aliens
        pass

    def check_game_over(self) -> None:
        if self.lives <= 0:
            self.sound_manager.play_sound("game_over")
            self.is_running = False
            self.save_high_score('highscore.txt')

    def save_high_score(self, filename: str) -> None:
        with open(filename, 'w') as file:
            file.write(str(self.high_score))

    def load_high_score(self, filename: str) -> int:
        try:
            with open(filename, 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

if __name__ == "__main__":
    game = Game()
    game.run()
```

### Key Points:

- **Game Loop**: The `main_game_loop` runs while `is_running` is `True` and handles all essential game operations, including updating positions, collision detection, rendering, and checking for game-over conditions.
- **Collision Detection**: Implemented rudimentary collision detection between bullets and aliens.
- **User Input**: The game currently has placeholder input handling; in a real implementation, you'd use a library to capture actual user input events.
- **Sound and Music**: `SoundManager` serves to play sounds and manage background music, but real sound functionality depends on an external library (like `pygame` for sounds and music).
- **Graphics and Rendering**: `GraphicsRenderer` is a stub demonstrating where and how you might implement drawing logic.
- **Background and Level Logic**: These are stubbed functions where further implementation is needed to meet specific design goals.
- **File Handling**: High score reading and writing is implemented simply with basic file I/O.

This refactored version brings more coherence to the logic flow and consolidates game-handling logic under the `Game` class. Actual event handling, rendering, and audio playback would typically require additional integration with graphical and audio libraries like `pygame`.


import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPACESHIP_SPEED = 5
BULLET_SPEED = 10
ALIEN_SPEED = 3
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Placeholder assets
SPACESHIP_IMAGE = 'spaceship_image.png'
ALIEN_IMAGE = 'alien_image.png'
BULLET_IMAGE = 'bullet_image.png'
BACKGROUND_MUSIC = 'background_music.mp3'
EXPLOSION_SOUND = 'explosion_sound.wav'
SHOOT_SOUND = 'shoot_sound.wav'

# GameObject base class
class GameObject:
    def __init__(self, x=0, y=0, speed=1):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

# Spaceship class
class Spaceship(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, SPACESHIP_SPEED)
        self.lives = 3

    def move_left(self):
        self.move(dx=-self.speed)

    def move_right(self):
        self.move(dx=self.speed)

    def shoot(self):
        return Bullet(self.x, self.y)

# Bullet class
class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, BULLET_SPEED)

    def move_up(self):
        self.move(dy=-self.speed)

# Alien class
class Alien(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, ALIEN_SPEED)

    def move(self, direction):
        if direction == 'left':
            self.move(dx=-self.speed)
        elif direction == 'right':
            self.move(dx=self.speed)

# AlienManager class
class AlienManager:
    def __init__(self):
        self.aliens = []

    def create_aliens(self):
        for i in range(5):
            alien = Alien(x=random.randint(0, SCREEN_WIDTH), y=random.randint(0, 100))
            self.aliens.append(alien)

    def move_aliens(self, direction):
        for alien in self.aliens:
            alien.move(direction)

    def check_direction_change(self):
        return any(alien.x <= 0 or alien.x >= SCREEN_WIDTH for alien in self.aliens)

    def determine_move_direction(self):
        if self.check_direction_change():
            return 'right' if random.choice([True, False]) else 'left'
        return 'left'

# ScoreManager class
class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0

    def increase_score(self):
        self.score += 10

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0
        return self.high_score

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(max(self.score, self.high_score)))

# Screen class
class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def refresh(self):
        pygame.display.flip()
        self.clock.tick(FPS)

    def draw_game_objects(self, spaceship, aliens, bullets):
        self.screen.fill(WHITE)
        # Placeholder rendering
        for bullet in bullets:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(bullet.x, bullet.y, 5, 10))

        for alien in aliens:
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(alien.x, alien.y, 50, 30))
        
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(spaceship.x, spaceship.y, 50, 20))

    def display_stats(self, lives, level, score, aliens_remaining):
        # Display stats
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Lives: {lives} Level: {level} Score: {score} Aliens: {aliens_remaining}", True, (0, 0, 0))
        self.screen.blit(text_surface, (20, SCREEN_HEIGHT - 40))

    def show_game_over_screen(self):
        # Display Game Over message
        pass

# AudioManager class
class AudioManager:
    def play_background_music(self):
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play(-1)

    def play_sound_effect(self, effect):
        sound = pygame.mixer.Sound(effect)
        sound.play()

# PauseManager class
class PauseManager:
    def __init__(self):
        self.paused = False

    def toggle(self):
        self.paused = not self.paused

# GameInitializer class
class GameInitializer:
    def __init__(self):
        self.screen = Screen()
        self.spaceship = Spaceship(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT-50)
        self.bullets = []
        self.alien_manager = AlienManager()
        self.score_manager = ScoreManager()
        self.audio_manager = AudioManager()
        self.pause_manager = PauseManager()
        self.level = 1

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.spaceship.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.move_right()
                elif event.key == pygame.K_SPACE:
                    bullet = self.spaceship.shoot()
                    self.bullets.append(bullet)
                    self.audio_manager.play_sound_effect(SHOOT_SOUND)
                elif event.key == pygame.K_p:
                    self.pause_manager.toggle()

    def update_game_state(self):
        for bullet in self.bullets:
            bullet.move_up()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        direction = self.alien_manager.determine_move_direction()
        self.alien_manager.move_aliens(direction)

        for bullet in self.bullets:
            for alien in self.alien_manager.aliens:
                if pygame.Rect(bullet.x, bullet.y, 5, 10).colliderect(pygame.Rect(alien.x, alien.y, 50, 30)):
                    self.score_manager.increase_score()
                    self.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    break

        if len(self.alien_manager.aliens) == 0:
            self.level += 1
            self.alien_manager.create_aliens()

        if any(alien.y >= self.spaceship.y for alien in self.alien_manager.aliens):
            self.screen.show_game_over_screen()
            self.score_manager.save_high_score()
            pygame.quit()
            sys.exit()

    def run(self):
        self.alien_manager.create_aliens()
        self.audio_manager.play_background_music()

        while True:
            self.screen.refresh()
            self.handle_input()
            if not self.pause_manager.paused:
                self.update_game_state()

                self.screen.draw_game_objects(self.spaceship, self.alien_manager.aliens, self.bullets)
                self.screen.display_stats(self.spaceship.lives, self.level, self.score_manager.score, len(self.alien_manager.aliens))

game = GameInitializer()
game.run()



import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ALIEN_SPEED = 1
BULLET_SPEED = -5
SPACESHIP_SPEED = 5
ALIEN_ROWS = 5
ALIEN_COLUMNS = 10
INITIAL_LIVES = 3
FPS = 60  # Frames per second
BACKGROUND_SCROLL_SPEED = 1

pygame.init()

class GameObject:
    def __init__(self, x=0, y=0, sprite=None, speed=1):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def draw(self, surface):
        if self.sprite:
            surface.blit(self.sprite, (self.x, self.y))

class Spaceship(GameObject):
    def __init__(self, sprite, bullet_sprite, lives, speed):
        super().__init__(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 60, sprite=sprite, speed=speed)
        self.bullet_sprite = bullet_sprite
        self.lives = lives

    def move_left(self):
        self.x = max(self.x - self.speed, 0)
    
    def move_right(self):
        self.x = min(self.x + self.speed, SCREEN_WIDTH - self.sprite.get_width())

    def shoot(self):
        return Bullet(self.x + self.sprite.get_width() // 2, self.y, self.bullet_sprite)

class Bullet(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x=x, y=y, sprite=sprite, speed=BULLET_SPEED)

    def move(self):
        self.y += self.speed

class Alien(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x=x, y=y, sprite=sprite, speed=ALIEN_SPEED)
        self.direction = 1

    def move(self, step_down=False):
        self.x += self.speed * self.direction
        if step_down:
            self.y += 30

class AlienManager:
    def __init__(self, alien_sprite):
        self.alien_sprite = alien_sprite
        self.aliens = [Alien(x * 60, y * 50 + 50, alien_sprite) for x in range(ALIEN_COLUMNS) for y in range(ALIEN_ROWS)]
    
    def move_aliens(self):
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
        for alien in self.aliens:
            alien.direction = direction

class ScoreManager:
    def __init__(self, font):
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = font

    def increase_score(self, value):
        self.score += value
        if self.score > self.high_score:
            self.high_score = self.score

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def display_scores(self, surface):
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
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Invaders')
        self.clock = pygame.time.Clock()

        # Load sprites
        self.spaceship_sprite = pygame.image.load('spaceship.png').convert_alpha()
        self.bullet_sprite = pygame.image.load('bullet.png').convert_alpha()
        self.alien_sprite = pygame.image.load('alien.png').convert_alpha()
        self.background_image = pygame.image.load('background.jpg').convert()

        # Initialize game objects
        self.spaceship = Spaceship(self.spaceship_sprite, self.bullet_sprite, INITIAL_LIVES, SPACESHIP_SPEED)
        self.alien_manager = AlienManager(self.alien_sprite)
        self.bullets = []
        self.background = Background(self.background_image)

        # Initialize score manager
        self.font = pygame.font.Font(None, 36)
        self.score_manager = ScoreManager(self.font)

        # Load sounds
        self.shoot_sound = pygame.mixer.Sound('shoot.wav')
        self.destroy_sound = pygame.mixer.Sound('destroy.wav')
        self.game_over_sound = pygame.mixer.Sound('game_over.wav')
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw_elements()
            self.clock.tick(FPS)

    def handle_events(self):
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
        self.background.scroll()
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        self.alien_manager.move_aliens()

        for bullet in self.bullets[:]:
            for alien in self.alien_manager.aliens[:]:
                if self.check_collision(bullet, alien):
                    self.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    self.destroy_sound.play()
                    self.score_manager.increase_score(10)
                    break

        if any(alien.y + alien.sprite.get_height() > self.spaceship.y for alien in self.alien_manager.aliens):
            self.game_over()

    def check_collision(self, bullet, alien):
        return alien.x < bullet.x < alien.x + alien.sprite.get_width() and alien.y < bullet.y < alien.y + alien.sprite.get_height()

    def draw_elements(self):
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        for alien in self.alien_manager.aliens:
            alien.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.score_manager.display_scores(self.screen)
        pygame.display.flip()

    def game_over(self):
        self.game_over_sound.play()
        self.score_manager.save_high_score()
        pygame.quit()
        sys.exit()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
```

Make sure to replace the sprite image file paths, sound file paths, and the background image file path with valid paths to your assets when integrating this code into a proje

