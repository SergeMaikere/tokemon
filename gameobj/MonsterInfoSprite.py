from pygame import Font

from settings import *
from gameobj.MonsterSprite import MonsterSprite
from utils.MyGroup import MyGroup

class MonsterInfoSprite ( pygame.sprite.Sprite ):
	def __init__( self, monster_sprite: MonsterSprite, font: Font, *groups: MyGroup ) -> None:
		super().__init__(*groups)

		self.monster_sprite = monster_sprite
		self.entity = self.monster_sprite.entity
		self.monster = self.monster_sprite.monster
		self.font = font

		self.z = BATTLE_LAYERS['name']

	def die_with_monster ( self ):
		if self.monster_sprite.groups(): return
		self.kill()