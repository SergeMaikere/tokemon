from pygame import Font

from settings import *
from entities.Entity import Entity
from entities.Player import Player
from gameobj.MonsterPatch import MonsterPatch
from gameobj.Battle import Battle
from utils.GameOverManager import GameOverManager
from utils.Helper import images_loader_dict, set_none, set_truthy
from utils.MyGroup import MyGroup
from utils.Types import FontTypes

class BattleManager:
	def __init__( 
			self, 
			player: Player, 
			fonts: dict[FontTypes, Font], 
			ui_images: dict[str, Surface], 
			*groups: MyGroup 
		) -> None:

		self.player = player
		self.GO = GameOverManager

		self.fonts = fonts
		self.ui_images = ui_images
		self.groups = groups

		self.battle_grounds = images_loader_dict('assets', 'graphics', 'backgrounds')
		self.battle, self.character = None, None


	def battle_trainer ( self, character: Entity ):	
		self.character = character
		self.battle = Battle( self.battle_grounds[character.datas['biome']], self.fonts, self.ui_images, character.datas['monsters'], *self.groups )

	def battle_monster ( self, sprite: MonsterPatch ):
		monsters = { i: (monster_name, sprite.level) for i, monster_name in enumerate(sprite.monsters) }
		self.battle = Battle( self.battle_grounds[sprite.biome], self.fonts, self.ui_images, monsters, *self.groups )

	def __handle_victory ( self ):
		if self.character:
			self.character.datas['defeated'] = True
			set_none(self, 'character')
		set_none(self, 'battle')

	def __handle_defeat ( self ):
		set_truthy(self.GO, 'is_game_over')
		set_none(self, 'battle')
		del self.battle

	def update ( self, dt: float ):
		if not self.battle: return
		if self.battle.victory: return self.__handle_victory()
		if self.battle.defeat: return self.__handle_defeat()
		self.battle.update(dt)