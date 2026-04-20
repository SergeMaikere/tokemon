from functools import partial, reduce
from pygame import FRect, Font
from random import sample, randint

from pygame.key import ScancodeWrapper

from entities.Player import Player
from settings import *
from assets.data.game_data import MONSTER_DATA
from entities.Monster import Monster
from utils.Helper import pipe, required, images_loader_dict

class MonsterIndex:
	def __init__( self, player: Player, fonts: dict[str, Font ] ) -> None:
		self.player = player
		self.fonts = fonts

		self.monsters = self.__get_random_monsters(8)
		self.monsters_icons = images_loader_dict('assets', 'graphics', 'icons')

		self.canvas = required(pygame.display.get_surface())
		self.tint_surface = self.__get_tinted_surface()

		self.main_rect = pygame.FRect(0, 0, self.canvas.width * 0.6, self.canvas.height * 0.8).move_to(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.list_index = 0
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
		self.__display_monster_index(keys)
		self.__up_and_down(keys)

	def __display_monster_index ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_RETURN]:
			self.player.is_mobile = not self.player.is_mobile
			self.open = not self.open

	def __up_and_down ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_UP]: self.list_index -= 1
		if keys[pygame.K_DOWN]: self.list_index += 1
		self.list_index = self.list_index % len(self.monsters)


	def __tint ( self ): self.canvas.blit(self.tint_surface, (0, 0))

	def __display ( self ):
		# display index's rect
		self.__draw_main_rect()
		# display side list
		self.__display_side_list()

	def __draw_main_rect ( self ):
		pygame.draw.rect(self.canvas, COLORS['black'], self.main_rect)

	def __display_side_list ( self ):
		for i, monster in self.monsters.items():
			pipe(
				self.__set_card,
				partial(self.__set_text, i),
				partial(self.__set_icon, i),
				partial(self.__draw_card, i)
			)(i)

	def __set_v_offset ( self ): 
		return 0 if self.list_index < self.max_list_items else (self.list_index - self.max_list_items + 1)

	def __set_card ( self, i: int ):
		v_offset = self.__set_v_offset()
		top = self.main_rect.top + (i - v_offset) * self.card_height
		card_rect = pygame.FRect(self.main_rect.left, top, self.card_width, self.card_height)
		return card_rect

	def __set_text ( self, i: int, card_rect: FRect ):
		text_surface = self.fonts['regular'].render(self.monsters[i].name, False, COLORS['pure white'])
		text_rect = text_surface.get_frect(midleft=card_rect.midleft + vector2(90, 0))
		return (card_rect, text_surface, text_rect)

	def __set_icon ( self, i: int, datas: tuple[FRect, Surface, FRect] ):
		card_rect =  datas[0]
		icon_surface = self.monsters_icons[self.monsters[i].name]
		icon_rect = icon_surface.get_frect(midleft=card_rect.midleft + vector2(15, 0))
		return ( *datas, icon_surface, icon_rect )

	def __draw_card ( self, i: int, datas: tuple[FRect, Surface, FRect, Surface, FRect] ):
		if datas[0].colliderect(self.main_rect):
			card_rect, text_surface, text_rect, icon_surface, icon_rect = datas
			bg_color = COLORS['gray'] if self.list_index == i else COLORS['light']
			pygame.draw.rect(self.canvas, bg_color, card_rect)
			self.canvas.blit(text_surface, text_rect)
			self.canvas.blit(icon_surface, icon_rect)


	def update ( self, dt: float ):
		self.__input()
		if self.open:
			self.__tint()
			self.__display()		