from settings import *
from pygame import Surface
from pygame.sprite import Group

class Sprite ( pygame.sprite.Sprite ):
	def __init__(self, type: str, image: Surface, *groups: Group, **anchor) -> None:
		super().__init__(*groups)

		self.type = type
		self.image = image
		self.rect = self.image.get_frect(**anchor)