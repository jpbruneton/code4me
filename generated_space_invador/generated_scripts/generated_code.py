
class Settings:
    """
    A class to manage all game settings and constants.
    """

    def __init__(self):
        """Initialize game settings and constants."""
        self.screen_width = 800
        self.screen_height = 600
        self.spaceship_speed = 2
        self.alien_initial_speed = 1
        self.alien_speed_increment = 1
        self.bullet_speed = 3



import random
from typing import Any, List

class Game:
    """
    A class to manage the state and behavior of the game.
    """
    
    def __init__(self, settings: Settings):
        """Initialize the game state with default values."""
        self.spaceship = Spaceship()
        self.aliens: List[Alien] = []
        self.alien_bullets: List[Bullet] = []
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.lives = 3
        self.paused = False
        self.game_over = False
        self.graphics: dict[str, Any] = {}
        self.settings = settings
    
    def start_screen(self):
        """Display the start screen and wait for the user to start the game."""
        # Here would go logic to display the start screen and wait for input.
        print("Welcome to the Alien Adventure Game! Press 'Enter' to start.")
        input()  # Placeholder for capturing the start input
    
    def game_over_screen(self):
        """Display the game over screen and offer the option to restart."""
        # Logic for displaying the game-over screen and asking for restart.
        print("Game Over! Press 'R' to retry or 'Q' to quit.")
        choice = input()
        if choice.lower() == 'r':
            self.reset()
        elif choice.lower() == 'q':
            self.exit()
    
    def reset(self):
        """Reset the game to its initial state without closing the application."""
        self.__init__(self.settings)  # Re-initialize with current settings
    
    def restart_level(self):
        """Restart the current level, resetting the aliens and spaceship state."""
        self.aliens.clear()  # Clear current aliens
        self.spaceship.reset_position()  # Reset spaceship
        # No score or lives changes, simply refresh level state.
    
    def pause(self):
        """Toggle the paused state of the game."""
        self.paused = not self.paused
    
    def update(self):
        """Update the game state, including spaceship, aliens, collisions, and score."""
        if not self.paused and not self.game_over:
            self.update_spaceship()
            self.update_aliens()
            self.update_alien_bullets()
            self.check_collisions()
            self.adjust_position()
    
    def draw(self):
        """Draw all game elements on screen, including spaceship, aliens, score, etc."""
        # Logic for drawing all elements.
        print(f"Drawing Game State. Score: {self.score}")
    
    def run(self):
        """Main loop to execute the game, manage timing, and handle exits."""
        while not self.game_over:
            self.input_handler()
            self.update()
            self.draw()
    
    def check_collisions(self):
        """Check for collisions between bullets and aliens, update score."""
        # Placeholder for collision detection
        for bullet in self.spaceship.bullets:
            for alien in self.aliens:
                if bullet.collides_with(alien):
                    self.score += 10  # Increase score
                    self.aliens.remove(alien)
                    self.spaceship.bullets.remove(bullet)
    
    def check_spaceship_collision(self):
        """Check if any alien bullet collided with the spaceship."""
        for bullet in self.alien_bullets:
            if bullet.collides_with(self.spaceship):
                self.lives -= 1
                self.alien_bullets.remove(bullet)
                if self.lives <= 0:
                    self.game_over = True
    
    def save_high_score(self):
        """Save the high score to a file."""
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))
    
    def load_high_score(self):
        """Load the high score from a file."""
        try:
            with open('high_score.txt', 'r') as f:
                self.high_score = int(f.read())
        except FileNotFoundError:
            self.high_score = 0
    
    def adjust_position(self):
        """Align alien movement when reaching screen edges."""
        # Placeholder to adjust alien position.
        for alien in self.aliens:
            if alien.is_at_edge():
                for a in self.aliens:
                    a.descend()
    
    def input_handler(self):
        """Process user input."""
        # Placeholder for input handling logic.
        print("Processing input..")
    
    def load_graphics(self):
        """Load graphics for spaceship, aliens, and bullets."""
        self.graphics = {
            'spaceship': 'spaceship_graphic',
            'alien': 'alien_graphic',
            'bullet': 'bullet_graphic'
        }
    
    def update_level(self):
        """Increase the level when all aliens are destroyed."""
        if not self.aliens:
            self.level += 1
            self.increase_difficulty()
    
    def alien_descend_and_check_game_over(self):
        """Make aliens descend and check if they reach the spaceship."""
        for alien in self.aliens:
            alien.descend()
            if alien.reached_spaceship():
                self.game_over = True
    
    def check_bullet_hits_spaceship(self):
        """Determine if any bullet hits the spaceship."""
        for bullet in self.alien_bullets:
            if bullet.collides_with(self.spaceship):
                self.lives -= 1
                self.alien_bullets.remove(bullet)
    
    def update_alien_bullets(self):
        """Update the positions of alien bullets."""
        for bullet in self.alien_bullets:
            bullet.update_position()
            if bullet.is_off_screen():
                self.alien_bullets.remove(bullet)
    
    def manage_graphics(self):
        """Handle updating graphics and animations."""
        # Placeholder for managing game graphics.
        print("Updating graphics...")
    
    def serialize_game_state(self):
        """Serialize the game state for pause and resume functionality."""
        game_state = {
            'score': self.score,
            'level': self.level,
            'lives': self.lives,
            'aliens': self.aliens,  # Assuming aliens are serializable
            'spaceship': self.spaceship,  # Assuming spaceship is serializable
        }
        return game_state
    
    def deserialize_game_state(self, game_state):
        """Deserialize the game state to resume functionality."""
        self.score = game_state['score']
        self.level = game_state['level']
        self.lives = game_state['lives']
        self.aliens = game_state['aliens']
        self.spaceship = game_state['spaceship']
    
    def retry_logic(self):
        """Allow players to retry from the last level."""
        # Implement retry logic based on levels and lives.
        self.lives = 3  # Reset lives
        self.restart_level()
    
    def increase_difficulty(self):
        """Increase game difficulty parameters."""
        self.settings.alien_initial_speed += 0.5 * self.level



