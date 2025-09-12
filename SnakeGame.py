import random
from time import sleep
import os
import keyboard
from typing import Optional

# This random project is a simple snake game from scratch



class Body():
    
    '''
    Body class for the snake
    '''

    class link():

        '''
        Link class for the snake body
        '''
        def __init__(self, x_coordinates : int, y_coordinates : int, next_link : Optional['Body.link'] = None,
                     prev_link : Optional['Body.link'] = None) -> None:

            '''
            Initialize a link in the snake body
            Args:
                coordinates (list[int, int]): The x, y coordinates of the link
                next_link (link, optional): The next link in the body
                prev_link (link, optional): The previous link in the body
            '''

            self.x_coordinates = x_coordinates
            self.y_coordinates = y_coordinates
            self.next_link = next_link
            self.prev_link = prev_link



    def __init__(self, board_length : int, board_width : int) -> None:

        # Head starts in the middle of the 2d array
        self.head : Body.link = self.link(x_coordinates = board_width // 2, 
                                          y_coordinates = board_length // 2)
        self.coordinates_dict : dict[Body.link, list[int]] = {self.head : [self.head.x_coordinates, 
                                                                           self.head.y_coordinates]}

    
    def add_link(self, change : list[int]) -> None:

        # Move head to new position
        self.head.x_coordinates += change[1]
        self.head.y_coordinates += change[0]

        # Create new link at the previous head position
        new_link : Body.link = self.link(x_coordinates = self.head.x_coordinates - change[1], 
                                         y_coordinates = self.head.y_coordinates - change[0], 
                                         next_link = self.head.next_link, prev_link = self.head)

        # If there was a link after the head, update its prev_link
        if self.head.next_link is not None:
            self.head.next_link.prev_link = new_link

        # Insert new link after head
        self.head.next_link = new_link
        self.coordinates_dict[new_link] = [new_link.x_coordinates, new_link.y_coordinates]
    

    def collision_detection(self, board_length : int, board_width : int) -> bool:

        '''
        Check for collisions
        Args:
            None
        Returns:
            bool: True if there is a collision, False otherwise
        '''
        
        # Check for collision with walls
        if self.head.x_coordinates not in range(board_width) or self.head.y_coordinates not in range(board_length):
            print('You hit a wall!')
            return True

        # Check for collision with self
        for link in self.coordinates_dict:
            
            if (link != self.head and 
                self.coordinates_dict[link] == [self.head.x_coordinates, self.head.y_coordinates]):
                print('You hit yourself!')

                return True

        return False
    

    def update_coordinates_dict(self) -> None:

        '''
        Update the coordinates dictionary for the snake body
        '''
        
        # Clear the coordinates dictionary
        self.coordinates_dict = {}
        body = self.head

        # Insert new coordinates into dictionary
        while body is not None:

            self.coordinates_dict[body] = [body.x_coordinates, body.y_coordinates]
            body = body.next_link



class Food():

    '''
    Food class for the snake game
    '''

    def __init__(self, x_coordinates : int, y_coordinates : int) -> None:

        '''
        Initialize the food object
        Args:
            x_coordinates (int): The x-coordinate of the food
            y_coordinates (int): The y-coordinate of the food
        '''

        self.x_coordinates : int = x_coordinates
        self.y_coordinates : int = y_coordinates
    

    def spawn(self, board_length : int, board_width : int, body : Body) -> None:

        '''
        Spawn the food in a random position on the board
        Args:
            board_length (int): The length of the board
            board_width (int): The width of the board
            body (Body): The snake body
        Returns:
            None
        '''


        while True:

            x_location : int = random.randint(0, board_width - 1)
            y_location : int = random.randint(0, board_length - 1)

            # Check if the food is spawning on the snake body
            if all([x_location != link.x_coordinates or y_location != link.y_coordinates for link in body.coordinates_dict]):

                self.x_coordinates = x_location
                self.y_coordinates = y_location
                break



class Movements():

    '''
    Movement and display methods for the snake game
    '''

    def __init__(self, body : Body, food : Food, board_length : int, board_width : int) -> None:

        '''
        Initialize the movement and display methods for the snake game
        Args:
            body (Body): The snake body
            food (Food): The food object
            board_length (int): The length of the game board
            board_width (int): The width of the game board
        '''

        # Snake itself
        self.body : Body = body

        # Food
        self.food : Food = food

        # Initialize the display array
        self.arr : list[list[str]] = [['' for _ in range(board_width)] for _ in range(board_length)]


    def display(self, board_length : int, board_width : int, score : int) -> None:

        '''
        Display the current state of the game
        Args:
            board_length (int): The length of the game board
            board_width (int): The width of the game board
            score (int): The current score of the game
        Returns:
            None
        '''

        mamaguevo : list[str] = ['M', 'A', 'M', 'A', 'G', 'U', 'E', 'V', 'O']
        mama_counter : int = 0

        # Refresh the array and set the head to display as 'S'
        os.system('cls' if os.name == 'nt' else 'clear')
        self.arr = [['' for _ in range(board_width)] for _ in range(board_length)]
        body = self.body.head

        # Display the head as 'X'
        if body.x_coordinates in range(board_length) and body.y_coordinates in range(board_width):
            
            self.arr[body.y_coordinates][body.x_coordinates] = 'X'

        # Display the rest of the body as  the words 'MAMAGUEVO'
        while body.next_link is not None:

            body = body.next_link
            self.arr[body.y_coordinates][body.x_coordinates] = mamaguevo[mama_counter]
            mama_counter = (mama_counter + 1) % len(mamaguevo)

        # Display the food
        self.arr[self.food.y_coordinates][self.food.x_coordinates] = 'Q'

        # Display the empty spaces
        for row in self.arr:

            print(' '.join(str(x) if x != '' else '.' for x in row))
        
        print(f'Score: {score}')
        sleep(0.05)


    def moving(self, key_hit : str) -> None:

        '''
        Move the snake in the direction of the key pressed
        Args:
            key_hit (str): The key that was pressed
        Returns:
            None
        '''

        # Set up temporary variables to hold the previous coordinates
        body = self.body.head
        temp_x : int = body.x_coordinates
        temp_y : int = body.y_coordinates

        #Define direction based on key press
        if key_hit in ['w', 's']:

            body.y_coordinates -= 1 if key_hit == 'w' else -1
        
        elif key_hit in ['a', 'd']:

            body.x_coordinates -= 1 if key_hit == 'a' else -1

        # Shift the rest of the body
        while body.next_link:

            body = body.next_link
            temp2_x : int = body.x_coordinates
            temp2_y : int = body.y_coordinates
            body.x_coordinates = temp_x
            body.y_coordinates = temp_y
            temp_x = temp2_x
            temp_y = temp2_y

        # Update the coordinates dictionary after shifting
        self.body.update_coordinates_dict()



# Initialize score
score : int = 0

# board limits
board_length : int = 20
board_width : int = 20

# Initialize the snake and food
snake = Body(board_length = board_length, 
             board_width = board_width)

food = Food(x_coordinates = 0, 
            y_coordinates = 0)

# Spawn the food
food.spawn(board_length = board_length, 
           board_width = board_width, 
           body = snake)

# Initialize the movement and display methods
move = Movements(body = snake, 
                 food = food, 
                 board_length = board_length, 
                 board_width = board_width)

DIRECTIONS : dict[str, tuple[int]]= {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0)
}

