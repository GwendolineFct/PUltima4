#!/usr/bin/env python3
# # Simple pygame program

# Import and initialize the pygame library
import pygame
import graphics
from avatar import Avatar
from event import KeyEvent, MouseEvent
from graphics import gfx_animate_shapes, gfx_init

from binaries import *

pygame.init()
gfx_init()

pygame.key.set_repeat(500,125)
clock = pygame.time.Clock()


# Define constants for the screen width and height
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

OFFSCREEN_WIDTH = 320
OFFSCREEN_HEIGHT = 200

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
offscreen = pygame.Surface((OFFSCREEN_WIDTH, OFFSCREEN_HEIGHT))

pygame.display.set_icon(pygame.transform.scale(graphics.shapes[61],(64,64)))

handler = Avatar()

while handler is not None:
    elapsed_time = clock.tick(60)

    gfx_animate_shapes(elapsed_time)

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user click the window close button? If so, stop the loop.
        if event.type == pygame.QUIT:
            handler.dispose()
            handler = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handler = handler.handle_event(MouseEvent(pygame.mouse.get_pressed(num_buttons=3), pygame.mouse.get_pos()))
        elif event.type == pygame.KEYDOWN:
            handler = handler.handle_event(KeyEvent(event.key, event.mod))

    if handler is None:
        continue

    handler.update(elapsed_time)
    handler.render(offscreen)

    screen.blit(pygame.transform.scale(offscreen, (SCREEN_WIDTH,SCREEN_HEIGHT)), (0,0))
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()