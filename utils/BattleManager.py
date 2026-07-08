
from settings import *
from pygame import Font
from entities.Entity import Entity
from entities.Player import Player
from gameobj.Battle import Battle
from utils.MonsterManager import MonsterManager
from utils.GameOverManager import GameOverManager
from utils.Helper import images_loader_dict, set_truthy
from utils.MyGroup import MyGroup
from utils.Types import FontTypes

class BattleManager:
	def __init__( 
			self, 
			player: Player, 
			monster_manager: MonsterManager, 
			fonts: dict[FontTypes, Font], 
			ui_images: dict[str, Surface], 
			game_over_manager: GameOverManager,
			*groups: MyGroup 
		) -> None:

		self.player = player
		self.MM = monster_manager
		self.GO = game_over_manager

		self.fonts = fonts
		self.ui_images = ui_images
		self.groups = groups

		self.battle_grounds = images_loader_dict('assets', 'graphics', 'backgrounds')
		self.battle, self.character = None, None


	def battle_trainer ( self, character: Entity ):
		self.character = character
		self.battle = Battle( self.battle_grounds[character.datas['biome']], self.MM, self.fonts, self.ui_images, character.datas['monsters'], *self.groups )

	def __handle_victory ( self ):
		if self.character:
			self.character.datas['defeated'] = True
			self.character = None
		self.battle = None

	def __handle_defeat ( self ):
		set_truthy(self.GO, 'is_game_over')
		self.battle = None

	def update ( self, dt: float ):
		if not self.battle: return
		if self.battle.victory: return self.__handle_victory()
		if self.battle.defeat: return self.__handle_defeat()
		self.battle.update(dt)