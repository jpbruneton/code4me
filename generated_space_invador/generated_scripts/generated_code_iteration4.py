
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
        pass

    def handle_collision(self, bullets, aliens):
        """
        Handle collision between spaceship bullets and aliens.
        
        Args:
            bullets (List): List of Bullet objects.
            aliens (List): List of Alien objects.
        """
        pass

    def handle_spaceship_collision(self, aliens):
        """
        Function to handle collision between aliens and the spaceship.
        
        Args:
            aliens (List): List of Alien objects.
        """
        pass


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
        pass

    def descend(self):
        """
        Make the alien descend down the screen.
        """
        pass

    def handle_collision(self, spaceship):
        """
        Function to handle the logic when an alien reaches the spaceship.
        
        Args:
            spaceship (Spaceship): Spaceship object that the alien collides with.
        """
        pass


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
        pass


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
        pass

    def update_game_state(self):
        """
        Update the game state based on player input and game events.
        """
        pass

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
    pass

def display_game_info(score, high_score, level, lives, remaining_aliens):
    """
    Display game information including score, high score, level, lives, and remaining aliens.
    """
    pass



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
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

class Bullet:
    def __init__(self, pos: Position):
        self.pos = pos
        self.active = True

    def update(self):
        self.pos.move(0, Settings.BULLET_SPEED)

    def is_off_screen(self) -> bool:
        return self.pos.y < 0

class Spaceship:
    def __init__(self):
        self.pos = Position(Settings.WIDTH // 2, Settings.HEIGHT - 50)
        self.bullets: List[Bullet] = []

    def move(self, direction: str):
        if direction == 'left':
            new_x = max(self.pos.x - Settings.SPACESHIP_SPEED, 0)
        elif direction == 'right':
            new_x = min(self.pos.x + Settings.SPACESHIP_SPEED, Settings.WIDTH)
        self.pos.move(new_x - self.pos.x, 0)

    def shoot(self):
        bullet_pos = Position(self.pos.x, self.pos.y - 10)
        self.bullets.append(Bullet(bullet_pos))

    def update_bullets(self):
        for bullet in self.bullets.copy():
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

class Alien:
    def __init__(self, pos: Position, speed: int):
        self.pos = pos
        self.speed = speed
        self.alive = True

    def move(self, direction: int):
        self.pos.move(direction * self.speed, 0)

    def descend(self):
        self.pos.move(0, Settings.ALIEN_DESCENT_STEP)

class Game:
    def __init__(self):
        self.spaceship = Spaceship()
        self.aliens, self.current_direction = self.setup_aliens(), 1
        self.score, self.high_score = 0, self.load_high_score()
        self.level, self.lives, self.paused, self.game_over = 1, 3, False, False

    def setup_aliens(self) -> List[Alien]:
        aliens = []
        start_x, start_y, x_gap, y_gap = 50, 50, 60, 50
        speed = Settings.ALIEN_INITIAL_SPEED + (self.level - 1) * Settings.ALIEN_SPEED_INCREMENT
        for row in range(5):
            for col in range(10):
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
        edge_hit = any(alien.pos.x <= 0 or alien.pos.x >= Settings.WIDTH - Settings.ALIEN_BOUNDARY for alien in self.aliens)
        if edge_hit:
            for alien in self.aliens:
                alien.descend()
            self.current_direction *= -1

    def check_collisions(self):
        for bullet in self.spaceship.bullets.copy():
            for alien in self.aliens.copy():
                if alien.alive and self.collision_detected(bullet.pos, alien.pos):
                    bullet.active = False
                    alien.alive = False
                    self.score += 10
                    self.spaceship.bullets.remove(bullet)
                    self.aliens.remove(alien)

    def collision_detected(self, bullet_pos: Position, alien_pos: Position) -> bool:
        return (abs(bullet_pos.x - alien_pos.x) < 10 and
                abs(bullet_pos.y - alien_pos.y) < 10)

    def update_game_state(self):
        self.spaceship.update_bullets()
        self.check_collisions()
        if not any(alien.alive for alien in self.aliens):
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
            self.check_game_over()
        
        self.save_high_score()

    def handle_input(self):
        # Placeholder for handling player inputs, to be implemented with actual input handling.
        pass

    def check_game_over(self):
        if self.lives <= 0 or any(alien.pos.y >= self.spaceship.pos.y for alien in self.aliens if alien.alive):
            self.game_over = True
            self.display_game_over_screen()

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


