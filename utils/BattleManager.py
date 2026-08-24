from pygame import Font

from settings import *
from entities.Entity import Entity
from entities.Player import Player
from gameobj.MonsterPatch import MonsterPatch
from gameobj.Battle import Battle
from utils.GameOverManager import GameOverManager
from utils.Helper import images_loader_dict, set_none, set_truthy
from utils.MyGroup import MyGroup
from utils.Transition import Transition
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
		self.battle, self.character, self.patch = None, None, None

		self.transition_overworld = Transition(self.player, lambda _: set_none(self, 'battle'))
		self.state = 'standby'


	def battle_trainer ( self, character: Entity ):	
		self.character = character
		self.battle = Battle( self.battle_grounds[character.datas['biome']], self.fonts, self.ui_images, character.datas['monsters'], *self.groups )
		self.state = 'ongoing'

	def battle_monsters ( self, sprite: MonsterPatch ):
		self.patch = sprite
		monsters = { i: (monster_name, sprite.level) for i, monster_name in enumerate(sprite.monsters) }
		self.battle = Battle( self.battle_grounds[sprite.biome], self.fonts, self.ui_images, monsters, *self.groups )
		self.state = 'ongoing'

	def __handle_victory ( self ):
		if self.character:
			self.character.datas['defeated'] = True
			set_none(self, 'character')

		if self.patch:
			set_truthy(self.patch, 'defeated')
			set_none(self, 'patch')

		self.transition_overworld.start()
		self.state = 'back_to_world'

	def __handle_defeat ( self ):
		set_truthy(self.GO, 'is_game_over')
		self.transition_overworld.start()
		self.state = 'back_to_world'

	def __check_victory ( self ):
		if self.battle and self.battle.victory and self.state == 'ongoing':
			self.state = 'victory'

	def __check_defeat ( self ):
		if self.battle and self.battle.defeat and self.state == 'ongoing':
			self.state = 'defeat'

	def __update_battle ( self, dt: float ):
		if not self.battle: return
		self.battle.update(dt)

	def __update_transition ( self, dt: float ):
		if self.transition_overworld.state == 'standby': self.state = 'standby'
		self.transition_overworld.update(dt)

	def update ( self, dt: float ):
		match self.state:
			case 'standby': return
			case 'victory': self.__handle_victory()
			case 'defeat': self.__handle_defeat()
			case 'back_to_world': self.__update_transition(dt)
		
		self.__check_victory()
		self.__check_defeat()
		self.__update_battle(dt)
