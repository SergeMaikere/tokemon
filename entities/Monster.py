from assets.data.game_data import MONSTER_DATA

class Monster:
	def __init__( self, name: str, level: int ) -> None:
		self.name, self.level = name, level

		self.stats = MONSTER_DATA[name]['stats']
		self.element = self.stats['element']