from gameobj.Sprite import Sprite
from settings import *

class TransitionSprite ( Sprite ):
	def __init__(self, image: Surface, target: str, pos: str, *groups: Group, **anchor: tuple[float, float]) -> None:
		super().__init__('transition', WORLD_LAYERS['main'], image, *groups, **anchor)

		self.target = target
		self.pos = pos