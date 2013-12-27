#!/usr/bin/env python
#  put install and uninstall mod in to class make it so you can install and uninstall mods without passing in argument

import os
import shutil
import sys

def translate_path(path, path_root):
	# path = '/home/collin/Desktop/mod1/file1'
	# path_root = mod = '/home/collin/Desktop/mod1'

	# first we get the length of path_root so we can remove that many characters
	# from path
	path_root_length = len(path_root)
	# path_root_length = 25

	# now we remove that many characters from the begining of path, we do this
	# by manipulating the string as an array
	path = path[path_root_length:]
	# path = '/file1'

	# because path still begins with a / we will add a . to the begining specifying
	# it as a relateive path
	path = '.' + path
	# path = './file1'
	return path

def count_directory_contents(directory):
	files = 0
	directories = 0
	for root, tmp_dirs, tmp_files in os.walk(directory):
		files += len(tmp_files)
		directories += len(tmp_dirs)
	return {'files': files, 'directories':directories}

def print_directory_contents(directory):
	for root, directories, files in os.walk(directory):
		for f in files:
			print(os.path.join(root, f))
		for d in directories:
			print(os.path.join(root, d))

def copy_file(source, destination):
	source = open(source, 'rb')
	destination = open(destination, 'wb')
	chunk = source.read(1024)
	while chunk:
		destination.write(chunk)
		chunk = source.read(1024)
	return 0

class ModInstall:
	def __init__(self, mod, game, backup = None):
		self.game = os.path.abspath(os.path.normpath(game))
		self.mod = os.path.abspath(os.path.normpath(mod))
		if backup == None:
			self.backup = os.path.join(os.getcwd(), 'backup')
		else:
			self.backup = os.path.abspath(os.path.normpath(backup))
		
	def install_mod(self):
		mod = self.mod
		game = self.game
		backup = self.backup
		print('mod directory: ' + mod)
		print('game directory: ' + game)
		print('backup directory: ' + backup)
		if not os.path.isdir(mod):
			print('Invalid directory')
		if not os.path.isdir(game):
			print('Invalid directory')
		if os.path.isdir(backup):
			confirm = raw_input('Are you sure you want to delete this directory ' + backup + ' [y/N] ')
			if confirm == 'y':
				shutil.rmtree(backup)
			else: 
				return 0
		os.mkdir(backup)
		for root, directories, files in os.walk(mod):
			for d in directories:
				mod_dir = os.path.join(root, d)
				backup_dir = os.path.normpath(os.path.join(backup, translate_path(mod_dir, mod)))
				game_dir = os.path.normpath(os.path.join(game, translate_path(mod_dir, mod)))
				
				#print('Game File = ' + game_file + ' Mod File = ' + mod_file)
				if os.path.isdir(game_dir):
					#print('File needs to be backed up ' + game_file)
					os.mkdir(backup_dir)
					print('Directory has been created ' + backup_dir)
			for f in files:
				mod_file = os.path.join(root, f)
				backup_file = os.path.normpath(os.path.join(backup, translate_path(mod_file, mod)))
				game_file = os.path.normpath(os.path.join(game, translate_path(mod_file, mod)))
				if os.path.isfile(game_file):
					#print('File needs to be backed up ' + game_file)
					copy_file(game_file, backup_file)
					print('File has been backed up ' + game_file)
					
		for root, directories, files in os.walk(mod):
			for d in directories:
				mod_dir = os.path.join(root, d)
				game_dir = os.path.normpath(os.path.join(game, translate_path(mod_dir, mod)))
	
				if not os.path.isdir(game_dir):
					os.mkdir(game_dir)
					print('Directory has been created ' + game_dir)
			for f in files:
				mod_file = os.path.join(root, f)
				game_file = os.path.normpath(os.path.join(game, translate_path(mod_file, mod)))
				copy_file(mod_file, game_file)
		return 0

	def uninstall_mod(self):
		backup = self.backup
		mod = self.mod
		game = self.game
		print('mod directory: ' + mod)
		print('game directory: ' + game)
		print('backup directory: ' + backup)

		for root, directories, files in os.walk(mod):
			for f in files:
				mod_file = os.path.join(root, f)
				backup_file = os.path.normpath(os.path.join(backup, translate_path(mod_file, mod)))
				game_file = os.path.normpath(os.path.join(game, translate_path(mod_file, mod)))
				if os.path.isfile(backup_file):
					copy_file(backup_file, game_file)
				else:
					os.unlink(game_file)
		for root, directories, files in os.walk(mod):
			for d in directories:
				mod_dir = os.path.join(root, d)
				backup_dir = os.path.normpath(os.path.join(backup, translate_path(mod_dir, mod)))
				game_dir = os.path.normpath(os.path.join(game, translate_path(mod_dir, mod)))
				if not os.path.isdir(backup_dir):
					shutil.rmtree(game_dir)

def main():
	game_mod = ModInstall(sys.argv[1], sys.argv[2], sys.argv[3])
	if sys.argv[4] == '-i':
		game_mod.install_mod()
	elif sys.argv[4] == '-u': 
		game_mod.uninstall_mod()
	return 0

if __name__ == '__main__':
	main()

