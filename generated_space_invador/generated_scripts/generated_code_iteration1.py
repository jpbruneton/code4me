
import random

class Spaceship:
    """
    Class representing a spaceship in the game environment.
    """

    def __init__(self, x_pos=0, y_pos=0):
        """
        Initialize a Spaceship object with the given x and y positions.
        
        Args:
            x_pos (int): Current x position of the spaceship.
            y_pos (int): Current y position of the spaceship.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move_left(self):
        """
        Move the spaceship to the left.
        """
        self.x_pos -= 1

    def move_right(self):
        """
        Move the spaceship to the right.
        """
        self.x_pos += 1

    def shoot(self):
        """
        Make the spaceship shoot a bullet.
        """
        # Implementation for shooting a bullet

    def handle_collision(self, bullets, aliens):
        """
        Handle collision between spaceship bullets and aliens.
        
        Args:
            bullets (List): List of Bullet objects.
            aliens (List): List of Alien objects.
        """
        # Implementation for collision handling

    def handle_spaceship_collision(self, aliens):
        """
        Function to handle collision between aliens and the spaceship.
        
        Args:
            aliens (List): List of Alien objects.
        """
        # Implementation for spaceship collision handling


class Alien:
    """
    Class representing an alien entity in a game environment.
    """

    def __init__(self, x_pos=0, y_pos=0):
        """
        Initialize an Alien object with the given x and y positions.
        
        Args:
            x_pos (int): Current x position of the alien.
            y_pos (int): Current y position of the alien.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_alive = True

    def move(self):
        """
        Move the alien left or right.
        """
        # Implementation for moving the alien

    def descend(self):
        """
        Make the alien descend down the screen.
        """
        # Implementation for making the alien descend

    def handle_collision(self, spaceship):
        """
        Function to handle the logic when an alien reaches the spaceship.
        
        Args:
            spaceship (Spaceship): Spaceship object that the alien collides with.
        """
        # Implementation for handling collision with the spaceship


