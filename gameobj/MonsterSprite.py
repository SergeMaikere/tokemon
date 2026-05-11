from random import uniform
from typing import Literal

from settings import *
from entities.Monster import Monster
from gameobj.AnimatedSprite import AnimatedSprite
from utils.MyGroup import MyGroup
from utils.Types import Trainers

class MonsterSprite ( AnimatedSprite ):
	def __init__(self, monster: Monster, entity: Trainers, frames: dict[str, list[Surface]], pos: Point, *groups: MyGroup) -> None:
		
		self.monster = monster
		self.entity: Trainers = entity
		self.state: Literal['idle', 'attack'] = 'idle'

		self.monster_frames = self.__flip_frames(frames)
		self.frames = self.monster_frames[self.state]

		super().__init__('monster_sprite', WORLD_LAYERS['top'], self.frames, *groups, center=pos)

		self.z = 'monster'
		self.speed = ANIMATION_SPEED + uniform(-1, 1)
		self._paused = False



	def __flip_frames ( self, frames: dict[str, list[Surface]] ):
		if self.entity != 'player': return frames
		return { k: [pygame.transform.flip(surface, True, False) for surface in surfaces] for k, surfaces in frames.items() }

	def set_paused ( self, paused: bool ): self._paused = paused
	
	def update ( self, dt: float ):
		if self._paused: return
		self._animate(dt)
		self.monster.increment_initiative(dt)
		