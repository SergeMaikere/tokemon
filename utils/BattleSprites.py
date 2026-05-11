from pygame.sprite import Sprite

from settings import *
from utils.Helper import required
from utils.MyGroup import MyGroup


class BattleSprites ( MyGroup ):
	def __init__(self, *sprites: Sprite) -> None:
		super().__init__('battle_sprites', *sprites)

		self.canvas = required(pygame.display.get_surface())

	def draw ( self ):
		for sprite in sorted(self, key=lambda sprite: sprite.z):
			if sprite.z == BATTLE_LAYERS['outline']:	
				self.canvas.blit(sprite.image, sprite.rect)

			self.canvas.blit(sprite.image, sprite.rect)