snake.add_link([1, 0])
move.display(board_length = board_length, 
             board_width = board_width,
             score = score)

# Initial direction/key press
key : str = 's'

# Main game loop
while True:

    for new_key in ['w', 'a', 's', 'd', 'q']:

        if keyboard.is_pressed(new_key):

            if ((new_key in ['w', 's'] and key not in ['w', 's']) or 
                (new_key in ['a', 'd'] and key not in ['a', 'd'])):

                key = new_key

            if new_key == 'q':

                print("Game Ended")
                keyboard.unhook_all()
                exit()

            break
    
    if snake.collision_detection(board_length, board_width):

        print("Game Over!")
        keyboard.unhook_all()
        input('Press Enter to exit...')
        os.system('cls' if os.name == 'nt' else 'clear')
        break
    
    change_x : int = 0
    change_y : int = 0

    if [snake.head.x_coordinates, snake.head.y_coordinates] == [food.x_coordinates, food.y_coordinates]:

        # determine how new link will be added based on snake direction
        change_x, change_y = DIRECTIONS[key]

        snake.add_link(change = [change_y, change_x])

        food.spawn(board_length = board_length,
                   board_width = board_width,
                   body = snake)
        
        score += 1

    move.moving(key)

    move.display(board_length = board_length,
                 board_width = board_width,
                 score = score)