class Spaceship:
    """
    A class to represent the player's spaceship in the game.
    Handles spaceship's position, bullets, movement, and drawing.
    """

    def __init__(self):
        """Initialize the spaceship with a default position and empty bullet list."""
        self.position = (400, 550)  # Default starting position at the bottom center of the screen.
        self.bullets = []  # List to manage bullets fired by the spaceship.

    def move(self, direction: str):
        """
        Change the spaceship's position based on input direction.
        :param direction: 'left' or 'right' indicating the movement direction.
        """
        x, y = self.position
        if direction == 'left':
            x = max(x - 5, 0)  # Move left but don't go off-screen.
        elif direction == 'right':
            x = min(x + 5, 800)  # Move right but stay within screen limits.
        self.position = (x, y)

    def shoot(self):
        """Fire a bullet from the spaceship's current position."""
        # Bullet will appear just above the spaceship.
        bullet_position = (self.position[0], self.position[1] - 10)
        bullet = Bullet(bullet_position)  # Assumes Bullet is a class that can be initialized with a position.
        self.bullets.append(bullet)

    def draw(self):
        """Draw the spaceship at its current position."""
        # Placeholder for drawing logic - Printing position for now.
        print(f"Drawing spaceship at position {self.position}")



import random

class Alien:
    """
    A class to represent an alien in the game.
    Handles alien's position, state, type, speed, moving, drawing, and shooting mechanics.
    """
    def __init__(self, position: tuple[int, int], alien_type: str, speed: int):
        """
        Initialize the alien at a given position, marked as alive with a type and speed.
        :param position: Initial position of the alien as a (x, y) tuple.
        :param alien_type: The type/category of the alien (e.g., "basic").
        :param speed: The speed at which the alien moves.
        """
        self.position = position
        self.alive = True  # Marks the alien as alive.
        self.alien_type = alien_type
        self.speed = speed

    def move(self):
        """
        Update the alien's position. The alien moves horizontally, and possibly descends.
        """
        x, y = self.position
        # Logic to move the alien horizontally
        x += self.speed
        # Suppose aliens descend vertically by a fixed small amount whenever moving.
        # In a real game, logic would vary based on game state.
        self.position = (x, y)

    def draw(self):
        """
        Draw the alien at its current position if it is alive.
        """
        if self.alive:
            print(f"Drawing alien of type {self.alien_type} at position {self.position}")

    def alien_shoot(self):
        """
        Implement alien shooting random bullets towards the spaceship.
        The bullet is shot only if the alien is still alive.
        """
        if self.alive:
            # Randomly determine if the alien will shoot
            if random.random() < 0.1:  # 10% chance of shooting when called
                bullet_position = (self.position[0], self.position[1] + 10)  # Below the alien
                bullet = Bullet(bullet_position)  # assuming Bullet can be created with a position
                # Note: In practice, you'd need access to the game's bullet list or some manager
                print(f"Alien of type {self.alien_type} shooting bullet from {bullet_position}")




