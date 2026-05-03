from settings import *
from entities.Monster import Monster
from gameobj.AnimatedSprite import AnimatedSprite
from utils.MyGroup import MyGroup

class MonsterSprite ( AnimatedSprite ):
	def __init__(self, monster: Monster, frames: dict[str, list[Surface]], pos: Point, *groups: MyGroup) -> None:
		super().__init__('monster_sprite', WORLD_LAYERS['top'], frames['idle'], *groups, center=pos)

		self.monster = monster
		self.monster_frames = frames

