import pygame
import math
import numpy as np

class CubeGUI:
    def __init__(self, screen, cube):  # Initialize GUI with screen and cube state
        self.screen = screen
        self.screen_width = 1024  # Increased window size for better visibility
        self.screen_height = 768
        self.cube = cube  # The cube object whose state we are visualizing
        self.colors = [
            (240, 240, 240),  # White
            (255, 255, 0),    # Yellow
            (255, 0, 0),      # Red
            (255, 165, 0),    # Orange
            (0, 0, 255),      # Blue
            (0, 255, 0),      # Green
        ]
        self.cell_size = 50  # Size of each cell in the cube
        self.margin = 5  # Margin between cells
        self.border_color = (100, 100, 100)  # Border color for the cube faces
        self.border_width = 2  # Border width

        # Center position for the cube net (layout of cube faces on the screen)
        self.center_x = self.screen_width // 2 - (self.cell_size * 6)
        self.center_y = self.screen_height // 2 - (self.cell_size * 4)

        # Mouse interaction variables
        self.dragging = False  # Flag for mouse dragging
        self.drag_start = None  # Starting point for dragging
        self.selected_face = None  # Selected face during dragging
        self.drag_threshold = 20  # Threshold for detecting a drag

        # Face positions and labels
        self.face_positions = [{'face': i, 'rect': None} for i in range(6)]  # Holds face information
        self.face_labels = [
            "FRONT (White)",    # 0
            "BACK (Yellow)",    # 1
            "RIGHT (Red)",      # 2
            "LEFT (Orange)",    # 3
            "TOP (Blue)",       # 4
            "BOTTOM (Green)"    # 5
        ]

        # Layout order for displaying cube faces (each tuple represents a (x, y) position in the grid)
        self.layouts = [
            (1, 1),  # Front (White) - 0
            (3, 1),  # Back (Yellow) - 1
            (2, 1),  # Right (Red) - 2
            (0, 1),  # Left (Orange) - 3
            (1, 0),  # Top (Blue) - 4
            (1, 2),  # Bottom (Green) - 5
        ]

        self.label_color = (0, 0, 0)  # Label color
        self.font = pygame.font.Font(None, 28)  # Font for labels

        # Info box at the top left corner for instructions or information
        self.info_font = pygame.font.Font(None, 24)
        self.info_box = pygame.Rect(10, 10, 300, 100)

        # Button configuration for rotating the cube faces
        self.button_font = pygame.font.Font(None, 24)
        self.button_height = 30  # Button height
        self.button_width = 100  # Button width
        self.button_margin = 5  # Space between buttons
        self.button_color = (200, 200, 200)  # Default button color
        self.button_hover_color = (180, 180, 180)  # Button color when hovered
        self.button_text_color = (0, 0, 0)  # Button text color

        # Create buttons for each face rotation (Clockwise and Counter-Clockwise)
        self.buttons = []
        faces = ['Front', 'Back', 'Right', 'Left', 'Top', 'Bottom']
        x_start = 50
        y_start = 50  # Starting position for buttons

        # Add rotation buttons for each face
        for i, face in enumerate(faces):
            # Clockwise button
            self.buttons.append({
                'rect': pygame.Rect(x_start, y_start + i * (self.button_height + self.button_margin) * 2,
                                  self.button_width, self.button_height),
                'text': f'{face} CW',  # Clockwise rotation label
                'action': (i, 1),  # Action to rotate clockwise
                'hover': False  # Button hover state
            })
            # Counter-clockwise button
            self.buttons.append({
                'rect': pygame.Rect(x_start + self.button_width + self.button_margin,
                                  y_start + i * (self.button_height + self.button_margin) * 2,
                                  self.button_width, self.button_height),
                'text': f'{face} CCW',  # Counter-clockwise rotation label
                'action': (i, -1),  # Action to rotate counter-clockwise
                'hover': False  # Button hover state
            })

        # Add reset button to reset the cube state
        self.reset_button = {
            'rect': pygame.Rect(x_start, y_start + len(faces) * (self.button_height + self.button_margin) * 2,
                                self.button_width * 2 + self.button_margin, self.button_height),
            'text': 'Reset Cube',  # Reset cube label
            'color': (255, 100, 100),  # Light red color for reset button
            'hover_color': (255, 80, 80),  # Darker red when hovered
            'hover': False  # Hover state
        }

    def draw(self):
        # Clear screen first
        self.screen.fill((255, 255, 255))  # White background

        # Draw reset button and handle hover effect
        mouse_pos = pygame.mouse.get_pos()
        self.reset_button['hover'] = self.reset_button['rect'].collidepoint(mouse_pos)
        button_color = self.reset_button['hover_color'] if self.reset_button['hover'] else self.reset_button['color']

        pygame.draw.rect(self.screen, button_color, self.reset_button['rect'])  # Draw button
        pygame.draw.rect(self.screen, self.border_color, self.reset_button['rect'], 1)  # Draw button border

        reset_text = self.button_font.render(self.reset_button['text'], True, (0, 0, 0))  # Button text
        text_rect = reset_text.get_rect(center=self.reset_button['rect'].center)  # Center text
        self.screen.blit(reset_text, text_rect)

        # Draw info text (instructions, etc.)
        info_text = ["Press ENTER to solve"]
        for i, text in enumerate(info_text):
            info_surface = self.info_font.render(text, True, (0, 0, 0))  # Info text
            self.screen.blit(info_surface, (20, 20 + i * 25))

        # Draw face rotation buttons and handle hover effect
        for button in self.buttons:
            button['hover'] = button['rect'].collidepoint(mouse_pos)  # Check hover
            color = self.button_hover_color if button['hover'] else self.button_color

            pygame.draw.rect(self.screen, color, button['rect'])  # Draw button
            pygame.draw.rect(self.screen, self.border_color, button['rect'], 1)  # Draw button border

            # Draw button text
            text = self.button_font.render(button['text'], True, self.button_text_color)
            text_rect = text.get_rect(center=button['rect'].center)  # Center text
            self.screen.blit(text, text_rect)

        # Draw cube faces
        cube_start_x = 300  # Move cube display to the right
        for face in range(6):
            x_offset = self.layouts[face][0] * (self.cell_size * 3 + self.margin)
            y_offset = self.layouts[face][1] * (self.cell_size * 3 + self.margin)

            # Calculate centered position for face
            face_rect = pygame.Rect(
                cube_start_x + x_offset,
                self.center_y + y_offset,
                self.cell_size * 3,
                self.cell_size * 3
            )

            # Draw face background and border
            pygame.draw.rect(self.screen, self.border_color, face_rect)

            # Draw face label
            label = self.font.render(self.face_labels[face], True, self.label_color)
            label_pos = (
                face_rect.centerx - label.get_width() // 2,
                face_rect.y - 30 if face != 5 else face_rect.y + self.cell_size * 3 + 10  # Special position for bottom label
            )
            self.screen.blit(label, label_pos)

            # Draw cells for each face (colored squares)
            for i in range(3):
                for j in range(3):
                    color = self.colors[self.cube.state[face][i][j]]  # Color based on cube state
                    rect = pygame.Rect(
                        face_rect.x + j * self.cell_size + self.border_width,
                        face_rect.y + i * self.cell_size + self.border_width,
                        self.cell_size - self.border_width * 2,
                        self.cell_size - self.border_width * 2
                    )
                    pygame.draw.rect(self.screen, color, rect)  # Draw cell
                    pygame.draw.rect(self.screen, self.border_color, rect, 1)  # Draw cell border

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check reset button click and reset the cube to its initial state
            if self.reset_button['rect'].collidepoint(event.pos):
                for i in range(6):
                    self.cube.state[i] = np.full((3, 3), i)  # Reset cube faces
                return

            # Check face rotation button clicks
            for button in self.buttons:
                if button['rect'].collidepoint(event.pos):
                    face, direction = button['action']  # Get face and rotation direction
                    self.cube.make_move((face, direction))  # Apply rotation move
                    break
