
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
        # To be implemented later

    def handle_collision(self, bullets, aliens):
        """
        Handle collision between spaceship bullets and aliens.
        
        Args:
            bullets (List): List of Bullet objects.
            aliens (List): List of Alien objects.
        """
        # To be implemented later

    def handle_spaceship_collision(self, aliens):
        """
        Function to handle collision between aliens and the spaceship.
        
        Args:
            aliens (List): List of Alien objects.
        """
        # To be implemented later


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
        # To be implemented later

    def descend(self):
        """
        Make the alien descend down the screen.
        """
        # To be implemented later

    def handle_collision(self, spaceship):
        """
        Function to handle the logic when an alien reaches the spaceship.
        
        Args:
            spaceship (Spaceship): Spaceship object that the alien collides with.
        """
        # To be implemented later


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
        # To be implemented later


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
        # To be implemented later

    def update_game_state(self):
        """
        Update the game state based on player input and game events.
        """
        # To be implemented later

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
    # To be implemented later

def display_game_info(score, high_score, level, lives, remaining_aliens):
    """
    Display game information including score, high score, level, lives, and remaining aliens.
    """
    # To be implemented later


import os
from typing import List

class Settings:
    WIDTH, HEIGHT = 800, 600
    SPACESHIP_SPEED = 5
    ALIEN_INITIAL_SPEED = 1
    ALIEN_SPEED_INCREMENT = 0.5
    BULLET_SPEED = -5
    ALIEN_DESCENT_STEP = 10
    ALIEN_BOUNDARY = 40

class Position:
    def __init__(self, x: int, y: int):
        """
        Represents a position in 2D space.
        
        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
        """
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        """
        Move the position by dx and dy.
        
        Args:
            dx (int): Change in x-coordinate.
            dy (int): Change in y-coordinate.
        """
        self.x += dx
        self.y += dy

class Bullet:
    def __init__(self, pos: Position):
        """
        Represents a bullet in the game.
        
        Args:
            pos (Position): Initial position of the bullet.
        """
        self.pos = pos
        self.active = True

    def update(self):
        """
        Update the bullet's position, moving it upwards.
        """
        self.pos.move(0, Settings.BULLET_SPEED)

    def is_off_screen(self) -> bool:
        """
        Check if the bullet is off the screen.
        
        Returns:
            bool: True if off screen, False otherwise.
        """
        return self.pos.y < 0

class Spaceship:
    def __init__(self):
        """
        Represents the spaceship controlled by the player.
        """
        self.pos = Position(Settings.WIDTH // 2, Settings.HEIGHT - 50)
        self.bullets: List[Bullet] = []

    def move(self, direction: str):
        """
        Move the spaceship left or right.
        
        Args:
            direction (str): Direction to move ('left' or 'right').
        """
        if direction == 'left':
            new_x = max(self.pos.x - Settings.SPACESHIP_SPEED, 0)
        elif direction == 'right':
            new_x = min(self.pos.x + Settings.SPACESHIP_SPEED, Settings.WIDTH)
        self.pos.move(new_x - self.pos.x, 0)

    def shoot(self):
        """
        Shoot a bullet from the spaceship.
        """
        bullet_pos = Position(self.pos.x, self.pos.y - 10)
        self.bullets.append(Bullet(bullet_pos))

    def update_bullets(self):
        """
        Update all bullets, removing those that are off-screen.
        """
        for bullet in self.bullets.copy():
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

class Alien:
    def __init__(self, pos: Position, speed: int):
        """
        Represents an alien in the game.
        
        Args:
            pos (Position): Initial position of the alien.
            speed (int): Speed of the alien movement.
        """
        self.pos = pos
        self.speed = speed
        self.alive = True

    def move(self, direction: int):
        """
        Move the alien horizontally.
        
        Args:
            direction (int): Direction to move (-1 for left, 1 for right).
        """
        self.pos.move(direction * self.speed, 0)

    def descend(self):
        """
        Move the alien one step downwards.
        """
        self.pos.move(0, Settings.ALIEN_DESCENT_STEP)

class Game:
    def __init__(self):
        """
        Main game class managing the game state and logic.
        """
        self.spaceship = Spaceship()
        self.aliens, self.current_direction = self.setup_aliens(), 1
        self.score, self.high_score = 0, self.load_high_score()
        self.level, self.lives, self.paused, self.game_over = 1, 3, False, False

    def setup_aliens(self) -> List[Alien]:
        """
        Setup the initial positions and state of the alien invaders.
        
        Returns:
            List[Alien]: A list of alien objects.
        """
        aliens = []
        start_x, start_y, x_gap, y_gap = 50, 50, 60, 50
        speed = Settings.ALIEN_INITIAL_SPEED + (self.level - 1) * Settings.ALIEN_SPEED_INCREMENT
        for row in range(5):
            for col in range(10):
                position = Position(start_x + col * x_gap, start_y + row * y_gap)
                aliens.append(Alien(position, speed))
        return aliens

    def load_high_score(self) -> int:
        """
        Load the high score from a file.
        
        Returns:
            int: The saved high score.
        """
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        """
        Save the current score as high score if it exceeds the previous high score.
        """
        if self.score > self.high_score:
            with open('high_score.txt', 'w') as file:
                file.write(str(self.score))

    def adjust_aliens(self):
        """
        Adjust aliens' positions and direction after hitting the screen edge.
        """
        edge_hit = any(alien.pos.x <= 0 or alien.pos.x >= Settings.WIDTH - Settings.ALIEN_BOUNDARY for alien in self.aliens)
        if edge_hit:
            for alien in self.aliens:
                alien.descend()
            self.current_direction *= -1

    def check_collisions(self):
        """
        Check and handle collisions between bullets and aliens.
        """
        for bullet in self.spaceship.bullets.copy():
            for alien in self.aliens.copy():
                if alien.alive and self.collision_detected(bullet.pos, alien.pos):
                    bullet.active = False
                    alien.alive = False
                    self.score += 10
                    self.spaceship.bullets.remove(bullet)
                    self.aliens.remove(alien)

    def collision_detected(self, bullet_pos: Position, alien_pos: Position) -> bool:
        """
        Detect collision between a bullet and an alien.
        
        Args:
            bullet_pos (Position): The position of the bullet.
            alien_pos (Position): The position of the alien.
        
        Returns:
            bool: True if collision is detected, False otherwise.
        """
        return bullet_pos.x == alien_pos.x and bullet_pos.y == alien_pos.y

    def update_game_state(self):
        """
        Update the game state, including bullets and checking for collisions.
        """
        self.spaceship.update_bullets()
        self.check_collisions()
        if not any(alien.alive for alien in self.aliens):
            self.level += 1
            self.aliens = self.setup_aliens()

    def run_game(self):
        """
        Main game loop.
        """
        print("Welcome to Space Invaders! Press 'Enter' to start.")
        input()
        while not self.game_over:
            self.handle_input()
            if not self.paused:
                self.update_game_state()
                self.adjust_aliens()
            self.check_game_over()

    def handle_input(self):
        """
        Placeholder for handling player inputs (to be implemented with actual input handling).
        """
        pass

    def check_game_over(self):
        """
        Check for game over conditions and proceed to appropriate handling.
        """
        if self.lives <= 0 or any(alien.pos.y >= self.spaceship.pos.y for alien in self.aliens):
            self.game_over = True
            self.display_game_over_screen()

    def display_game_over_screen(self):
        """
        Show the game over screen, allowing the user to restart or quit.
        """
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


