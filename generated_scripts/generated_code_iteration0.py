To build a simple "Space Invaders" game in Python without using any game development frameworks, we will take a structured approach, leveraging the use of classes. Below is a revamped version of the code that aims to organize and improve upon the initial snippets provided. We will include more defined structures and logic while still using placeholder comments for certain functionalities like image and sound handling.

Below is a restructured implementation:

```python
import os
from typing import List, Tuple


class Spaceship:
    def __init__(self, position: Tuple[int, int] = (0, 0)):
        self.position = position

    def move(self, direction: str) -> None:
        if direction == 'left':
            self.position = (self.position[0] - 1, self.position[1])  # Adjust as needed
        elif direction == 'right':
            self.position = (self.position[0] + 1, self.position[1])  # Adjust as needed

    def shoot(self) -> 'Bullet':
        # Assuming bullet spawns at spaceship position and moves upwards
        return Bullet(position=(self.position[0], self.position[1] - 1))

    def display(self) -> None:
        # Placeholder for rendering logic
        pass


class Alien:
    def __init__(self, position: Tuple[int, int], speed: int = 1):
        self.position = position
        self.is_alive = True
        self.speed = speed

    def move(self) -> None:
        # Move logic for aliens (e.g., zigzag pattern)
        self.position = (self.position[0] + self.speed, self.position[1])
    
    def display(self) -> None:
        # Placeholder for rendering logic
        pass


class Bullet:
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.is_active = True

    def move(self) -> None:
        # Assuming bullets move upwards
        self.position = (self.position[0], self.position[1] - 1)

    def display(self) -> None:
        # Placeholder for rendering logic
        pass


class SoundManager:
    def __init__(self, shoot_sound: str, destroy_sound: str, game_over_sound: str, background_music: str):
        self.shoot_sound = shoot_sound
        self.destroy_sound = destroy_sound
        self.game_over_sound = game_over_sound
        self.background_music = background_music

    def play_sound(self, sound: str) -> None:
        # Implement sound playing logic here using a suitable library
        pass

    def play_background_music(self) -> None:
        # Implement background music playing logic here using a suitable library
        pass

    def stop_music(self) -> None:
        # Stop background music
        pass


class Game:
    def __init__(self):
        self.spaceship = Spaceship()
        self.aliens: List[Alien] = []
        self.bullets: List[Bullet] = []
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.level = 1
        self.is_running = False
        self.background_position = (0, 0)
        self.sound_manager = SoundManager("shoot.wav", "destroy.wav", "game_over.wav", "background.mp3")
        
    def run(self):
        # Main entry point to start the game
        self.load_high_score("high_score.txt")
        self.is_running = True
        while self.is_running:
            self.main_game_loop()

    def main_game_loop(self):
        # Encapsulates the main game loop and the logical flow
        while self.is_running:
            self.handle_user_input()
            self.update_entities()
            self.detect_collisions()
            self.render_all()
            self.check_gameover_conditions()
            self.scroll_background()
            # Add delay or control frame rate here

    def handle_user_input(self):
        # Collect and handle user inputs (e.g., 'left', 'right', 'shoot', 'pause', 'quit' commands)
        pass

    def update_entities(self):
        # Move the spaceship, bullets, and aliens
        for alien in self.aliens:
            alien.move()
        for bullet in self.bullets:
            bullet.move()

    def detect_collisions(self):
        # Check for collisions between bullets and aliens, and aliens and spaceship
        pass

    def render_all(self):
        # Render the spaceship, aliens, bullets, and HUD
        self.spaceship.display()
        for alien in self.aliens:
            alien.display()
        for bullet in self.bullets:
            bullet.display()
        self.display_hud_and_scoreboard()

    def scroll_background(self):
        # Implement logic for scrolling the background
        pass

    def check_gameover_conditions(self):
        # Check if the game should end
        pass

    def display_hud_and_scoreboard(self):
        # Display score, high score, lives, level, and number of aliens
        pass

    def save_high_score(self, filename: str) -> None:
        with open(filename, 'w') as file:
            file.write(str(self.high_score))

    def load_high_score(self, filename: str) -> None:
        try:
            with open(filename, 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

# Sample code to create a game instance and run it
if __name__ == "__main__":
    game = Game()
    game.run()
```

### Key Improvements and Additions:

1. **Structured Classes**: Clearly defined `Spaceship`, `Alien`, and `Bullet` classes with properties and methods relevant to each entity.

2. **Game Mechanics**: Included basic logic structure for moving the entities, shooting, detecting collisions, and handling game loops.

