class Item(object):
	def __init__(self, name):
		self.name = name
		self.worth = 0
		self.weight = 1
		self.position = None

	def store(self):
		data = self.__dict__
		data['type'] = self.__class__.__name__
		if self.position:
			data['position'] = self.position.store()
		return data

class ItemWeapon(Item):
	def __init__(self, name):
		super(ItemWeapon, self).__init__(name)
		self.durabilty = 100
		self.damage = 1
