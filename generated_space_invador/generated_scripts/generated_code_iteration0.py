
import random

class Spaceship:
    """
    Class representing a spaceship in a game environment.
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
            file.write(str(high_score)

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



import random
import os
from typing import Any, List, Tuple

class Settings:
    """
    A class to manage all game settings and constants.
    """
    def __init__(self):
        """Initialize game settings and constants."""
        self.screen_width = 800
        self.screen_height = 600
        self.spaceship_speed = 5
        self.alien_initial_speed = 1
        self.alien_speed_increment = 0.5
        self.bullet_speed = 3


class Spaceship:
    """
    A class to represent the player's spaceship.
    """
    def __init__(self):
        """Initialize the spaceship with a default position and empty bullet list."""
        self.position = (400, 550)
        self.bullets: List[Bullet] = []

    def move(self, direction: str):
        """Move the spaceship left or right."""
        x, y = self.position
        if direction == 'left':
            x = max(x - Settings().spaceship_speed, 0)
        elif direction == 'right':
            x = min(x + Settings().spaceship_speed, 800)
        self.position = (x, y)

    def shoot(self):
        """Fire a bullet."""
        bullet_position = (self.position[0], self.position[1] - 10)
        bullet = Bullet(bullet_position)
        self.bullets.append(bullet)

    def reset_position(self):
        """Reset the spaceship to its default position."""
        self.position = (400, 550)


class Alien:
    """
    A class to represent an alien in the game.
    """
    def __init__(self, position: Tuple[int, int], alien_type: str, speed: int):
        self.position = position
        self.alien_type = alien_type
        self.speed = speed
        self.alive = True

    def move(self, direction: int):
        """Move the alien horizontally."""
        x, y = self.position
        x += direction * self.speed
        self.position = (x, y)

    def descend(self):
        """Descend the alien."""
        x, y = self.position
        self.position = (x, y + 10)


class Bullet:
    """
    A class to represent bullets in the game.
    """
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.active = True

    def update_position(self):
        """Update the bullet position."""
        x, y = self.position
        y -= 5  # Move the bullet upwards
        self.position = (x, y)

    def is_off_screen(self) -> bool:
        """Check if the bullet is off the screen."""
        return self.position[1] < 0

    def collides_with(self, obj) -> bool:
        """Check if the bullet collides with the given object."""
        # Simple collision logic (can be replaced with meaningful logic based on dimensions)
        return self.position == obj.position


class Game:
    """
    A class to manage game state and logic.
    """
    def __init__(self, settings: Settings):
        self.settings = settings
        self.spaceship = Spaceship()
        self.aliens: List[Alien] = self.initialize_aliens()
        self.alien_bullets: List[Bullet] = []
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.lives = 3
        self.paused = False
        self.game_over = False
        self.load_high_score()

    def start_screen(self):
        """Display the start screen."""
        print("Welcome to Space Invaders! Press 'Enter' to start.")
        input()

    def game_over_screen(self):
        """Display the game over screen."""
        print("Game Over! Press 'R' to restart or 'Q' to quit.")
        choice = input().lower()
        if choice == 'r':
            self.reset()
        elif choice == 'q':
            self.exit_game()

    def reset(self):
        """Reset the game state."""
        self.__init__(self.settings)

    def exit_game(self):
        """Exit the game."""
        self.save_high_score()
        self.game_over = True

    def pause(self):
        """Toggle the paused state."""
        self.paused = not self.paused

    def load_high_score(self):
        """Load the high score from a file."""
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                self.high_score = int(file.read().strip())
        else:
            self.high_score = 0

    def save_high_score(self):
        """Save the high score to a file."""
        with open('high_score.txt', 'w') as file:
            file.write(str(max(self.score, self.high_score)))

    def update(self):
        """Update the game state."""
        if not self.paused and not self.game_over:
            self.update_spaceship()
            self.update_aliens()
            self.update_alien_bullets()
            self.check_collisions()
            self.adjust_alien_position()
            self.update_level()

    def update_spaceship(self):
        """Update spaceship and its bullets."""
        for bullet in self.spaceship.bullets:
            bullet.update_position()
            if bullet.is_off_screen():
                self.spaceship.bullets.remove(bullet)

    def update_aliens(self):
        """Update alien positions."""
        for alien in self.aliens:
            alien.move(1)  # Move right
            if alien.is_at_edge():
                self.alien_descend_and_check_game_over()
                break

    def alien_descend_and_check_game_over(self):
        """Descend the aliens and check game over conditions."""
        for alien in self.aliens:
            alien.descend()
            if alien.reached_spaceship(self.spaceship.position):
                self.game_over = True

    def update_alien_bullets(self):
        """Update alien bullets positions."""
        for bullet in self.alien_bullets:
            bullet.update_position()
            if bullet.is_off_screen():
                self.alien_bullets.remove(bullet)

    def check_collisions(self):
        """Check for any collisions."""
        self.check_bullet_collisions()
        self.check_spaceship_collision()

    def check_bullet_collisions(self):
        """Check if spaceship bullets hit aliens."""
        for bullet in self.spaceship.bullets:
            for alien in self.aliens:
                if alien.alive and bullet.collides_with(alien):
                    bullet.active = False
                    alien.alive = False
                    self.score += 10
        self.spaceship.bullets = [b for b in self.spaceship.bullets if b.active]

    def check_spaceship_collision(self):
        """Check if any alien bullet hits spaceship."""
        for bullet in self.alien_bullets:
            if bullet.collides_with(self.spaceship):
                self.lives -= 1
                self.alien_bullets.remove(bullet)
                if self.lives <= 0:
                    self.game_over = True

    def adjust_alien_position(self):
        """Adjust alien position when reaching screen edges."""
        for alien in self.aliens:
            if alien.position[0] <= 0 or alien.position[0] >= self.settings.screen_width:
                for a in self.aliens:
                    a.descend()
                break

    def input_handler(self):
        """Process user inputs."""
        print("Processing input...")  # Placeholder for real input handling

    def update_level(self):
        """Check and handle level transitions."""
        if not any(alien.alive for alien in self.aliens):
            self.level += 1
            self.aliens = self.initialize_aliens()

    def initialize_aliens(self) -> List[Alien]:
        """Set up aliens for a new level."""
        aliens = []
        alien_types = ["basic", "advanced", "elite"]
        rows = 5
        columns = 10
        alien_speed = self.settings.alien_initial_speed + (self.level - 1) * self.settings.alien_speed_increment
        start_x, start_y = 50, 50
        x_gap, y_gap = 60, 50

        for row in range(rows):
            for col in range(columns):
                position = (start_x + col * x_gap, start_y + row * y_gap)
                alien_type = alien_types[row % len(alien_types)]
                aliens.append(Alien(position, alien_type, alien_speed))
        return aliens

    def display_stats(self):
        """Render and display the current game stats."""
        num_aliens = sum(alien.alive for alien in self.aliens)
        stats = (
            f"Score: {self.score}",
            f"High Score: {self.high_score}",
            f"Level: {self.level}",
            f"Lives: {self.lives}",
            f"Remaining Aliens: {num_aliens}"
        )
        for stat in stats:
            print(stat)

    def run(self):
        """Run the game loop."""
        self.start_screen()
        while not self.game_over:
            self.input_handler()
            self.update()
            self.draw()

    def draw(self):
        """Draw all game elements."""
        print("Drawing game state...")
        self.display_stats()
        self.spaceship.draw()
        for alien in self.aliens:
            alien.draw()
        for bullet in self.spaceship.bullets + self.alien_bullets:
            bullet.draw()


