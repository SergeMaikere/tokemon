from settings import *
from gameobj.Sprite import Sprite
from utils.MyGroup import MyGroup

class AnimatedSprite ( Sprite ):
	def __init__(self, name: str, z: int, frames: list[Surface], *groups: MyGroup, **anchor) -> None:
		super().__init__(name, z, frames[0], *groups, **anchor)

		self.index, self.frames = 0, frames
		self.image = self.frames[self.index]
		self.speed = ANIMATION_SPEED

	def _animate ( self, dt: float ):
		self.image = self._get_image(dt)

	def _get_image ( self, dt: float ):
		self.index += self.speed * dt
		return self.frames[ int(self.index) % len(self.frames) ]

	def update ( self, dt: float ):
		self._animate(dt)