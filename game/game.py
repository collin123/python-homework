import argparse
import cmd
import logging
import random

__version__ = '0.1'

class Player(object):
	def __init__(self, name, position = None):
		if not position:
			position = Position(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))
		self.position = position
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

	def pre_move(self):
		pass

	def post_move(self):
		self.logger.debug('player moved to ' + str(self.player.position))

class Interface(cmd.Cmd, object):
	def __init__(self, name):
		super(Interface, self).__init__()
		self.player = Player(name)
		self.game_engine = GameEngine(self.player)

	def do_go(self, args):
		self.game_engine.pre_move()
		position = self.player.position
		if args == 'north':
			if position.latitude == 10:
				print('you cannot go north anymore')
			else:
				position.latitude += 1
		elif args == 'east':
			if position.longitude == 10:
				print('you cannot go east anymore')
			else:
				position.longitude += 1
		elif args == 'south':
			if position.latitude == -10:
				print('you cannot go south anymore')
			else:
				position.latitude -= 1
		elif args == 'west':
			if position.longitude == -10:
				print('you cannot go west anymore')
			else:
				position.longitude -= 1
		elif args == 'up':
			if position.altitude == 10:
				print('you cannot go up anymore')
			else:
				position.altitude += 1
		elif args == 'down':
			if position.altitude == -10:
				print('you cannot go down anymore')
			else:
				position.altitude -= 1
		self.game_engine.post_move()

class Map(object):
	def __init__(self, map_size = None):
		if map_size == None:
			map_size = [10, 10]


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

