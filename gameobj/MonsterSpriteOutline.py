from typing import Literal

from gameobj.MonsterSprite import MonsterSprite
from settings import *
from gameobj.AnimatedSprite import AnimatedSprite
from utils.MyGroup import MyGroup
from utils.Types import Trainers

class MonsterSpriteOutline ( AnimatedSprite ):
	def __init__(self, monster_sprite: MonsterSprite, frames: dict[str, list[Surface]], *groups: MyGroup) -> None:
		
		self.monster_sprite = monster_sprite
		self.entity: Trainers = self.monster_sprite.entity
		self.state: Literal['idle', 'attack'] = 'idle'

		self.monster_frames = self.__flip_frames(frames)
		self.frames = self.monster_frames[self.state]

		super().__init__('monster_sprite_outline', BATTLE_LAYERS['outline'], self.frames, *groups, center=self.monster_sprite.rect.center)


	def __flip_frames ( self, frames: dict[str, list[Surface]] ):
		if self.entity != 'player': return frames
		return { k: [pygame.transform.flip(surface, True, False) for surface in surfaces] for k, surfaces in frames.items() }
	
	def _animate ( self, dt: float ):
		self.index = self.monster_sprite.index
		self.image = self.frames[ int(self.index) % len(self.frames) ]