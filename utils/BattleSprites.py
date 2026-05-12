from pygame.sprite import Sprite

from gameobj.MonsterSprite import MonsterSprite
from settings import *
from utils.Helper import required
from utils.MyGroup import MyGroup


class BattleSprites ( MyGroup ):
	def __init__(self, *sprites: Sprite) -> None:
		super().__init__('battle_sprites', *sprites)

		self.canvas = required(pygame.display.get_surface())

	def draw_all ( self, current_monster: MonsterSprite ):
		for sprite in sorted(self, key=lambda sprite: sprite.z):
			if sprite.z == BATTLE_LAYERS['outline'] and sprite.monster_sprite == current_monster:
				self.canvas.blit(sprite.image, sprite.rect)

			self.canvas.blit(sprite.image, sprite.rect)
