from typing import Literal

from settings import *
from entities.Monster import Monster
from gameobj.AnimatedSprite import AnimatedSprite
from utils.MyGroup import MyGroup

class MonsterSprite ( AnimatedSprite ):
	def __init__(self, monster: Monster, entity: Literal['player', 'opponent'], frames: dict[str, list[Surface]], pos: Point, *groups: MyGroup) -> None:
		self.monster = monster
		self.entity = entity
		self.monster_frames = self.__flip_frames(frames)

		self.state: Literal['idle', 'attack'] = 'idle'
		self.frames = self.monster_frames[self.state]
		
		super().__init__('monster_sprite', WORLD_LAYERS['top'], self.frames, *groups, center=pos)



	def __flip_frames ( self, frames: dict[str, list[Surface]] ):
		if self.entity != 'player': return frames
		return { k: [pygame.transform.flip(surface, True, False) for surface in surfaces] for k, surfaces in frames.items() }