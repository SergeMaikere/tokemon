
from pytmx.pytmx import ColorLike
from functools import partial
from typing import Any

from pygame import Font

from settings import *
from utils.Helper import add_color_to_surface, display_item, get_rect, get_text_surface, pipe, required
from utils.Types import Colors, Size

my_colors: Colors = {
	'bg': COLORS['white'],
	'text': 'black',
	'bg_selected': 'gray',
	'text_selected': 'pure white' 
}

class MyList:
	def __init__( self, my_list: list[Any], size: Size, visible_items: int, font: Font, pos: Point, colors: Colors = my_colors ) -> None:
		self.my_list = my_list
		self.size = size
		self.visible_items = visible_items
		self.font = font
		self.colors = colors

		self.canvas = required(pygame.display.get_surface())
		self.index = 0
		self.width, self.height = self.__get_card_dimensions()
		self.main_rect = self.__get_main_rect(pos)


	def __get_card_dimensions ( self ): return ( self.size['width'], self.size['height'] / self.visible_items )

	def __get_main_rect ( self, pos: Point ):
		return pygame.FRect((0, 0), (self.width, self.size['height'])).move_to(midleft=pos + vector2(20, 0))


	def __set_v_offset ( self ): 
		return 0 if self.index < self.visible_items else (self.index - self.visible_items + 1)

	def __get_card_rect ( self, i: int ):
		v_offset = self.__set_v_offset()
		return pygame.FRect(self.main_rect.left, self.main_rect.top + i * self.height + v_offset, self.width, self.height)

	def __draw_card_text ( self, card_rect: FRect ):
		return pygame.draw.rect(self.canvas, self.colors['bg'], card_rect)

	def __set_text ( self, text: str, card_rect: FRect ):
		text_surface = get_text_surface(self.font, text, self.colors['text'])
		text_rect = text_surface.get_frect(center=card_rect.center)
		return (text_surface, text_rect)

	def draw_list ( self ):
		for i ,text in enumerate(self.my_list):
			pipe(	
				self.__get_card_rect,
				self.__draw_card_text,
				partial(self.__set_text, text),
				partial(display_item, self.canvas)
			)(i)
