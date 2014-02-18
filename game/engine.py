import logging
import random

import enemies
import items

def xfrange(start, stop, step):
	while start < stop:
		yield start
		start += step

class GameEngine(object):
	def __init__(self, player, map):
		self.player = player
		self.logger = logging.getLogger('GameEngine')
		self.logger.info('GameEngine created')
		self.map = map
		elf = enemies.EnemyElf()
		elf.position = self.map.get_random_position()
		self.logger.debug('Put Elf at ' + str(elf.position))
		treasure = items.Item('Treasure Chest')
		treasure.position = self.map.get_random_position()
		self.logger.debug('Put treasure chest at ' + str(treasure.position))
		self.all_enemies = []
		self.all_enemies.append(elf)
		self.all_items = []
		self.all_items.append(treasure)

	def pre_move(self):
		pass

	def post_move(self):
		self.logger.debug('player moved to ' + str(self.player.position))

	def is_valid_position(self, position):
		return self.map.is_valid_position(position)

	def get_items_for_position(self, position):
		items = []
		for item in self.all_items:
			if item.position == position:
				items.append(item)
		return items

	def get_enemies_for_position(self, position):
		enemies = []
		for enemy in self.all_enemies:
			if enemy.position == position:
				enemies.append(enemy)
		return enemies

	def attack(self, enemy, weapon):
		weapon_damage = self.get_low_damage(weapon)
		enemy.health -= weapon_damage
		if enemy.health <= 0:
			enemy.position = None
		return weapon_damage

	def get_low_damage(self, weapon):
		weapon_low_damage = float(weapon.damage) / 2.0
		possible_damages = list(xfrange(weapon_low_damage, weapon.damage, 0.5))
		possible_damages.append(weapon.damage)
		return random.choice(possible_damages)

