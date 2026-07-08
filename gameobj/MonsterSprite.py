from random import uniform
from typing import Callable, Literal

from settings import *
from entities.Monster import Monster
from gameobj.AnimatedSprite import AnimatedSprite
from utils.Helper import required, compose
from utils.MyGroup import MyGroup
from utils.Timer import Timer
from utils.Types import Trainers

class MonsterSprite ( AnimatedSprite ):
	def __init__(self, monster: Monster, entity: Trainers, frames: dict[str, list[Surface]], outline_frames: dict[str, list[Surface]], pos: Point, handle_attack: Callable, *groups: MyGroup) -> None:
		
		self.monster = monster
		self.entity: Trainers = entity
		self.outline_frames = outline_frames
		self.pos = pos
		self.handle_attack = handle_attack
		self.my_groups = groups
		
		self.state: Literal['idle', 'attack'] = 'idle'
		self.monster_frames = self.__flip_frames(frames)
		self._frames = self.monster_frames[self.state]

		super().__init__('monster_sprite', BATTLE_LAYERS['monster'], self.frames, *groups, center=self.pos)

		self.speed = ANIMATION_SPEED + uniform(-1, 1)
		self._paused, self.flash, self.dead = False, False, False
		self.flash_timer = Timer(200, lambda: self.set_flash(False))

	@property
	def frames ( self ): 
		return self.monster_frames[self.state]

	@frames.setter
	def frames ( self, value ):
		self._frames = value

	def __flip_frames ( self, frames: dict[str, list[Surface]] ):
		if self.entity != 'player': return frames
		return { k: [pygame.transform.flip(surface, True, False) for surface in surfaces] for k, surfaces in frames.items() }

	def update_frames ( self ): self.frames = self.monster_frames[self.state]

	def set_paused ( self, paused: bool ): self._paused = paused

	def set_flash ( self, flash: bool ): self.flash = flash

	def set_state ( self, state: Literal['idle', 'attack'] ): self.state = state
	
	def start_flash ( self ):
		self.set_flash(True)
		self.flash_timer.start()		


	def _get_image ( self, dt: float ):
		if self.state == 'attack' and self.index >= len(self.frames):
			self.set_state('idle')
			self.handle_attack()
		if self.dead: return self.frames[0]
		
		self.index += self.speed * dt
		return self.frames[ int(self.index) % len(self.frames) ]

	def _animate ( self, dt: float ):
		self.image = compose(
			self._get_image,
			self.__flash_silhouette
		)( dt )
	
	def __flash_silhouette ( self, image: Surface ):
		if not self.flash: return image
		silhouette = pygame.mask.from_surface(required(image)).to_surface()
		silhouette.set_colorkey('black')
		return silhouette

	def update ( self, dt: float ):
		self._animate(dt)

		if self.flash_timer.running: self.flash_timer.update()

		if not self._paused: self.monster.increment_initiative(dt)
		