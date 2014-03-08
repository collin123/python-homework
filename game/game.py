import argparse
import copy
import cmd
import logging
import shlex
import random

import engine
import items
import map
import player

__version__ = '0.1'

class Interface(cmd.Cmd, object):
	def __init__(self, name):
		super(Interface, self).__init__()
		self.map = map.Map()
		self.player = player.Player(name, self.map.get_random_position())
		self.game_engine = engine.GameEngine(self.player, self.map)
		self.player.position = self.player.position
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
		if not self.game_engine.is_valid_position(position):
			self._print('Invalid position')
			self.player.position = old_position
			return
		self.game_engine.post_move()
		self.show_items_in_position(position)
		self.show_enemies_in_position(position)

	def show_items_in_position(self, position):
		for item in self.game_engine.get_items_for_position(position):
			self._print('There is a ' + item.name + ' here.')

	def show_enemies_in_position(self, position):
		for enemy in self.game_engine.get_enemies_for_position(position):
			self._print('There is a ' + enemy.name + ' here.')

	def do_attack(self, args):
		weapon = None
		args = args.lower()
		args = args.strip()
		args_list = shlex.split(args)
		weapon_name = args_list[2]
		target_enemy = args_list[0]
		for item in self.player.items:
			if item.name.lower() == weapon_name.lower():
				weapon = item
				break
		if not weapon:
			self._print('There is no ' + weapon_name)
			return
		if not isinstance(weapon, items.ItemWeapon):
			self._print('That is not a weapon')
			return
		self.logger.debug('Player tried using ' + weapon_name)

		enemies = self.game_engine.get_enemies_for_position(self.player.position)
		if not enemies:
			self._print('There are no enemies to attack')
			return 0
		enemy_attacked = False
		for enemy in enemies:
			if target_enemy == enemy.name.lower():
				enemy_attacked = True
				damage_dealt = self.game_engine.attack(enemy, weapon)
				break
		if not enemy_attacked:
			self._print('There is no ' + target_enemy + ' here')
			return
		self._print('You dealt ' + str(damage_dealt) + ' to ' + target_enemy)
		if enemy.health <= 0:
			self._print('You killed the ' + target_enemy)

	def do_show(self, args):
		args = args.lower()
		args = shlex.split(args)
		if args[0] == 'inventory' or 'inv':
			for item in self.player.items:
				self._print(item.name )

	def __str__(self):
		for item in self.game_engine.all_items:
			return item.name

	def do_take(self, args):
		args = args.lower()
		args = args.strip()
		items = self.game_engine.get_items_for_position(self.player.position)
		if not items:
			self._print('There are no items to take')
			return 0
		if args:
			item_found = False
			for item in items:
				if args == item.name.lower():
					self.add_to_inventory(item)
					item_found = True
					break
			if not item_found:
				self._print('There is no ' + args + ' here')
		elif len(items) == 1:
			self.add_to_inventory(items[0])
		else:
			self.show_items_in_position(self.player.position)

	def do_load(self, args):
		self.game_engine.load_game(args)

	def do_save(self, args):
		self.game_engine.save_game(self.player.position, args)

	def add_to_inventory(self, item):
		self._print('Added ' + item.name + ' to your inventory')
		item.position = None
		self.player.items.append(item)

	def postcmd(self, stop, line):
		if not self.game_engine.get_enemies_for_position(self.player.position) == None:
			for enemy in self.game_engine.get_enemies_for_position(self.player.position):
				attack_enemy = enemy
				damage = self.game_engine.attack(self.player, attack_enemy)
				self._print(enemy.name + ' did ' + str(damage) + ' to ' + self.player.name)
				if self.player.health <= 0:
					self._print('Player died fighting a ' + attack_enemy.name)

	def _print(self, message):
		print(message)

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
