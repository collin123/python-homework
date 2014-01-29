import argparse
import copy
import cmd
import logging
import random
#create a method for gameengine called get_items_for_position(self, position)
#iterate thro self.all_items and return items that are in the position

__version__ = '0.1'

class Player(object):
	def __init__(self, name, position = None):
		if not position:
			position = Position(0, 0, 0)
		self.position = position
		self.logger = logging.getLogger('Player')
		self.logger.debug('player started at ' + str(position))
		self.health = 100.0
		self.items = {}
		self.name = name
		self.money = 0

	def move_latitude(self, adjust):
		self.position.latitude = self.position.latitude + adjust

	def move_longitude(self, adjust):
		self.position.longitude = self.position.longitude + adjust

	def move_altitude(self, adjust):
		self.position.altitude = self.position.altitude + adjust

class Position(object):
	def __init__(self, latitude, longitude, altitude):
		self.latitude = latitude
		self.longitude = longitude
		self.altitude = altitude

	def __str__(self):
		return '(' + str(self.latitude) + ', ' + str(self.longitude) + ', ' + str(self.altitude) + ')'

class GameEngine(object):
	def __init__(self, player):
		self.player = player
		self.logger = logging.getLogger('GameEngine')
		self.logger.info('GameEngine created')
		self.map = Map()
		treasure = Item('Treasure Chest')
		treasure.position = self.map.get_random_position()
		self.logger.debug('Put treasure chest at ' + str(tresure.position))
		self.all_items = []
		self.all_items.append(treasure)

	def pre_move(self):
		pass

	def post_move(self):
		self.logger.debug('player moved to ' + str(self.player.position))

class Interface(cmd.Cmd, object):
	def __init__(self, name):
		super(Interface, self).__init__()
		self.player = Player(name)
		self.game_engine = GameEngine(self.player)
		self.map = self.game_engine.map
		self.player.position = self.map.get_random_position()
		self.logger = logging.getLogger('status')

	def do_go(self, args):
		self.game_engine.pre_move()
		position = self.player.position
		old_position = copy.copy(position)
		if args == 'north':
			position.latitude += 1
		elif args == 'east':
			position.longitude += 1
		elif args == 'south':
			position.latitude -= 1
		elif args == 'west':
			position.longitude -= 1
		elif args == 'up':
			position.altitude += 1
		elif args == 'down':
			position.altitude -= 1
		if not self.map.is_valid_position(position):
			self._print('Invalid position')
			self.player.position = old_position
			return
		for item in self.game_engine.get_items_for_position(position):
			self._print('There is a ' + item.name + ' here.')
		self.game_engine.post_move()

	def _print(self, message):
		print(message)

class Map(object):
	def __init__(self):
			#latitude, longitude, altitude
			self.map_size = [[15, 15, 15], [-15, -15, -5]]

	def is_valid_position(self, position):
		if not (position.latitude >= self.map_size[1][0] and position.latitude <= self.map_size[0][0]):
			return False
		if not (position.longitude >= self.map_size[1][1] and position.longitude <= self.map_size[0][1]):
			return False
		if not (position.altitude >= self.map_size[1][2] and position.altitude <= self.map_size[0][2]):
			return False
		return True

	def get_random_position(self):
		latitude = random.randint(self.map_size[1][0], self.map_size[0][0])
		longitude = random.randint(self.map_size[1][1], self.map_size[0][1])
		altitude = random.randint(self.map_size[1][2], self.map_size[0][2])
		position = Position(latitude, longitude, altitude)
		return position

class Item(object):
	def __init__(self, name):
		self.name = name
		self.worth = 0
		self.weight = 1
		self.position = None

class Weapon(Item):
	def __init__(self, name):
		super(Weapon, self).__init__(name)
		self.durabilty = 100
		self.damage = 1

def main():
	parser = argparse.ArgumentParser(description = '', conflict_handler = 'resolve')
	parser.add_argument('-v', '--version', action = 'version', version = parser.prog + ' Version: ' + __version__)
	parser.add_argument('-L', '--log', dest = 'loglvl', action = 'store', choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default = 'INFO', help = 'set the logging level')
	parser.add_argument('-n', '--name', dest = 'name', required = True, help = 'Choose player name')
	arguments = parser.parse_args()

	logging.getLogger('').setLevel(logging.DEBUG)
	console_log_handler = logging.StreamHandler()
	console_log_handler.setLevel(getattr(logging, arguments.loglvl))
	console_log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
	logging.getLogger('').addHandler(console_log_handler)

	interface = Interface(arguments.name)
	interface.cmdloop()
	return 0

if __name__ == '__main__':
	main()

