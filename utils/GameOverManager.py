from typing import Literal

from settings import *
from utils.Helper import quit_game, set_truthy


class GameOverManager:
	def __init__( self ) -> None:
		self.is_game_over, self.is_saved = False, False
		self.state: Literal[ 'undecided', 'play_again', 'quit' ] = 'undecided'

	def __display_game_over_screen ( self ):
		print('showing game over screen')

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
			case 'undecided': self.__save_progress()
			case 'play_again': self.__play_new_game()
			case 'quit': quit_game()