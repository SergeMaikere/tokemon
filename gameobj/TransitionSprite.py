from settings import *
from utils.MyGroup import MyGroup
from gameobj.Sprite import Sprite

class TransitionSprite ( Sprite ):
	def __init__(self, image: Surface, target: str, pos: str, *groups: MyGroup, **anchor: tuple[float, float]) -> None:
		super().__init__('transition', WORLD_LAYERS['main'], image, *groups, **anchor)

		self.target = target
		self.player_spawn_pos = pos