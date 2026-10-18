from functools import reduce
from typing import Literal

from pygame import surface
from pygame.key import ScancodeWrapper


from settings import *
from utils.Helper import add_color_to_surface, font_loader, add_background_to_text, display_item, get_canvas, get_rect, get_sized_surface, get_text_surface, quit_game, set_truthy, compose
from utils.Singleton import SingletonMeta
from utils.Types import GameOverOptions, GameOverStates, Pos


class GameOverManager ( metaclass=SingletonMeta ):
	def __init__( self ) -> None:
		self.fonts = {
			'giant': font_loader('dogicapixelbold', 80),
			'option': font_loader('PixeloidSan', 24)
		}
		self.canvas = get_canvas()
		self.state: GameOverStates = 'undecided'
		
		self.text = 'GAME OVER LOSER'
		self.options: list[GameOverOptions] = [ {'text': 'SAVE', 'state': 'save'}, {'text': 'TRY AGAIN IF YOU DARE', 'state': 'play_again'}, {'text': 'QUIT', 'state': 'quit'} ]
		self.button_padding_x, self.button_padding_y = 10, 20
		
		self.index = 0
		self.is_game_over, self.is_saved = False, False


	def __left_and_right ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_LEFT]: self.index -= 1
		if keys[pygame.K_RIGHT]: self.index += 1
		self.index = self.index % len(self.options)

	def __select_option ( self, keys: ScancodeWrapper ):
		if not keys[pygame.K_SPACE]: return
		self.state = self.options[self.index]['state']

	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		self.__left_and_right(keys)
		self.__select_option(keys)

	def __display_positive_message ( self, fonts ):
		return compose(
			lambda font: get_text_surface(font, self.text),
			lambda surface: add_background_to_text(surface, 60),
			lambda surface: get_rect(surface, center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)),
			lambda datas: display_item(self.canvas, datas)
		)( fonts ) 

	
	def __make_button ( self, index: int, text: str ):
		return compose(
			lambda text: get_text_surface(font=self.fonts['option'], text=text, color=COLORS['black'] if index == self.index else COLORS['white']),
			lambda surface: add_background_to_text(surface=surface, color=COLORS['light'] if index == self.index else COLORS['gray'])
		)( text )


	def __get_button_pos ( self, index: int, buttons: list[Surface] ):
		if index == 1: return buttons[0].width + self.button_padding_x
		if index == 2: return buttons[0].width + buttons[1].width + self.button_padding_x * 2
		return 0

	def __blit_button ( self, banner_rect: FRect, buttons: list[Surface] ):
		for i, button in enumerate(buttons):
			x = self.__get_button_pos(i, buttons)
			button_rect = button.get_rect(topleft=banner_rect.topleft + vector2(x, 0))
			self.canvas.blit(button, button_rect)
		return banner_rect

	def __display_options ( self, message_rect: FRect ):
		buttons = [ self.__make_button(i, option['text']) for i, option in enumerate(self.options) ]	
		compose(
			lambda buttons: get_sized_surface(reduce(lambda total, button: total + button.width, buttons, 0) + self.button_padding_y, buttons[0].height),
			lambda surface: get_rect(surface, midtop=message_rect.midbottom + vector2(0, self.button_padding_x * 2)),
			lambda datas: display_item(self.canvas, datas),
			lambda rect: self.__blit_button(rect, buttons),
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
		self.__input()
		self.__display_game_over_screen()

		match self.state:
			case 'save': self.__save_progress()
			case 'play_again': self.__play_new_game()
			case 'quit': quit_game()