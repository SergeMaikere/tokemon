from settings import *
from functools import partial

from gameobj.Dialog import Dialog
from entities.Entity import Entity
from entities.Player import Player
from utils.MonsterManager import MonsterManager
from utils.AllSprites import AllSprites
from utils.BattleManager import BattleManager
from utils.Timer import Timer
from utils.MyGroup import MyGroup
from utils.Helper import compose
from utils.DialogTools import is_dialog_possible

class DialogManager:
	def __init__ ( self, player: Player, characters: MyGroup, monster_manager: MonsterManager, battle_manager: BattleManager, all_sprites: AllSprites ):

		self.player = player
		self.characters = characters
		self.MM = monster_manager
		self.BM = battle_manager
		self.all_sprites = all_sprites

		self.timer = Timer(500)
		self.current_dialog = None
		self.in_battle = False
		

	def input ( self ):
		if self.in_battle: return
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_SPACE]:
			if self.current_dialog:
				self.__update_current_dialog()
			else:
				self.__initiate_dialog()
			self.timer.start()

	def __update_current_dialog ( self ):
		if not self.current_dialog: return
		self.current_dialog.update()

	def __initiate_dialog ( self ):
		if self.current_dialog: return
		for character in self.characters:
			compose(
				partial(self.__is_dialog_possible, self.player),
				self.__make_character_face_player,
				self._create_dialog,
				self.__immobilize_player
			)(character)

	def __is_dialog_possible ( self, player: Player, character: Entity ):
		if not is_dialog_possible(player, character): return None
		return character

	def __make_character_face_player ( self, character: Entity ):
		if not character: return None
		if self.player.state == 'left': character.state = 'right'
		if self.player.state == 'right': character.state = 'left'
		if self.player.state == 'up': character.state = 'down'
		if self.player.state == 'down': character.state = 'up'
		return character

	def _create_dialog ( self, character: Entity ):
		if not character: return None
		self.current_dialog = Dialog(character, self.finish_dialog, self.all_sprites)
		return character

	def __immobilize_player ( self, character: Entity ): 
		if not character: return None
		self.player.block()
		return character

	def finish_dialog ( self, dialog: Dialog, character: Entity ):
		if character.nurse:
			self.MM.heal_player_monsters()
		else:
			self.__start_battle(character)
		self.player.unblock()
		del dialog

	def __start_battle ( self, character: Entity ):
			self.in_battle = True
			self.current_dialog = None
			self.BM.battle_trainer(character)

	def update ( self ):
		if not self.timer.running: return self.input()
		self.timer.update()


