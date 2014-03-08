import random

class Map(object):
	def __init__(self):
			#latitude, longitude, altitude
			self.map_size = [[5, 5, 5], [-5, -5, -5]]

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

class Position(object):
	def __init__(self, latitude, longitude, altitude):
		self.latitude = latitude
		self.longitude = longitude
		self.altitude = altitude

	def store(self):
		data = self.__dict__
		data['type'] = self.__class__.__name__
		return data

	def __str__(self):
		return '(' + str(self.latitude) + ', ' + str(self.longitude) + ', ' + str(self.altitude) + ')'

	def __cmp__(self, other):
		if not isinstance(other, Position):
			return -1
		if not self.latitude == other.latitude:
			return -1
		if not self.longitude == other.longitude:
			return -1
		if not self.altitude == other.altitude:
			return -1
		return 0