3. **Sound Management**: A `SoundManager` class is included for playing sounds, though actual implementation is still needed.

4. **Data Persistence**: Functions to save and load high scores.

5. **Rendering and Display**: Simplified rendering and HUD logic placeholders; these would indeed need an actual rendering library to be fully functional (such as `tkinter`, `pygame`, or similar included graphics capabilities of Python).

6. **Game Flow**: A basic loop and structure to transition between states (play, pause, game over), though details would need actual implementation.

Please ensure you have the necessary libraries to handle sound, input, and display to complete the execution of the code. For a fully functioning game with graphics and sound, integrating a library like `pygame` would be advisable.


import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ALIEN_SPEED = 2
BULLET_SPEED = -5
SPACESHIP_SPEED = 5
INITIAL_LIVES = 3

pygame.init()

class GameObject:
    def __init__(self, x=0, y=0, speed=1):
        self.x = x
        self.y = y
        self.speed = speed

class Spaceship(GameObject):
    def __init__(self, lives, speed):
        super().__init__(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT-50, speed=speed)
        self.lives = lives

    def move_left(self):
        self.x = max(self.x - self.speed, 0)
    
    def move_right(self):
        self.x = min(self.x + self.speed, SCREEN_WIDTH)

    def shoot(self):
        return Bullet(self.x, self.y)

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, speed=BULLET_SPEED)

    def move(self):
        self.y += self.speed

class Alien(GameObject):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, speed=ALIEN_SPEED)

