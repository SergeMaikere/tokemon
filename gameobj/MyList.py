
from functools import partial
from typing import Any, Callable
from pygame import Font

from settings import *
from utils.Helper import display_item, get_rect, get_text_surface, compose, required
from utils.Types import Colors, Size

my_colors: Colors = {
	'bg': COLORS['white'],
	'text': 'black',
	'bg_selected': 'gray',
	'text_selected': 'pure white' 
}

class MyList:
	def __init__( self, my_list: list[Any], size: Size, visible_items: int, font: Font, pos: Point, get_index: Callable, colors: Colors = my_colors ) -> None:
		self.my_list = my_list
		self.size = size
		self.visible_items = visible_items
		self.font = font
		self.get_index = get_index
		self.colors = colors

		self.padding = 15 
		self.canvas = required(pygame.display.get_surface())
		self.width, self.height = self._get_card_dimensions()
		self.main_rect = self._get_main_rect(pos)


	def _get_card_dimensions ( self ): return ( self.size['width'], self.size['height'] / self.visible_items )

	def _get_main_rect ( self, pos: Point ):
		return pygame.FRect((0, 0), (self.width, self.size['height'])).move_to(midleft=pos + vector2(self.padding, 0))

	def _draw_main_rect ( self ): return pygame.draw.rect(self.canvas, self.colors['bg'], self.main_rect, 0, 5)

	def _set_v_offset ( self ): 
		return 0 if self.get_index() < self.visible_items else (self.get_index() - self.visible_items + 1)

	def _get_card_rect ( self, i: int ):
		v_offset = self._set_v_offset()
		return pygame.FRect(self.main_rect.left, self.main_rect.top + (i - v_offset) * self.height , self.width, self.height)

	def _is_card_visible ( self, card_rect: FRect ):
		if not card_rect.colliderect(self.main_rect): return
		return card_rect

	def _draw_card_text ( self, i: int, card_rect: FRect ):
		if not card_rect: return
		bg_color = self.colors['bg_selected' if self.get_index() == i else 'bg']
		if card_rect.collidepoint(self.main_rect.midtop):
			return pygame.draw.rect(self.canvas, bg_color, card_rect, 0, 0, 5, 5)
		if card_rect.collidepoint(self.main_rect.midbottom + vector2(1, -1)):
			return pygame.draw.rect(self.canvas, bg_color, card_rect, 0, 0, 0, 0, 5, 5)
		return pygame.draw.rect(self.canvas, bg_color, card_rect)

	def _set_text ( self, i: int, text: str, card_rect: FRect ):
		if not card_rect: return
		return compose(
			lambda text: get_text_surface(self.font, text, self.colors['text' if self.get_index() != i else 'text_selected']), 
			partial(get_rect, center=card_rect.center)
		)(text)
			

	def _blit_text ( self, datas: tuple[Surface, FRect] ):
		if not datas: return
		return display_item(self.canvas, datas)

	def _draw_list ( self ):
		self._draw_main_rect()

		for i ,text in enumerate(self.my_list):
			compose(	
				self._get_card_rect,
				self._is_card_visible,
				partial(self._draw_card_text, i),
				partial(self._set_text, i, text),
				self._blit_text
			)(i)


	def update ( self ):
		self._draw_list()
