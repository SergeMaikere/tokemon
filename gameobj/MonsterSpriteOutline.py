from typing import Callable, Literal
from settings import *
from gameobj.AnimatedSprite import AnimatedSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.MyGroup import MyGroup
from utils.Types import Trainers

class MonsterSpriteOutline ( AnimatedSprite ):
	def __init__(self, monster_sprite: MonsterSprite, *groups: MyGroup) -> None:
		self.monster_sprite = monster_sprite
		
		self.entity = self.monster_sprite.entity
		self.get_index = self.monster_sprite.get_index

		self.monster_frames = self.__flip_frames(self.monster_sprite.outline_frames)
		self._frames = self.monster_frames[self.monster_sprite.state]

		super().__init__('monster_sprite_outline', BATTLE_LAYERS['outline'], self.frames, *groups, center=self.monster_sprite.rect.center)


	@property
	def frames ( self ): 
		return self.monster_frames[self.monster_sprite.state]

	@frames.setter
	def frames ( self, value ):
		self._frames = value

	def __flip_frames ( self, frames: dict[str, list[Surface]] ):
		if self.entity != 'player': return frames
		return { k: [pygame.transform.flip(surface, True, False) for surface in surfaces] for k, surfaces in frames.items() }
	
	def _animate ( self, dt: float ):
		self.index = self.get_index()
		self.image = self.frames[ int(self.index) % len(self.frames) ]