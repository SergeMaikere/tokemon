from settings import *
from gameobj.Sprite import Sprite

class AnimatedSprite ( Sprite ):
	def __init__(self, z: int, frames: list[Surface], *groups: Group, **anchor) -> None:
		super().__init__(z, frames[0], *groups, **anchor)

		self.index, self.frames = 0, frames
		self.image = self.frames[self.index]

	def _animate ( self, dt: float ):
		self.index += ANIMATION_SPEED * dt
		self.image = self.frames[ int(self.index) % len(self.frames) ]

	def update ( self, dt: float ):
		self._animate(dt)