from gameobj.Sprite import Sprite
from settings import *
from utils.MyGroup import MyGroup
from utils.Timer import Timer

class TimedSprite ( Sprite ):
	def __init__(self, duration: int, image: Surface, *groups: MyGroup, **anchor: tuple[float, float]) -> None:
		super().__init__('timed sprite', BATTLE_LAYERS['overlay'], image, *groups, **anchor)

		self.timer = Timer(duration, func=lambda: self.kill(), autostart=True)

	def update ( self, _ ):
		self.timer.update()