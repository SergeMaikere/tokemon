from settings import *
from functools import partial
from pygame import Vector2

from gameobj.Dialog import Dialog
from entities.Character import Character
from entities.Player import Player
from utils.AllSprites import AllSprites
from utils.Timer import Timer
from utils.Helper import pipe, is_dialog_possible

class DialogManager:
	def __init__ ( self, player: Player, characters: Group, all_sprites: AllSprites ):

		self.player = player
		self.characters = characters
		self.all_sprites = all_sprites

		self.timer = Timer(500)
		self.current_dialog = None
		

	def input ( self ):
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
			pipe(
				partial(self.__is_dialog_possible, self.player),
				self.__make_character_face_player,
				self.__create_dialog,
				self.__immobilize_player
			)(character)

	def __is_dialog_possible ( self, player: Player, character: Character ):
		if not is_dialog_possible(player, character): return None
		return character

	def __make_character_face_player ( self, character: Character ):
		if not character: return None
		if self.player.state == 'left': character.state = 'right'
		if self.player.state == 'right': character.state = 'left'
		if self.player.state == 'up': character.state = 'down'
		if self.player.state == 'down': character.state = 'up'
		return character

	def __create_dialog ( self, character: Character ):
		if not character: return None
		self.current_dialog = Dialog(character, self.finish_dialog, self.all_sprites)
		return character

	def __immobilize_player ( self, character: Character ): 
		if not character: return None
		self.player.is_mobile = False
		return character

	def finish_dialog ( self, dialog: Dialog ):
		self.current_dialog = None
		self.player.is_mobile = True
		del dialog

	def update ( self ):
		if not self.timer.running: self.input()
		self.timer.update()

