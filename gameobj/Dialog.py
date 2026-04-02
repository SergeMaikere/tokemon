from typing import Callable
from settings import *
from pygame import Font
from gameobj.Sprite import Sprite
from entities.Character import Character
from utils.AllSprites import AllSprites
from utils.Helper import font_loader


class Dialog:
	def __init__ ( self, character: Character, finish_dialog: Callable, all_sprites: AllSprites ):

		self.character = character
		self.finish_dialog = finish_dialog
		self.all_sprites = all_sprites

		self.index = 0
		self.dialogs = self.character.datas['dialog']['default' if not self.character.datas['defeated'] else 'defeated']
		
		self.font: Font = font_loader('PixeloidSans')

		self.dialog_sprite = self.__get_sprite()

	def get_surface ( self ):
		return self.font.render(self.dialogs[self.index], False, COLORS['black'], COLORS['pure white'])

	def __get_sprite ( self ):
		return Sprite('dialog', WORLD_LAYERS['top'], self.get_surface(), self.all_sprites, midbottom=self.character.rect.midtop)

	def __kill_current_sprite ( self ):
		if self.dialog_sprite: self.dialog_sprite.kill()	

	def __finish_dialog ( self ):
		if self.index >= len(self.dialogs): 
			self.finish_dialog(self)

	def __create_new_dialog_sprite ( self ): 
		if self.index < len(self.dialogs):
			self.dialog_sprite = self.__get_sprite()

	def update ( self ):
		self.index += 1
		self.__kill_current_sprite()
		self.__finish_dialog()
		self.__create_new_dialog_sprite()
		
