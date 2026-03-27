from pygame import Font
from gameobj.Sprite import Sprite
from settings import *
from entities.Character import Character
from utils.AllSprites import AllSprites
from utils.Helper import font_loader


class Dialog:
	def __init__ ( self, character: Character, all_sprites: AllSprites ):

		self.character = character
		self.all_sprites = all_sprites

		self.index = 0
		self.dialogs = self.character.datas['dialog']['default' if not self.character.datas['defeated'] else 'defeated']
		
		self.font: Font = font_loader('PixeloidSans')

		self.image = self.get_surface()
		self.dialog_sprite = self.__get_sprite()

	def get_surface ( self ):
		return self.font.render(self.dialogs[self.index], False, COLORS['black'], COLORS['pure white'])

	def __get_sprite ( self ):
		return Sprite('dialog', WORLD_LAYERS['top'], self.image, self.all_sprites, midbottom=self.character.rect.midtop)

	def update ( self ):
		self.index += 1
		if self.dialog_sprite: self.dialog_sprite.kill()
		if self.index < len(self.dialogs):
			self.image = self.get_surface()
			self.dialog_sprite = self.__get_sprite()
		else:
			self.index = 0
