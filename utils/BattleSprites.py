from typing import Callable
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
		if hasattr(sprite, 'z') and sprite.z == BATTLE_LAYERS['outline']: return
		self.canvas.blit(sprite.image, sprite.rect)

	def __blit_monster_outline ( self, sprite: Sprite, monster: MonsterSprite | None ):
		if not monster: return
		if sprite.z != BATTLE_LAYERS['outline']: return
		if sprite.monster_sprite != monster: return
		self.canvas.blit(sprite.image, sprite.rect)


	def __highlight_current_monster ( self, sprite: Sprite, monster: MonsterSprite | None, is_player_targeted: Callable  ):
		if is_player_targeted(): return
		self.__blit_monster_outline(sprite, monster)

	def draw_all ( self, current_monster: MonsterSprite | None, targeted_monster: MonsterSprite | None, is_player_targeted: Callable ):
		for sprite in sorted(self, key=lambda sprite: sprite.z):
			self.__blit_general(sprite)
			self.__highlight_current_monster(sprite, current_monster, is_player_targeted)
			self.__blit_monster_outline(sprite, targeted_monster)
