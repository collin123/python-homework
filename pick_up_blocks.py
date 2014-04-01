"""
Use sprites to collect blocks.

Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Explanation video: http://youtu.be/4W2AqUetBi4
"""
#1. break out the main loop into function
#2. draw the blocks to random part of screen but the block moves down slowly
#
import pygame
import random
import os

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
MOVEMENT = 5
LIVES = 3
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
class Block(pygame.sprite.Sprite):
	"""
	This class represents the ball.
	It derives from the "Sprite" class in Pygame.
	"""
	# Constructor. Pass in the color of the block,
	# and its x and y position
	def __init__(self, image_file):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('sprites/', image_file))
		self.rect = self.image.get_rect()

	def reset_pos(self):
		self.rect.y = random.randrange(-300, -20)
		self.rect.x = random.randrange(0, SCREEN_WIDTH)

	def update(self):
		""" Called each frame. """

	# Move block down one pixel
		self.rect.y += 1
	# If block is too far down, reset to top of screen.
		if self.rect.y > 410:
			self.reset_pos()

class Player(Block):
	def __init__(self):
		super(Player, self).__init__('player.bmp')

	def center_player(self):
		self.rect.y = SCREEN_HEIGHT * 0.80
		self.rect.x = SCREEN_WIDTH * 0.48

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(20):
	# This represents a block
	block = Block('enemy_1.bmp')

	# Set a random location for the block
	block.rect.x = random.randrange(SCREEN_WIDTH)
	block.rect.y = random.randrange(SCREEN_HEIGHT)

	# Add the block to the list of objects
	block_list.add(block)
	all_sprites_list.add(block)

# Create a RED player block
player = Player()
player.center_player()
lives_left = 3

all_sprites_list.add(player)

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# See if the player block has collided with anything.
blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)
for block in blocks_hit_list:
	block.reset_pos()

score = 0

# -------- Main Program Loop -----------
while not done:
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_LEFT]:
		if player.rect.x > 0:
			player.rect.x -= MOVEMENT
	elif keys_pressed[pygame.K_RIGHT]:
		if player.rect.x <= SCREEN_WIDTH - player.image.get_width():
			player.rect.x += MOVEMENT
	screen.fill(WHITE)
	# See if the player block has collided with anything.
	blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
	if len(blocks_hit_list):
		lives_left -= 1
		player.center_player()
		if lives_left == 0:
			print('You lost')
			done = True
	all_sprites_list.draw(screen)

	block_list.update()

	# Limit to 60 frames per second
	clock.tick(60)

	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

pygame.quit()
