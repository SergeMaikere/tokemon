from settings import *
from gameobj.Sprite import Sprite
from utils.Types import Biomes

class MonsterPatch ( Sprite ):
	def __init__(self, biome: Biomes, level: int, monsters: list[str], image: Surface, *groups: Group, **anchor) -> None:
		super().__init__('monster_patch', image, *groups, **anchor)

		self.biome = biome
		self.level = level
		self.monsters = monsters

		self.y_order -= 60