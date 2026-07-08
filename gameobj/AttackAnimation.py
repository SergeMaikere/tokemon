

from settings import *
from gameobj.AnimatedSprite import AnimatedSprite
from utils.MyGroup import MyGroup


class AttackAnimation ( AnimatedSprite ):
	def __init__(self, frames: list[Surface], pos: Point, *groups: MyGroup) -> None:
		super().__init__('attack_animation', BATTLE_LAYERS['effects'], frames, *groups, center=pos)



	def _animate ( self, dt: float ):
		if int(self.index) < len(self.frames):
			self.index += self.speed * dt
			self.image = self.frames[ int(self.index) % len(self.frames) ]
		else:
			self.kill()