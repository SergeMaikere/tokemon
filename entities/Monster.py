from random import randint
from assets.data.game_data import MONSTER_DATA

class Monster:
	def __init__( self, name: str, level: int ) -> None:
		self.name, self.level = name, level

		self.base_stats = MONSTER_DATA[name]['stats']
		self.element = self.base_stats['element']

		self.xp = randint(0, 1000)
		self.level_up = self.level * 150


	def get_stat ( self, stat: str ):
		return self.base_stats[stat] * self.level