from functools import partial
from typing import Any
from pygame import FRect, Font

from settings import *
from utils.Helper import pipe, required

class SideList:
	def __init__( self, my_dict: dict[Any, Any], font: Font, main_rect: FRect, visible_items: int, icons: dict[str, Surface] | None = None  ) -> None:
		
		self.main_rect = main_rect
		self.dict = my_dict
		self.font = font
		self.visible_items = visible_items
		self.icons = icons

		self.canvas = required(pygame.display.get_surface())
		self.index = 0
		self.card_width, self.card_height = self.__get_card_dimensions(self.visible_items)


	def __get_card_dimensions ( self, n: int ): return ( self.main_rect.width * 0.3, self.main_rect.height / n )

	def __set_card ( self, i: int ):
		v_offset = self.__set_v_offset()
		top = self.main_rect.top + (i - v_offset) * self.card_height
		card_rect = pygame.FRect(self.main_rect.left, top, self.card_width, self.card_height)
		return card_rect

	def __set_v_offset ( self ): 
		return 0 if self.index < self.visible_items else (self.index - self.visible_items + 1)

	def __is_card_visible ( self, card_rect: FRect ):
		if not card_rect.colliderect(self.main_rect): return
		return card_rect

	def __set_text ( self, item: Any, card_rect: FRect | None ):
		if not card_rect: return
		text_surface = self.font.render(item.name, False, COLORS['white'])
		text_rect = text_surface.get_frect(midleft=card_rect.midleft + vector2(90, 0))
		return (card_rect, text_surface, text_rect)

	def __set_icon ( self, item: Any, datas: tuple[FRect, Surface, FRect] | None ):
		if not datas: return
		if not self.icons: return ( *datas, None, None )
		card_rect =  datas[0]
		icon_surface = self.icons[item.name]
		icon_rect = icon_surface.get_frect(midleft=card_rect.midleft + vector2(15, 0))
		return ( *datas, icon_surface, icon_rect )

	def __draw_card ( self, i: int, datas: tuple[FRect, Surface, FRect, Surface, FRect] | None ):
		if not datas: return
		card_rect, text_surface, text_rect, icon_surface, icon_rect = datas
		bg_color = COLORS['gray'] if self.index == i else COLORS['light']

		pygame.draw.rect(self.canvas, bg_color, card_rect)
		self.canvas.blit(text_surface, text_rect)
		if self.icons: self.canvas.blit(icon_surface, icon_rect)

	def display ( self ):
		for i, item in self.dict.items():
			pipe(
				self.__set_card,
				self.__is_card_visible,
				partial(self.__set_text, item),
				partial(self.__set_icon, item),
				partial(self.__draw_card, int(i))
			)(i)