class Bullet:
    """
    A class to represent bullets in the game.
    Handles the bullet's position, active state, movement, and drawing.
    """
    
    def __init__(self, position: tuple[int, int]):
        """
        Initialize a bullet at a given position, marked as active.
        :param position: The starting position of the bullet.
        """
        self.position = position
        self.active = True  # The bullet is active upon creation

    def move(self):
        """
        Update the bullet's position, moving it upwards on the screen.
        """
        x, y = self.position
        # Move the bullet upwards
        y -= 5
        self.position = (x, y)

    def draw(self):
        """
        Draw the bullet at its current position if it is active.
        """
        if self.active:
            print(f"Drawing bullet at position {self.position}")

    def deactivate_if_out_of_bounds(self, screen_height: int):
        """
        Deactivate the bullet if it exits the screen.
        :param screen_height: The height of the game screen.
        """
        _, y = self.position
        # Deactivate bullet if it is above the screen
        if y < 0:
            self.active = False



def handle_events(self, events: list[Any]) -> None:
    """
    Manage input events such as keyboard presses for spaceship movement,
    shooting, pausing, and exiting.
    
    :param events: List of events to process.
    """
    for event in events:
        if event.type == 'QUIT':
            self.game_over = True
        
        if event.type == 'KEYDOWN':
            if event.key == 'LEFT':
                self.spaceship.move('left')
            elif event.key == 'RIGHT':
                self.spaceship.move('right')
            elif event.key == 'SPACE':
                self.spaceship.shoot()
            elif event.key == 'P':
                self.pause()
            elif event.key == 'Q':
                self.game_over = True



def remove_inactive_bullets(self):
    """
    Remove bullets from the spaceship and alien bullet list if they are inactive
    or out of bounds to optimize performance.
    """
    self.spaceship.bullets = [
        bullet for bullet in self.spaceship.bullets if bullet.active]
    self.alien_bullets = [
        bullet for bullet in self.alien_bullets if bullet.active]



def update_bullets(self, bullets: list[Bullet], aliens: list[Alien]) -> None:
    """
    Update the positions of all active bullets and handle collision detection with aliens.
    
    :param bullets: List of bullets to update and check for collisions.
    :param aliens: List of aliens to check for collisions with bullets.
    """
    for bullet in bullets:
        bullet.move()  # Update bullet position
        # Check if bullet is off-screen and mark it as inactive if so
        if bullet.position[1] < 0:
            bullet.active = False
            
    # Handle bullet collisions with aliens
    for bullet in bullets:
        if bullet.active:  # Only check active bullets
            for alien in aliens:
                if alien.alive and bullet.collides_with(alien):
                    alien.alive = False  # Mark alien as dead
                    bullet.active = False  # Deactivate the bullet
                    self.score += 10  # Increase score by 10 for each hit
    # Remove inactive bullets for better performance
    bullets[:] = [bullet for bullet in bullets if bullet.active]



def initialize_aliens(self) -> list[Alien]:
    """
    Set up the initial positions and states of all aliens for a new level.
    :return: A list of Alien objects initialized with positions and default attributes.
    """
    initial_aliens = []
    alien_types = ["basic", "advanced", "elite"]
    rows = 5
    columns = 10
    alien_speed = self.settings.alien_initial_speed
    
    # Spacing between aliens
    start_x = 50
    start_y = 50
    x_gap = 60
    y_gap = 50
    
    for row in range(rows):
        for col in range(columns):
            position = (start_x + col * x_gap, start_y + row * y_gap)
            alien_type = alien_types[row % len(alien_types)]
            alien = Alien(position, alien_type, alien_speed)
            initial_aliens.append(alien)
    
    return initial_aliens



def display_stats(self) -> None:
    """
    Render the current score, high score, level, number of lives, 
    and remaining aliens on the screen.
    """
    num_aliens = len([alien for alien in self.aliens if alien.alive])
    stats = (
        f"Score: {self.score}",
        f"High Score: {self.high_score}",
        f"Level: {self.level}",
        f"Lives: {self.lives}",
        f"Remaining Aliens: {num_aliens}"
    )
    # Display each stat in a user-friendly manner
    for stat in stats:
        print(stat)


