class Enemy(object):
	def __init__(self, name):
		self.damage = 2
		self.health = 25
		self.name = name
		self.position = None

class EnemyElf(Enemy):
	def __init__(self, id = 0):
		name = 'Elf'
		if id:
			name += ' ' + str(id)
		super(EnemyElf, self).__init__(name)
		self.damage = 3
		self.health = 15

class EnemySpider(Enemy):
	def __init__(self, id = 0):
		name = 'Spider'
		if id:
			name += ' ' + str(id)
		super(EnemySpider, self).__init__(name)
		self.damage = 5
		self.health = 10

