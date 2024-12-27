import random
import numpy as np

class RubiksCube:
    def __init__(self):
        # Initialize the cube with each face having a unique color
        # Colors: 0=white, 1=yellow, 2=red, 3=orange, 4=blue, 5=green
        self.state = np.zeros((6, 3, 3), dtype=int)
        for i in range(6):
            self.state[i] = np.full((3, 3), i)  # Set each face to its corresponding color index

    def make_move(self, move):
        # Perform a move on the Rubik's Cube
        face, direction = move
        # Rotate the selected face
        self.state[face] = np.rot90(self.state[face], -direction)  # Rotate face 90 degrees, direction controls clockwise/counter-clockwise
        
        # Update the adjacent faces based on the selected face being rotated
        if face == 0:  # Front (White)
            self._rotate_adjacent_to_front(direction)
        elif face == 1:  # Back (Yellow)
            self._rotate_adjacent_to_back(direction)
        elif face == 2:  # Right (Red)
            self._rotate_adjacent_to_right(direction)
        elif face == 3:  # Left (Orange)
            self._rotate_adjacent_to_left(direction)
        elif face == 4:  # Top (Blue)
            self._rotate_adjacent_to_top(direction)
        elif face == 5:  # Bottom (Green)
            self._rotate_adjacent_to_bottom(direction)

    def _rotate_adjacent_to_front(self, direction):
        # Handle the rotation of adjacent faces when rotating the front (white) face
        if direction == 1:  # Clockwise
            temp = self.state[4][2].copy()  # Save the top row of the blue face
            self.state[4][2] = self.state[3][:, 2][::-1]  # Move the right column of the orange face to the blue face
            self.state[3][:, 2] = self.state[5][0]  # Move the bottom row of the green face to the orange face
            self.state[5][0] = self.state[2][:, 0][::-1]  # Move the left column of the red face to the green face
            self.state[2][:, 0] = temp  # Move the saved top row of blue face to the red face
        else:  # Counter-clockwise
            temp = self.state[4][2].copy()  # Save the top row of the blue face
            self.state[4][2] = self.state[2][:, 0]  # Move the left column of the red face to the blue face
            self.state[2][:, 0] = self.state[5][0][::-1]  # Move the bottom row of the green face to the red face
            self.state[5][0] = self.state[3][:, 2]  # Move the right column of the orange face to the green face
            self.state[3][:, 2] = temp[::-1]  # Move the saved top row of the blue face to the orange face, reversed

    def _rotate_adjacent_to_back(self, direction):
        # Handle the rotation of adjacent faces when rotating the back (yellow) face
        if direction == 1:  # Clockwise
            temp = self.state[4][0].copy()  # Save the bottom row of the blue face
            self.state[4][0] = self.state[2][:, 2][::-1]  # Move the right column of the red face to the blue face
            self.state[2][:, 2] = self.state[5][2]  # Move the top row of the green face to the red face
            self.state[5][2] = self.state[3][:, 0][::-1]  # Move the left column of the orange face to the green face
            self.state[3][:, 0] = temp  # Move the saved bottom row of the blue face to the orange face
        else:  # Counter-clockwise
            temp = self.state[4][0].copy()  # Save the bottom row of the blue face
            self.state[4][0] = self.state[3][:, 0]  # Move the left column of the orange face to the blue face
            self.state[3][:, 0] = self.state[5][2][::-1]  # Move the top row of the green face to the orange face
            self.state[5][2] = self.state[2][:, 2]  # Move the right column of the red face to the green face
            self.state[2][:, 2] = temp[::-1]  # Move the saved bottom row of the blue face to the red face, reversed

    def _rotate_adjacent_to_right(self, direction):
        # Handle the rotation of adjacent faces when rotating the right (red) face
        if direction == 1:  # Clockwise
            temp = self.state[0][:, 2].copy()  # Save the right column of the white face
            self.state[0][:, 2] = self.state[4][:, 2]  # Move the right column of the blue face to the white face
            self.state[4][:, 2] = self.state[1][:, 0][::-1]  # Move the left column of the yellow face to the blue face
            self.state[1][:, 0] = self.state[5][:, 2][::-1]  # Move the right column of the green face to the yellow face
            self.state[5][:, 2] = temp  # Move the saved right column of the white face to the green face
        else:  # Counter-clockwise
            temp = self.state[0][:, 2].copy()  # Save the right column of the white face
            self.state[0][:, 2] = self.state[5][:, 2]  # Move the right column of the green face to the white face
            self.state[5][:, 2] = self.state[1][:, 0][::-1]  # Move the left column of the yellow face to the green face
            self.state[1][:, 0] = self.state[4][:, 2][::-1]  # Move the right column of the blue face to the yellow face
            self.state[4][:, 2] = temp  # Move the saved right column of the white face to the blue face

    def _rotate_adjacent_to_left(self, direction):
        # Handle the rotation of adjacent faces when rotating the left (orange) face
        if direction == 1:  # Clockwise
            temp = self.state[0][:, 0].copy()  # Save the left column of the white face
            self.state[0][:, 0] = self.state[5][:, 0]  # Move the left column of the green face to the white face
            self.state[5][:, 0] = self.state[1][:, 2][::-1]  # Move the right column of the yellow face to the green face
            self.state[1][:, 2] = self.state[4][:, 0][::-1]  # Move the left column of the blue face to the yellow face
            self.state[4][:, 0] = temp  # Move the saved left column of the white face to the blue face
        else:  # Counter-clockwise
            temp = self.state[0][:, 0].copy()  # Save the left column of the white face
            self.state[0][:, 0] = self.state[4][:, 0]  # Move the left column of the blue face to the white face
            self.state[4][:, 0] = self.state[1][:, 2][::-1]  # Move the right column of the yellow face to the blue face
            self.state[1][:, 2] = self.state[5][:, 0][::-1]  # Move the left column of the green face to the yellow face
            self.state[5][:, 0] = temp  # Move the saved left column of the white face to the green face

    def _rotate_adjacent_to_top(self, direction):
        # Handle the rotation of adjacent faces when rotating the top (blue) face
        if direction == 1:  # Clockwise
            temp = self.state[0][0].copy()  # Save the top left corner of the white face
            self.state[0][0] = self.state[3][0]  # Move the left column of the orange face to the white face
            self.state[3][0] = self.state[1][0]  # Move the left column of the yellow face to the orange face
            self.state[1][0] = self.state[2][0]  # Move the left column of the red face to the yellow face
            self.state[2][0] = temp  # Move the saved top left corner of the white face to the red face
        else:  # Counter-clockwise
            temp = self.state[0][0].copy()  # Save the top left corner of the white face
            self.state[0][0] = self.state[2][0]  # Move the left column of the red face to the white face
            self.state[2][0] = self.state[1][0]  # Move the left column of the yellow face to the red face
            self.state[1][0] = self.state[3][0]  # Move the left column of the orange face to the yellow face
            self.state[3][0] = temp  # Move the saved top left corner of the white face to the orange face

    def _rotate_adjacent_to_bottom(self, direction):
        # Handle the rotation of adjacent faces when rotating the bottom (green) face
        if direction == 1:  # Clockwise
            temp = self.state[0][2].copy()  # Save the bottom right corner of the white face
            self.state[0][2] = self.state[2][2]  # Move the right column of the red face to the white face
            self.state[2][2] = self.state[1][2]  # Move the right column of the yellow face to the red face
            self.state[1][2] = self.state[3][2]  # Move the right column of the orange face to the yellow face
            self.state[3][2] = temp  # Move the saved bottom right corner of the white face to the orange face
        else:  # Counter-clockwise
            temp = self.state[0][2].copy()  # Save the bottom right corner of the white face
            self.state[0][2] = self.state[3][2]  # Move the right column of the orange face to the white face
            self.state[3][2] = self.state[1][2]  # Move the right column of the yellow face to the orange face
            self.state[1][2] = self.state[2][2]  # Move the right column of the red face to the yellow face
            self.state[2][2] = temp  # Move the saved bottom right corner of the white face to the red face
    
    def scramble(self):
        # Scramble the cube by performing a series of random moves
        moves = [(f, d) for f in range(6) for d in [-1, 1]]  # List of possible moves (face, direction)
        for _ in range(20):  # Perform 20 random moves
            self.make_move(random.choice(moves))  # Apply a random move

    def is_solved(self):
        # Check if the cube is solved by verifying that each face has only one color
        return all(np.all(self.state[i] == i) for i in range(6))

    def get_state(self):
        # Return a copy of the current state of the cube
        return self.state.copy()
