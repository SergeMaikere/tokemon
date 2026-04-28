from random import randint
from assets.data.game_data import MONSTER_DATA

class Monster:
	def __init__( self, name: str, level: int ) -> None:
		self.name, self.level = name, level

		self.base_stats = MONSTER_DATA[name]['stats']
		self.element = self.base_stats['element']

		self.xp = randint(0, 1000)
		self.level_up = self.level * 150

		self.health = max(0, self.get_stat('max_health') - randint(10, 100))
		self.energy = max(0, self.get_stat('max_energy') - randint(10, 100))


	def get_stat ( self, stat: str ): return self.base_stats[stat] * self.level

	def get_stats ( self ):
		return { stat.replace('max_', ''): value * self.level for stat, value in {stat: value for stat, value in self.base_stats.items() if stat != 'element'}.items() }
