from settings import *
from pygame import FRect


class Sprite ( pygame.sprite.Sprite ):
	def __init__(self, name: str, z: int, image: Surface, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__(*groups)

		self.name = name
		self.z = z
		self.image = image

		self.rect: FRect = self.image.get_frect(**anchor)
		self.hitbox = self.rect.copy()
		self.y_order = self.rect.centery