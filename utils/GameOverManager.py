from functools import reduce
from typing import Literal

from pygame import surface


from settings import *
from utils.Helper import add_color_to_surface, font_loader, add_background_to_text, display_item, get_canvas, get_rect, get_sized_surface, get_text_surface, quit_game, set_truthy, compose
from utils.Singleton import SingletonMeta
from utils.Types import Pos


class GameOverManager ( metaclass=SingletonMeta ):
	def __init__( self ) -> None:
		self.fonts = {
			'giant': font_loader('dogicapixelbold', 80),
			'option': font_loader('PixeloidSan', 24)
		}
		self.canvas = get_canvas()
		self.state: Literal[ 'undecided', 'save', 'play_again', 'quit' ] = 'undecided'
		
		self.is_game_over, self.is_saved = False, False
		self.text = 'GAME OVER LOSER'
		self.options = [ 'SAVE', 'TRY AGAIN IF YOU DARE', 'QUIT' ]


	def __display_positive_message ( self, fonts ):
		return compose(
			lambda font: get_text_surface(font, self.text),
			lambda surface: add_background_to_text(surface, 60),
			lambda surface: get_rect(surface, center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)),
			lambda datas: display_item(self.canvas, datas)
		)( fonts ) 

	
	def __make_button ( self, text: str ):
		return compose(
			lambda text: get_text_surface(self.fonts['option'], text),
			lambda surface: add_background_to_text(surface, 20)
		)( text )


	def __blit_first_button ( self, datas: tuple[Surface, FRect], buttons: list[Surface] ):
		surface, rect = datas
		surface.blit(buttons[0], rect.topleft)
		return datas

	def __blit_second_button ( self, datas: tuple[Surface, FRect], buttons: list[Surface] ):
		surface, rect = datas
		surface.blit(buttons[1], rect.topleft + vector2(buttons[0].width, 0))
		return datas

	def __blit_third_button ( self, datas: tuple[Surface, FRect], buttons: list[Surface] ):
		surface, rect = datas
		surface.blit(buttons[2], rect.topleft + vector2(buttons[0].width + buttons[1].width, 0))
		return datas

	def __display_options ( self, message_rect: FRect ):
		buttons = [ self.__make_button(option) for option in self.options ]	
		voyeur(f'Game Over Manager __display_options -> {buttons}')
		compose(
			lambda buttons: get_sized_surface(reduce(lambda total, button: total + button.width, buttons, 0) + 20, buttons[0].height),
			lambda surface: add_color_to_surface(surface),
			lambda surface: get_rect(surface, midtop=message_rect.midbottom + vector2(0, 20)),
			lambda datas: display_item(self.canvas, datas)
		)( buttons )

	def __display_game_over_screen ( self ):
		self.canvas.fill('black')
		return compose(
			self.__display_positive_message,
			self.__display_options,
		)( self.fonts['giant'] )

	def __save_progress ( self ):
		if self.is_saved: return
		set_truthy(self, 'is_saved')
		print('Saving game')
	
	def __play_new_game ( self ):
		print('Playing new game')

	def update ( self ):
		if not self.is_game_over: return
		self.__display_game_over_screen()

		match self.state:
			case 'save': self.__save_progress()
			case 'play_again': self.__play_new_game()
			case 'quit': quit_game()