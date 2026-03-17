from settings import *
from pygame import Surface
from pygame.sprite import Group

from utils.Types import States

class Entity ( pygame.sprite.Sprite ):
	def __init__(self, frames: dict[str, list[Surface]], pos: tuple[float, float], *groups: Group) -> None:
		super().__init__(*groups)

		self.type = 'entity'
		self.state: States = 'down'
		
		self.index = 0
		self.frames = frames

		self.image = self.frames[self.state][self.index]
		self.rect = self.image.get_frect(center=pos)

		self.direction = pygame.Vector2()
		self.speed = 100
		self.animation_speed = 5

	def _set_direction ( self ):
		pass

	def _set_state ( self ):
		if self.direction.y == 1: self.state = 'down'
		if self.direction.x == 1: self.state = 'right'
		if self.direction.x == -1: self.state = 'left'
		if self.direction.y == -1: self.state = 'up'

	def _animate ( self, dt: float ):
		if not self.direction: self.index = 0
		self.index += self.animation_speed * dt
		self.image = self.frames[self.state][int(self.index) % len(self.frames[self.state])]

	def _move ( self, dt: float ):
		self.rect.center += self.direction * self.speed * dt

	def update ( self, dt: float ):
		self._set_direction()
		self._set_state()
		self._animate(dt)
		self._move(dt)

