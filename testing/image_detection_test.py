#!/usr/bin/env python3
'''
This file contains a function that captures the state of the physical maze with the
image detection functions in image_detection/image_detection.py and displays it on
screen using the pygame module.
'''

# Import modules.
import pygame

# Import classes, functions and values.
from objects import Maze, Ball
from image_detection.image_detection import initialise_maze, update_ball
from graphics.objects import SpriteBall
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from settings import PixelScale, White, Black

def image_detection_test():

    # Capture and initialise all elements in the maze.
    ActiveMaze = Maze(Ball([40, 40]), [], [], [])

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("'initialise_maze' should return an object of Maze class. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise clock.
    Clock = pygame.time.Clock()
    # Initialise display surface.
    Screen = pygame.display.set_mode((ActiveMaze.Size[0] * PixelScale, (ActiveMaze.Size[1] + 22) * PixelScale))
    pygame.display.set_caption("Maze Display")

    # Initialise text module.
    pygame.font.init()
    # Create fonts.
    Font1 = pygame.font.SysFont("Times New Roman", 7 * PixelScale)

    # Generate graphic objects.
    # Generate ball.
    BallList = pygame.sprite.Group()
    SpriteBall1 = SpriteBall(
        ActiveMaze.Ball.S, # [mm], numpy vector, size 2.
        ActiveMaze.Ball.R, # [mm], numpy vector, size 2.
    )
    BallList.add(SpriteBall1)
    # Generate walls.
    WallList = initialise_walls(ActiveMaze.Walls)
    # Generate holes.
    HoleList = initialise_holes(ActiveMaze.Holes)
    # Generate checkpoints.
    CheckpointList = initialise_checkpoints(ActiveMaze.Checkpoints)

    # Start main code.
    Running = 1
    while Running == 1:
        ''' PYGAME GRAPHICS END '''

        # Update ball position.
        BallUpdate = update_ball()
        ActiveMaze.Ball.Active = BallUpdate[0]
        ActiveMaze.Ball.S = BallUpdate[1]

        ''' PYGAME GRAPHICS START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0

        if ActiveMaze.Ball.Active == True:
            # Update Sprite Ball position.
            SpriteBall1.rect.centerx = ActiveMaze.Ball.S[0] * PixelScale # Ball position in pixels based on center of ball.
            SpriteBall1.rect.centery = ActiveMaze.Ball.S[1] * PixelScale # Ball position in pixels based on center of ball.
        else:
            SpriteBall1.kill()

        # Create surface with text describing the ball's position.
        BallPositionTxt = Font1.render(str(ActiveMaze.Ball), False, Black)

        # Update graphics. Could optimise.
        Screen.fill(White)
        WallList.draw(Screen) # Draw walls.
        HoleList.draw(Screen) # Draw holes.
        CheckpointList.draw(Screen) # Draw checkpoints.
        BallList.draw(Screen) # Draw ball.
        # Blit text to screen.
        Screen.blit(BallPositionTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 6) * PixelScale))
        pygame.display.flip() # Update display.

        Clock.tick()
        # Enable below to print T or fps of full graphics loop.
        #print("{:.0f}ms".format(Clock.get_time()))
        #print("{:.0f}fps".format(1/Clock.get_time()*1000))
        ''' PYGAME GRAPHICS END '''

    pygame.quit()