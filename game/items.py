class Item(object):
	def __init__(self, name):
		self.name = name
		self.worth = 0
		self.weight = 1
		self.position = None

class ItemWeapon(Item):
	def __init__(self, name):
		super(ItemWeapon, self).__init__(name)
		self.durabilty = 100
		self.damage = 1
