from typing import Any
from settings import *
from pygame.sprite import Sprite

class MyGroup ( pygame.sprite.Group ):

	def __init__(self, name: str, *sprites: Sprite) -> None:
		super().__init__(*sprites)

		self.name = name

	def draw_all ( self, *args: Any, **kwargs: Any ):
		pass
