from settings import *
from entities.Entity import Entity
from pygame import Surface
from pygame.sprite import Group

class Player ( Entity ):
	def __init__(self, frames: list[Surface], pos: tuple[float, float], *groups: Group) -> None:
		super().__init__(frames, pos, *groups)

		self.speed = 250

	def _set_direction ( self ):
		keys = pygame.key.get_pressed()
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
		self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
		self.direction = self.direction.normalize() if self.direction else self.direction
