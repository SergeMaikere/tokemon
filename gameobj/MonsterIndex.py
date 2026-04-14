from functools import reduce
from random import sample, randint

from entities.Player import Player
from settings import *
from assets.data.game_data import MONSTER_DATA
from entities.Monster import Monster
from utils.Helper import required

class MonsterIndex:
	def __init__( self, player: Player ) -> None:
		self.player = player
		self.monsters = self.__get_random_monsters(8)

		self.canvas = required(pygame.display.get_surface())
		self.tint_surface = self.__get_tinted_surface()

		self.main_rect = pygame.FRect(0, 0, self.canvas.width * 0.6, self.canvas.height * 0.8).move_to(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.card_width, self.card_height, self.max_list_items = self.__get_card_dimensions(6)

		self.open = False

	def __get_tinted_surface ( self ):
		tint_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		tint_surface.set_alpha(200)
		return tint_surface

	def __get_random_monsters ( self, n: int ):
		return { i: monster for i, monster in enumerate([Monster(monster_name, randint(1, 100)) for monster_name in sample([name for name in MONSTER_DATA.keys()], n)]) }
	
	def __get_card_dimensions ( self, n: int ): return ( self.main_rect.width * 0.3, self.main_rect.height / n, n )


	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_RETURN]:
			self.player.is_mobile = not self.player.is_mobile
			self.open = not self.open

	def __tint ( self ): self.canvas.blit(self.tint_surface, (0, 0))

	def __display_index ( self ):
		# display index's rect
		pygame.draw.rect(self.canvas, COLORS['gray'], self.main_rect)

		# display side list
		self.__display_side_list()

	def __display_side_list ( self ):
		for i, monster in self.monsters.items():
			top = self.main_rect.top + i * self.card_height
			card_rect = pygame.FRect(self.main_rect.left, top, self.card_width, self.card_height)
			pygame.draw.rect(self.canvas, COLORS['pure white'], card_rect)

	def update ( self, dt: float ):
		self.__input()
		if self.open:
			self.__tint()
			self.__display_index()		