class AlienManager:
    def __init__(self):
        self.aliens = [Alien(x * 50, 50) for x in range(0, SCREEN_WIDTH//50)]

    def move_aliens(self):
        direction = self.determine_move_direction()
        for alien in self.aliens:
            alien.x += direction * alien.speed

    def determine_move_direction(self):
        if any(alien.x <= 0 for alien in self.aliens):
            return 1
        elif any(alien.x >= SCREEN_WIDTH for alien in self.aliens):
            return -1
        return random.choice([-1, 1])  # simple logic for side movement

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()

    def increase_score(self):
        self.score += 10
        self.high_score = max(self.score, self.high_score)

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

    def draw_game_objects(self, spaceship, aliens, bullets):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (spaceship.x, spaceship.y, 50, 30))
        for alien in aliens:
            pygame.draw.rect(self.screen, (0, 255, 0), (alien.x, alien.y, 40, 20))
        for bullet in bullets:
            pygame.draw.rect(self.screen, (255, 0, 0), (bullet.x, bullet.y, 5, 10))

    def display_text(self, text, position):
        font = pygame.font.Font(None, 26)
        render = font.render(text, True, (255, 255, 255))
        self.screen.blit(render, position)

    def update(self):
        pygame.display.flip()

class GameInitializer:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship(lives=INITIAL_LIVES, speed=SPACESHIP_SPEED)
        self.alien_manager = AlienManager()
        self.bullets = []
        self.score_manager = ScoreManager()
        self.screen = Screen()

    def run(self):
        while True:
            self.clock.tick(30)
            self.handle_input()
            self.update_game_state()
            self.update_display()
            self.check_collisions()
            if self.is_game_over():
                self.game_over()
                break

    def handle_input(self):
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

    def update_game_state(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        self.alien_manager.move_aliens()

    def update_display(self):
        self.screen.draw_game_objects(self.spaceship, self.alien_manager.aliens, self.bullets)
        self.screen.display_text(f'Score: {self.score_manager.score}', (10, 10))
        self.screen.display_text(f'Lives: {self.spaceship.lives}', (10, 40))
        self.screen.update()

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for alien in self.alien_manager.aliens[:]:
                if self.check_collision(bullet, alien):
                    self.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    self.score_manager.increase_score()
                    break

    def check_collision(self, bullet, alien):
        return alien.x < bullet.x < alien.x + 40 and alien.y < bullet.y < alien.y + 20
    
    def is_game_over(self):
        return any(alien.y >= self.spaceship.y for alien in self.alien_manager.aliens)

    def game_over(self):
        self.screen.display_text("GAME OVER", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
        self.screen.update()
        pygame.time.wait(2000)
        self.score_manager.save_high_score()
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameInitializer()
    game.run()



import random
import sys
import os

class GameEntity:
    def __init__(self, x, y, sprite, width, height):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = width
        self.height = height

    def draw(self):
        # Hypothetical graphics library usage
        graphics_library.draw_sprite(self.sprite, self.x, self.y, self.width, self.height)


class Spaceship(GameEntity):
    def __init__(self, x, y, sprite, bullet_sprite, width, height):
        super().__init__(x, y, sprite, width, height)
        self.lives = 3
        self.bullet_sprite = bullet_sprite

    def move_left(self):
        self.x = max(0, self.x - 5)

    def move_right(self):
        self.x = min(GameEngine.SCREEN_WIDTH - self.width, self.x + 5)

    def shoot(self):
        return Bullet(self.x + self.width // 2, self.y, self.bullet_sprite, 5, 5)


class Alien(GameEntity):
    def __init__(self, x, y, sprite, width, height):
        super().__init__(x, y, sprite, width, height)
        self.direction = 1

    def move(self):
        self.x += self.direction * 1
        if self.x <= 0 or self.x + self.width >= GameEngine.SCREEN_WIDTH:
            self.direction *= -1
            self.y += 5
        
    def check_collision(self, bullet):
        return (self.x < bullet.x < self.x + self.width and
                self.y < bullet.y < self.y + self.height)

    def handle_explosion(self):
        pass  # Play explosion animation


class Bullet(GameEntity):
    def __init__(self, x, y, sprite, width, height):
        super().__init__(x, y, sprite, width, height)

    def move(self):
        self.y -= 5
        return self.y > 0


class ScrollingBackground:
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.y = 0

    def scroll(self):
        self.y = (self.y + self.speed) % GameEngine.SCREEN_HEIGHT

    def draw(self):
        graphics_library.draw_image(self.image, 0, -self.y)


class InputManager:
    def process_input(self, spaceship):
        events = input_system.get_events()
        for event in events:
            if event.type == 'QUIT':
                GameEngine.exit_game()
            elif event.type == 'KEYDOWN':
                if event.key == 'LEFT':
                    spaceship.move_left()
                elif event.key == 'RIGHT':
                    spaceship.move_right()
                elif event.key == 'SPACE':
                    return spaceship.shoot()
        return None


class GameState:
    def __init__(self):
        self.current_state = 'Start'

    def change_state(self, new_state):
        self.current_state = new_state


class GameEngine:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self):
        self.spaceship = Spaceship(400, 550, 'spaceship_sprite', 'bullet_sprite', 50, 30)
        self.aliens = []
        self.bullets = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1
        self.is_paused = False
        self.background = ScrollingBackground('background_image', 1)
        self.input_manager = InputManager()
        self.state = GameState()

    def start_game(self):
        self.play_background_music()
        self.create_alien_formation()

    def create_alien_formation(self):
        for i in range(3):
            for j in range(7):
                self.aliens.append(Alien(j * 50 + 50, i * 40 + 50, 'alien_sprite', 40, 30))

    def run(self):
        self.start_game()
        while self.state.current_state != 'GameOver':
            bullet = self.input_manager.process_input(self.spaceship)
            if bullet:
                self.bullets.append(bullet)

            self.update_game_state()
            self.draw_game()

    def update_game_state(self):
        if self.is_paused:
            return

        for bullet in self.bullets[:]:
            if not bullet.move():
                self.bullets.remove(bullet)

        for alien in self.aliens[:]:
            alien.move()
            for bullet in self.bullets[:]:
                if alien.check_collision(bullet):
                    self.play_sound_effect('destroy')
                    self.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.score += 10

        for alien in self.aliens:
            if alien.y + alien.height > self.spaceship.y:
                self.play_sound_effect('game_over')
                self.state.change_state('GameOver')

    def draw_game(self):
        self.background.scroll()
        self.background.draw()
        self.spaceship.draw()
        for alien in self.aliens:
            alien.draw()
        for bullet in self.bullets:
            bullet.draw()

    def load_high_score(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            with open('high_score.txt', 'w') as file:
                file.write(str(self.score))

    def play_background_music(self):
        audio_system.play_music('background_music', loop=True)

    def play_sound_effect(self, action):
        if action == 'shoot':
            audio_system.play_sound('shoot_sound')
        elif action == 'destroy':
            audio_system.play_sound('destroy_sound')
        elif action == 'game_over':
            audio_system.play_sound('game_over_sound')

    def exit_game(self):
        self.save_high_score()
        sys.exit()

# Placeholder objects and methods
graphics_library = type('graphics', (object,), {"draw_sprite": lambda *args: None, "draw_image": lambda *args: None})
input_system = type('input', (object,), {"get_events": lambda: []})
audio_system = type('audio', (object,), {"play_music": lambda *args, **kwargs: None, "play_sound": lambda *args: None})

GameEngine().run()