class Bullet:
    """
    Class representing a bullet fired in the game environment.
    """

    def __init__(self, x_pos=0, y_pos=0):
        """
        Initialize a Bullet object with the given x and y positions.

        Args:
            x_pos (int): Current x position of the bullet.
            y_pos (int): Current y position of the bullet.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.is_active = True

    def move(self):
        """
        Move the bullet in the game space.
        """
        # Implementation for moving the bullet


class GameStateManager:
    """
    Class responsible for managing the game state and screens, including gameplay logic.
    """

    def __init__(self):
        """
        Initialize a GameStateManager object with default game settings.
        """
        self.current_screen = "main_menu"
        self.is_game_over = False
        self.player_score = 0
        self.high_score = self.load_high_score()
        self.current_level = 1
        self.player_lives = 3
        self.remaining_aliens = 0
        self.spaceship = Spaceship()
        self.aliens = []
        self.bullets = []

    def change_screen(self, new_screen):
        """
        Change the current screen being displayed to the new screen.

        Args:
            new_screen (String): The screen to switch to.
        """
        self.current_screen = new_screen

    def start_game(self):
        """
        Start the game and display the main game screen.
        """
        self.change_screen("game_screen")
        self.restart_game()

    def end_game(self):
        """
        End the game and display the game over screen.
        """
        self.change_screen("game_over_screen")
        self.is_game_over = True

    def restart_game(self):
        """
        Restart the game with initial settings and display the start screen.
        """
        self.player_score = 0
        self.current_level = 1
        self.player_lives = 3
        self.spaceship = Spaceship()
        self.aliens = []
        self.bullets = []

    def run(self):
        """
        Main function to run the Space Invaders game.
        """
        self.start_game()
        
        while not self.is_game_over:
            self.handle_player_input()
            self.update_game_state()
            self.display_game()

    def handle_player_input(self):
        """
        Handle player input for controlling the spaceship.
        """
        # Logic for handling player input goes here

    def update_game_state(self):
        """
        Update the game state based on player input and game events.
        """
        # Logic to update game entities, check collisions, etc.

    def display_game(self):
        """
        Display the game graphics and information on the screen.
        """
        display_game_graphics(self.spaceship, self.aliens, self.bullets)
        display_game_info(self.player_score, self.high_score, self.current_level, self.player_lives, self.remaining_aliens)

    def load_high_score(self):
        """
        Load the high score from a file.
        """
        try:
            with open('high_score.txt', 'r') as file:
                high_score = int(file.read().strip())
        except FileNotFoundError:
            high_score = 0
        return high_score

    def save_high_score(self, high_score):
        """
        Save the high score to a file.

        Args:
            high_score (int): The high score to save.
        """
        with open('high_score.txt', 'w') as file:
            file.write(str(high_score))

def display_game_graphics(spaceship, aliens, bullets):
    """
    Display the game graphics for spaceship, aliens, and bullets.
    """
    # Implementation for displaying game graphics

def display_game_info(score, high_score, level, lives, remaining_aliens):
    """
    Display game information including score, high score, level, lives, and remaining aliens.
    """
    # Implementation for displaying game information




import os
from typing import Any, List, Tuple

class Settings:
    """Class to handle game configurations."""
    # Initializing game constants.
    WIDTH, HEIGHT = 800, 600
    SPACESHIP_SPEED = 5
    ALIEN_INITIAL_SPEED = 1
    ALIEN_SPEED_INCREMENT = 0.5
    BULLET_SPEED = -5

class Position:
    """Utility class to manage x, y coordinates."""
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

class Bullet:
    """Represents a bullet shot by the spaceship."""
    def __init__(self, pos: Position):
        self.pos = pos
        self.active = True

    def update(self):
        # Move the bullet up.
        self.pos.move(0, Settings.BULLET_SPEED)

    def is_off_screen(self) -> bool:
        return self.pos.y < 0 or self.pos.y > Settings.HEIGHT

class Spaceship:
    """Represents the player's spaceship."""
    def __init__(self):
        self.pos = Position(Settings.WIDTH // 2, Settings.HEIGHT - 50)
        self.bullets: List[Bullet] = []

    def move(self, direction: str):
        if direction == 'left':
            new_x = max(self.pos.x - Settings.SPACESHIP_SPEED, 0)
        else:  # right
            new_x = min(self.pos.x + Settings.SPACESHIP_SPEED, Settings.WIDTH)
        self.pos.move(new_x - self.pos.x, 0)

    def shoot(self):
        """Fire a bullet."""
        bullet_pos = Position(self.pos.x, self.pos.y - 10)
        self.bullets.append(Bullet(bullet_pos))

    def update_bullets(self):
        # Update and remove off-screen bullets.
        for bullet in self.bullets.copy():
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

class Alien:
    """Represents an alien invader."""
    def __init__(self, pos: Position, speed: int):
        self.pos = pos
        self.speed = speed
        self.alive = True

    def move(self, direction: int):
        """Move the alien horizontally."""
        self.pos.move(direction * self.speed, 0)

    def descend(self):
        """Descend the alien."""
        self.pos.move(0, 10)

class Game:
    """Central class to manage the game's state and logic."""
    def __init__(self):
        self.settings = Settings()
        self.spaceship = Spaceship()
        self.aliens, self.current_direction = self.setup_aliens(), 1
        self.score, self.high_score = 0, self.load_high_score()
        self.level, self.lives, self.paused, self.game_over = 1, 3, False, False

    def setup_aliens(self) -> List[Alien]:
        aliens = []
        start_x, start_y, x_gap, y_gap = 50, 50, 60, 50
        speed = Settings.ALIEN_INITIAL_SPEED + (self.level - 1) * Settings.ALIEN_SPEED_INCREMENT
        for row in range(5):  # 5 rows of aliens
            for col in range(10):  # 10 columns in each row
                position = Position(start_x + col * x_gap, start_y + row * y_gap)
                aliens.append(Alien(position, speed))
        return aliens

    def load_high_score(self) -> int:
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            with open('high_score.txt', 'w') as file:
                file.write(str(self.score))
    
    def adjust_aliens(self):
        edge_hit = any(alien for alien in self.aliens if alien.pos.x <= 0 or alien.pos.x >= Settings.WIDTH - 40)
        if edge_hit:
            for alien in self.aliens:
                alien.descend()
            self.current_direction *= -1

    def check_collisions(self):
        for bullet in self.spaceship.bullets:
            for alien in self.aliens:
                if alien.alive and bullet.pos.x == alien.pos.x and bullet.pos.y == alien.pos.y:
                    bullet.active = False
                    alien.alive = False
                    self.score += 10

    def update_game_state(self):
        self.spaceship.update_bullets()
        self.aliens = [alien for alien in self.aliens if alien.alive]
        if not self.aliens:
            self.level += 1
            self.aliens = self.setup_aliens()

    def run_game(self):
        print("Welcome to Space Invaders! Press 'Enter' to start.")
        input()
        while not self.game_over:
            self.handle_input()
            if not self.paused:
                self.update_game_state()
                self.adjust_aliens()
                self.save_high_score()
            if self.lives <= 0 or any(alien.pos.y >= self.spaceship.pos.y for alien in self.aliens):
                self.game_over = True
                self.display_game_over_screen()

    def handle_input(self):
        # Placeholder for user input logic
        pass

    def display_game_over_screen(self):
        print(f"Game Over! Final Score: {self.score}")
        print("Press 'R' to restart or 'Q' to quit.")
        while True:
            choice = input().lower()
            if choice == 'r':
                self.__init__()
                self.run_game()
                break
            elif choice == 'q':
                break

if __name__ == "__main__":
    game = Game()
    game.run_game()


