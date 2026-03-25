from settings import *


class Sprite ( pygame.sprite.Sprite ):
	def __init__(self, z: int, image: Surface, *groups: Group, **anchor) -> None:
		super().__init__(*groups)

		self.z = z
		self.image = image
		self.rect = self.image.get_frect(**anchor)
		self.y_order = self.rect.centery