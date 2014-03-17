"""
 Show how to use a sprite backed by a graphic.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

pygame.init()

# Set the width and height of the screen [width, height]
size = (300, 300)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
center = {'x':size[0]/2, 'y':size[1]/2}
position = {'x':150, 'y':150}
shrink = True
while not done:
	# --- Main event loop
	if position['x'] == center['x'] or position['y'] == center['y']:
		shrink = False
		print('increasing size')
	elif position['x'] == 0 or position['y'] == 0:
		shrink = True
	if shrink:
		position['x'] += 1
		position['y'] += 1
	else:
		position['x'] -= 1
		position['y'] -= 1
	r_size = {'x':0, 'y':0}
	r_size['x'] = (center['x'] - position['x']) * 2
	r_size['y'] = (center['y'] - position['y']) * 2
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop

	# --- Game logic should go here

	# --- Drawing code should go here

	# First, clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.
	screen.fill(WHITE)
	pygame.draw.rect(screen, BLACK, [position['x'], position['y'], r_size['x'], r_size['y']])


	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

	# --- Limit to 60 frames per second
	clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
