from typing import Any
from pygame.sprite import Sprite

from gameobj.MonsterSprite import MonsterSprite
from settings import *
from utils.Helper import required
from utils.MyGroup import MyGroup


class BattleSprites ( MyGroup ):
	def __init__(self, *sprites: Sprite) -> None:
		super().__init__('battle_sprites', *sprites)

		self.canvas = required(pygame.display.get_surface())



	def __blit_general ( self, sprite: Sprite ):
		if sprite.z == BATTLE_LAYERS['outline']: return
		self.canvas.blit(sprite.image, sprite.rect)

	def __blit_monster_outline ( self, sprite: Sprite, current_monster: MonsterSprite | None ):
		if not current_monster: return
		if sprite.z != BATTLE_LAYERS['outline']: return
		if sprite.monster_sprite != current_monster: return
		self.canvas.blit(sprite.image, sprite.rect)



	def draw ( self, current_monster: MonsterSprite | None ):
		for sprite in sorted(self, key=lambda sprite: sprite.z):
			self.__blit_general(sprite)
			self.__blit_monster_outline(sprite, current_monster)
