from functools import reduce
from typing import Callable
from pygame.key import ScancodeWrapper

from settings import *
from entities.Player import Player
from utils.Helper import font_loader, add_background_to_text, display_item, get_canvas, get_rect, get_sized_surface, get_text_surface, quit_game, set_falsy, set_truthy, compose
from utils.MusicManager import MusicManager
from utils.Singleton import SingletonMeta
from utils.Transition import Transition
from utils.MonsterManager import MonsterManager as MM
from utils.Types import GameOverOptions, GameOverStates

class GameOverManager ( metaclass=SingletonMeta ):
	def __init__( self, player: Player, reset_player: Callable, reset_characters: Callable ) -> None:
		self.player = player
		self.reset_player = reset_player
		self.reset_characters = reset_characters

		self.fonts = {
			'giant': font_loader('dogicapixelbold', 80),
			'option': font_loader('PixeloidSan', 24)
		}
		self.canvas = get_canvas()
		self.state: GameOverStates = 'undecided'
		
		self.text = 'GAME OVER LOSER'
		self.options: list[GameOverOptions] = [ {'text': 'TRY AGAIN IF YOU DARE', 'state': 'play_again'}, {'text': 'QUIT', 'state': 'quit'} ]
		self.button_padding_x, self.button_padding_y = 10, 20
		
		self.index = 0
		self.is_game_over, self.is_saved = False, False

		self.transition_overworld = Transition(self.player, self.__display_overworld)


	def __display_overworld ( self, _ ):
		set_falsy(self, 'is_game_over')
		self.state = 'undecided'
		self.player.state = 'down'
		self.reset_player()
		self.reset_characters()
		MM.set_monsters()
		MusicManager.switch('game_over', 'overworld')

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
	
	def __play_new_game ( self, dt: float ):
		if self.transition_overworld.state == 'standby':
			self.transition_overworld.start()
		self.transition_overworld.update(dt)

	def update ( self, dt: float ):
		if not self.is_game_over: return
		self.__input()
		self.__display_game_over_screen()

		match self.state:
			case 'play_again': self.__play_new_game(dt)
			case 'quit': quit_game()