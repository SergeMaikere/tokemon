from settings import *
from gameobj.Sprite import Sprite
from utils.MyGroup import MyGroup

class AnimatedSprite ( Sprite ):
	def __init__(self, name: str, z: int, frames: list[Surface], *groups: MyGroup, **anchor) -> None:
		super().__init__(name, z, frames[0], *groups, **anchor)

		self.index, self.frames = 0, frames
		self.image = self.frames[self.index]

	def _animate ( self, dt: float ):
		if self.name == 'monster': print(int(self.index))
		self.index += ANIMATION_SPEED * dt
		self.image = self.frames[ int(self.index) % len(self.frames) ]

	def update ( self, dt: float ):
		self._animate(dt)