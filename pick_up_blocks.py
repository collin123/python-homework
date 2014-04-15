import os
import random
import time

import pygame

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
MOVEMENT = 5
LIVES = 3
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
BULLET_WIDTH = 15
BULLET_HEIGHT = 30

class Block(pygame.sprite.Sprite):
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

class Bullet(pygame.sprite.Sprite):
	def __init__(self, position):
		super(Bullet, self).__init__()
		self.bullet_position = position
		self.image = pygame.Surface([BULLET_WIDTH, BULLET_HEIGHT])
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	def update(self):
		self.rect.y -= 2

def main():
	pygame.init()
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	block_list = pygame.sprite.Group()
	bullet_list = pygame.sprite.Group()
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
	player = Player()
	player.center_player()
	lives_left = 3
	all_sprites_list.add(player)
	done = False
	clock = pygame.time.Clock()
	blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)
	map(lambda block: block.reset_pos(), blocks_hit_list)
	score = 0
	last_shot = 0
	while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
			keys_pressed = pygame.key.get_pressed()
			if keys_pressed[pygame.K_LEFT]:
				if player.rect.x > 0:
					player.rect.x -= MOVEMENT
			if keys_pressed[pygame.K_RIGHT]:
				if player.rect.x <= SCREEN_WIDTH - player.image.get_width():
					player.rect.x += MOVEMENT
			if keys_pressed[pygame.K_SPACE]:
				if ((time.time() - last_shot) > 0.5) and (len(bullet_list) < 5):
					last_shot = time.time()
					position = [player.rect.x, player.rect.y]
					position[0]  = position[0] + player.image.get_width() / 2
					position[0] = position[0] - (BULLET_WIDTH / 2)
					bullet = Bullet(position)
					bullet_list.add(bullet)
					all_sprites_list.add(bullet)
			screen.fill(WHITE)
			blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)
			map(lambda block: block.reset_pos(), blocks_hit_list)
			if len(blocks_hit_list):
				lives_left -= 1
				player.center_player()
				if lives_left == 0:
					print('You lost')
					done = True
			for bullet in bullet_list:
				blocks_hit_list = pygame.sprite.spritecollide(bullet, block_list, False)
				for block in blocks_hit_list:
					block.reset_pos()
				score += len(blocks_hit_list)
				if bullet.rect.y < -BULLET_HEIGHT:
					bullet_list.remove(bullet)
					all_sprites_list.remove(bullet)
			all_sprites_list.draw(screen)

			block_list.update()
			bullet_list.update()

			# Limit to 60 frames per second
			clock.tick(60)

			# Go ahead and update the screen with what we've drawn.
			pygame.display.flip()
	print('Your score was: ' + str(score))
	pygame.quit()

if __name__ == '__main__':
	main()
