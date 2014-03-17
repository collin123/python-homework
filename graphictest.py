"""
 Show how to use a sprite backed by a graphic.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""
import random
import time

import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

pygame.init()

# Set the width and height of the screen [width, height]

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
tiles = {'r0': (0, 0),
	'r1': (200, 0),
	'r2': (100, 100),
	'r3': (0, 200),
	'r4': (200, 200)
}

def is_cursor_in_rectangle(size, rectangle_position, cursor_position):
	if rectangle_position[0] + size <= cursor_position[0]:
		return False
	if rectangle_position[0] >= cursor_position[0]:
		return False
	if rectangle_position[1] + size <= cursor_position[1]:
		return False
	if rectangle_position[1] >= cursor_position[1]:
		return False
	return True

# -------- Main Program Loop -----------
def game(level):
	random_tile = random.choice(tiles.keys())
	size = (300, 300)
	screen = pygame.display.set_mode(size)
	center = {'x':size[0]/2, 'y':size[1]/2}
	rectangle_size = 100
	screen.fill(WHITE)
	position = (0, 0)
	pygame.display.set_caption("Level " + str(level))
	tries = 6 - level
	for key, value in tiles.items():
		pygame.draw.rect(screen, BLACK, [ value[0], value[1], rectangle_size, rectangle_size])
	while tries:
		# --- Main event loop
		decrement_tries = False
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				return False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				position = pygame.mouse.get_pos()
				decrement_tries = True

		for key, value in tiles.items():
			if is_cursor_in_rectangle(rectangle_size, value, position):
				if decrement_tries:
					tries -= 1
				if random_tile == key:
					color = GREEN
				else:
					color = RED
			else:
				color = BLACK
			pygame.draw.rect(screen, color, [value[0], value[1], rectangle_size, rectangle_size])
			if color == GREEN:
				pygame.display.flip()
				time.sleep(1)
				return True
		# --- Game logic should go here
		pygame.display.flip()

		# --- Limit to 60 frames per second
		clock.tick(60)
	return False

for level in range(1, 6):
	if not game(level):
		break
pygame.quit()
