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
center = {'x':size[0]/2, 'y':size[1]/2}
rectangle_size = 100
screen.fill(WHITE)
for key, value in tiles.items():
	pygame.draw.rect(screen, BLACK, [ value[0], value[1], rectangle_size, rectangle_size])
while not done:
	# --- Main event loop
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		elif event.type == pygame.MOUSEBUTTONDOWN:
			position = pygame.mouse.get_pos()
			for key, value in tiles.items():
				cursor_in_shape = is_cursor_in_rectangle(rectangle_size, value, position)
				if cursor_in_shape:
					pygame.draw.rect(screen, RED, [ value[0], value[1], rectangle_size, rectangle_size])
				else:
					pygame.draw.rect(screen, BLACK, [ value[0], value[1], rectangle_size, rectangle_size])

	# --- Game logic should go here

	# --- Drawing code should go here

	# First, clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.


	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

	# --- Limit to 60 frames per second
	clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
