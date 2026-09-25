from random import randint

from pygame import Font

from settings import *
from entities.Entity import Entity
from entities.Player import Player
from gameobj.MonsterPatch import MonsterPatch
from gameobj.Battle import Battle
from utils.GameOverManager import GameOverManager
from utils.EvolutionManager import EvolutionManager
from utils.Helper import images_loader_dict, set_none, set_truthy
from utils.MyGroup import MyGroup
from utils.Transition import Transition
from utils.Types import BattleStates, FontTypes

class BattleManager:
	def __init__( 
			self, 
			player: Player, 
			fonts: dict[FontTypes, Font], 
			ui_images: dict[str, Surface], 
			evolution_manager: EvolutionManager,
			*groups: MyGroup 
		) -> None:

		self.player = player
		self.EM = evolution_manager
		self.GOM = GameOverManager

		self.fonts = fonts
		self.ui_images = ui_images
		self.groups = groups

		self.battle_grounds = images_loader_dict('assets', 'graphics', 'backgrounds')
		self.battle, self.character, self.patch = None, None, None

		self.transition_overworld = Transition(self.player, lambda _: set_none(self, 'battle'))
		self.state: BattleStates = 'standby'
		self.temp = None


	def is_state ( self, state: BattleStates ): return self.state == state

	def set_state( self, state: BattleStates ): 
		self.state = state

	def battle_trainer ( self, character: Entity ):	
		self.character = character
		self.battle = Battle( self.battle_grounds[character.datas['biome']], self.fonts, self.ui_images, character.datas['monsters'], *self.groups )
		self.set_state('ongoing')

	def battle_monsters ( self, sprite: MonsterPatch ):
		self.patch = sprite
		monsters = { i: (monster_name, sprite.level + randint(-3, 3)) for i, monster_name in enumerate(sprite.monsters) }
		self.battle = Battle( self.battle_grounds[sprite.biome], self.fonts, self.ui_images, monsters, *self.groups )
		self.set_state('ongoing')

	def __handle_victory ( self ):
		if self.character:
			self.character.datas['defeated'] = True

		if self.patch:
			set_truthy(self.patch, 'defeated')
			set_none(self, 'patch')

		self.transition_overworld.start()
		self.set_state('back_to_world')

	def __handle_defeat ( self ):
		set_truthy(self.GOM, 'is_game_over')
		self.transition_overworld.start()
		self.set_state('back_to_world')

	def __check_victory ( self ):
		if self.battle and self.battle.victory:
			self.set_state('victory')

	def __check_defeat ( self ):
		if self.battle and self.battle.defeat:
			self.set_state('defeat')

	def __update_battle ( self, dt: float ):
		if not self.battle: return
		self.battle.update(dt)

	def __back_to_main_world ( self, dt: float ):
		if self.transition_overworld.state == 'standby': self.set_state('evolution')
		self.transition_overworld.update(dt)

	def __check_for_evolution ( self ):
		self.EM.handle_evolution()
		self.state = 'evolution_ongoing'

	def __check_for_evolution_end ( self ):
		if self.EM.evolution: return
		self.set_state('defeated_enemy_dialog')

	def update ( self, dt: float ):
		if self.temp != self.state:
			voyeur(f'Battle Manager state => {self.state}')
			self.temp = self.state
		match self.state:
			case 'standby': return
			case 'ongoing':
				self.__check_victory()
				self.__check_defeat()
			case 'victory': self.__handle_victory()
			case 'defeat': self.__handle_defeat()
			case 'back_to_world': self.__back_to_main_world(dt)
			case 'evolution': self.__check_for_evolution()
			case 'evolution_ongoing': self.__check_for_evolution_end()
		self.__update_battle(dt)
