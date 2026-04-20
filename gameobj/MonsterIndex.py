from pygame import Font
from pygame.key import ScancodeWrapper

from settings import *
from entities.Player import Player
from gameobj.SideList import SideList
from utils.Helper import required
from utils.MonsterManager import MonsterManager

class MonsterIndex:
	def __init__( self, player: Player, monster_manager: MonsterManager, fonts: dict[str, Font ] ) -> None:
		self.player = player
		self.fonts = fonts

		self.MM = monster_manager

		self.canvas = required(pygame.display.get_surface())
		self.tint_surface = self.__get_tinted_surface()

		self.main_rect = pygame.FRect(0, 0, self.canvas.width * 0.6, self.canvas.height * 0.8).move_to(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.side_list = SideList(self.MM.monsters, self.fonts['regular'], self.main_rect, 6, self.MM.monsters_icons)

		self.open = False

	def __get_tinted_surface ( self ):
		tint_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		tint_surface.set_alpha(200)
		return tint_surface

	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		self.__display_monster_index(keys)
		self.__up_and_down(keys)

	def __display_monster_index ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_RETURN]:
			self.player.is_mobile = not self.player.is_mobile
			self.open = not self.open

	def __up_and_down ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_UP]: self.side_list.index -= 1
		if keys[pygame.K_DOWN]: self.side_list.index += 1
		self.side_list.index = self.side_list.index % len(self.MM.monsters)

	def __draw_main_rect ( self ):
		pygame.draw.rect(self.canvas, COLORS['black'], self.main_rect)
	
	def __tint ( self ): self.canvas.blit(self.tint_surface, (0, 0))

	def __display ( self ):
		if not self.open: return
		self.__tint()
		self.__draw_main_rect()
		self.side_list.display()


	def update ( self, dt: float ):
		self.__input()
		self.__display()		