from settings import *
from gameobj.Sprite import Sprite
from utils.MyGroup import MyGroup
from utils.Types import Biomes, MonsterNames

class MonsterPatch ( Sprite ):
	def __init__(self, biome: Biomes, level: int, monsters: list[MonsterNames], image: Surface, *groups: MyGroup, **anchor) -> None:
		super().__init__('monster_patch', WORLD_LAYERS['main' if biome != 'sand' else 'bg'], image, *groups, **anchor)

		self.biome = biome
		self.level = level
		self.monsters = monsters

		self.y_order -= 60