from settings import *
from typing import Callable
from pygame import Font

from gameobj.Sprite import Sprite
from entities.Character import Character
from utils.AllSprites import AllSprites
from utils.Helper import font_loader, pipe
from utils.Types import Size


class Dialog:
	def __init__ ( self, character: Character, finish_dialog: Callable, all_sprites: AllSprites ):

		self.character = character
		self.finish_dialog = finish_dialog
		self.all_sprites = all_sprites

		self.index = 0
		self.dialogs = self.character.datas['dialog']['default' if not self.character.datas['defeated'] else 'defeated']
		
		self.font: Font = font_loader('PixeloidSans')
		self.padding = 5
		self.dialog_sprite = self.__create_dialog_sprite()


	
	def __create_dialog_sprite ( self ):
		return pipe(
			self.__get_dims,
			self.__make_bg,
			self.__make_bulle_surf,
			self.__make_bulle_sprite
		)(self.__get_text_surface())

	def __get_text_surface ( self ):
		return self.font.render(self.dialogs[self.index], False, COLORS['black'], COLORS['pure white'])

	def __get_dims ( self, text_surf: Surface ):
		width = max( 30, text_surf.get_width() + 2 * self.padding )
		height = text_surf.get_height() + 2 * self.padding
		return ( text_surf, {'width': width, 'height': height} )

	def __make_bg ( self, datas: tuple[Surface, Size] ):
		text_surf, size = datas
		bg_surf = pygame.Surface((size['width'], size['height']), pygame.SRCALPHA)
		bg_surf.fill((0,0,0,0))
		return (text_surf, bg_surf, size)

	def __make_bulle_surf ( self, datas: tuple[Surface, Surface, Size] ):
		text_surf, bg_surf, size = datas
		pygame.draw.rect( bg_surf, COLORS['pure white'], bg_surf.get_frect(topleft=(0, 0)), 0, 4 )
		bg_surf.blit( text_surf, text_surf.get_frect(center=(size['width']/2, size['height']/2)) )
		return bg_surf

	def __make_bulle_sprite ( self, bulle_surf: Surface ):
		return Sprite('dialog', WORLD_LAYERS['top'], bulle_surf, self.all_sprites, midbottom=self.character.rect.midtop)

	def __kill_current_sprite ( self ):
		if self.dialog_sprite: self.dialog_sprite.kill()	

	def __create_new_dialog_sprite ( self ): 
		self.dialog_sprite = self.__create_dialog_sprite()

	def update ( self ):
		self.index += 1
		self.__kill_current_sprite()
		
		if self.index < len(self.dialogs):
			self.__create_new_dialog_sprite()
		else:
			self.finish_dialog(self)
		
