
from pygame import Surface
from pygame.sprite import Group
from utils.MyGroup import MyGroup
from gameobj.Sprite import Sprite


class CollisionSprite ( Sprite ):
	def __init__(self, z: int, image: Surface, *groups: MyGroup, **anchor) -> None:
		super().__init__('object', z, image, *groups, **anchor)

		self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)