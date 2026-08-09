from settings import *
from entities.Entity import Entity
from pygame import Surface
from utils.MyGroup import MyGroup
from pygame.sprite import Group

class Player ( Entity ):
	def __init__(self, frames: dict[str, list[Surface]], pos: tuple[float, float], *groups: MyGroup) -> None:
		super().__init__('player', frames, pos, *groups)

		self.speed = 250
		self.is_noticed = False


	def set_is_noticed ( self, noticed: bool ): self.is_noticed = noticed

	def _set_direction ( self ):
		keys = pygame.key.get_pressed()
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
		self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
		self.direction = self.direction.normalize() if self.direction else self.direction
