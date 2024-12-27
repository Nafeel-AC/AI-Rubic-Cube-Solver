import pygame
import sys
from cube import RubiksCube
from solver import CubeSolver
from gui import CubeGUI

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))  # Set the screen size for the GUI window
    pygame.display.set_caption("Rubik's Cube Solver")  # Set the window title
    
    # Initialize the Rubik's Cube, solver, and GUI components
    cube = RubiksCube()  # Create an instance of the Rubik's Cube
    solver = CubeSolver()  # Create an instance of the solver
    gui = CubeGUI(screen, cube)  # Create the GUI instance to display the cube and handle user interactions
    
    clock = pygame.time.Clock()  # To control the frame rate
    solving = False  # Flag to check if the cube is being solved
    processing = False  # Flag to check if the solution is being processed
    solution = []  # List to store the sequence of moves to solve the cube
    font = pygame.font.Font(None, 36)  # Initialize font for rendering text
    
    move_delay = 0.5  # Set delay between moves when solving (in seconds)
    last_move_time = 0  # Time of the last move made
    
    while True:
        current_time = pygame.time.get_ticks() / 1000  # Get the current time in seconds
        
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Exit Pygame if the window is closed
                sys.exit()  # Exit the program
            
            if event.type == pygame.KEYDOWN:
                # Scramble the cube when the space bar is pressed
                if event.key == pygame.K_SPACE and not solving:
                    cube.scramble()
                # Start processing the solution when the Enter key is pressed
                elif event.key == pygame.K_RETURN and not processing and not solving:
                    processing = True  # Flag to indicate that we are processing the solution
            
            # Handle user input (only when not processing or solving)
            if not processing and not solving:
                gui.handle_input(event)
        
        screen.fill((255, 255, 255))  # Clear the screen by filling it with white
        
        if processing:
            # Display the processing message while the solution is being generated
            text = font.render("Processing... Please wait", True, (0, 0, 0))
            screen.blit(text, (300, 50))  # Draw the text at a specific position
            pygame.display.flip()  # Update the screen to show the text
            
            # Solve the cube and update the solution list
            solution = solver.solve(cube)
            processing = False  # Stop processing after the solution is generated
            if solution:
                solving = True  # Set the flag to start solving
                last_move_time = current_time  # Record the time of the first move
        
        if solving and solution:
            # Move the cube step by step according to the solution
            if current_time - last_move_time >= move_delay:
                move = solution.pop(0)  # Get the next move from the solution
                cube.make_move(move)  # Apply the move to the cube
                last_move_time = current_time  # Update the time of the last move
                if not solution:  # If no more moves are left, stop solving
                    solving = False
        
        gui.draw()  # Draw the current state of the cube in the GUI
        
        # Show the remaining moves count if the cube is being solved
        if solving:
            text = font.render(f"Solving: {len(solution)} moves remaining", True, (0, 0, 0))
            screen.blit(text, (300, 50))  # Draw the status message
        
        pygame.display.flip()  # Update the screen with the new frame
        clock.tick(30)  # Control the frame rate to 30 FPS

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
