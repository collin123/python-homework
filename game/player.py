import logging

import items

class Player(object):
	def __init__(self, name, position):
		self.position = position
		self.logger = logging.getLogger('Player')
		self.logger.debug('player started at ' + str(self.position))
		self.health = 100.0
		self.items = []
		self.name = name
		self.money = 0

		ocarina = items.Item('Ocarina')
		self.items.append(ocarina)
		wooden_sword = items.ItemWeapon('sword')
		wooden_sword.damage = 5
		self.items.append(wooden_sword)

	def move_latitude(self, adjust):
		self.position.latitude = self.position.latitude + adjust

	def move_longitude(self, adjust):
		self.position.longitude = self.position.longitude + adjust

	def move_altitude(self, adjust):
		self.position.altitude = self.position.altitude + adjust
