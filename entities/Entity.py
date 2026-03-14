from settings import *
from pygame import Surface
from pygame.sprite import Group

class Entity ( pygame.sprite.Sprite ):
	def __init__(self, frames: list[Surface], pos: tuple[float, float], *groups: Group) -> None:
		super().__init__(*groups)

		self.type = 'entity'
		
		self.index = 0
		self.frames = frames

		self.image = self.frames[self.index]
		self.rect = self.image.get_frect(center=pos)

		self.direction = pygame.Vector2()
		self.speed = 100

	def _set_direction ( self ):
		pass

	def _move ( self, dt: float ):
		self.rect.center += self.direction * self.speed * dt

	def update ( self, dt: float ):
		self._set_direction()
		self._move(dt)

