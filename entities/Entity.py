from gameobj.Sprite import Sprite
from settings import *
from pygame import Surface
from pygame.sprite import Group

from utils.Types import States

class Entity ( Sprite ):
	def __init__( self, name: str, frames: dict[str, list[Surface]], pos: tuple[float, float], *groups: Group ) -> None:
		super().__init__(name, WORLD_LAYERS['main'], frames['down'][0], *groups, center=pos)

		self.state: States = 'down'
		
		self.index = 0
		self.frames = frames
		self.hitbox = self.rect.inflate(-self.rect.width/2, -60)

		self.is_mobile = True
		self.speed = 100
		self.direction = pygame.Vector2()

	def _set_direction ( self ):
		pass

	def _set_state ( self ):
		if self.direction.y == 1: self.state = 'down'
		if self.direction.x == 1: self.state = 'right'
		if self.direction.x == -1: self.state = 'left'
		if self.direction.y == -1: self.state = 'up'

	def _animate ( self, dt: float ):
		if not self.direction: self.index = 0
		self.index += ANIMATION_SPEED * dt
		self.image = self.frames[self.state][int(self.index) % len(self.frames[self.state])]

	def _move ( self, dt: float ):
		self.rect.center += self.direction * self.speed * dt

	def update ( self, dt: float ):
		if self.is_mobile:
			self._set_direction()
			self._set_state()
			self._move(dt)
		self._animate(dt)

