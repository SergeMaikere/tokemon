
from pytmx.pytmx import ColorLike
from functools import partial
from typing import Any

from pygame import Font

from settings import *
from utils.Helper import display_item, get_rect, get_text_surface, pipe, required
from utils.Types import Colors, Size

my_colors: Colors = {
	'bg': 'white',
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
		self.main_rect = self._get_main_rect(pos)


	def __get_card_dimensions ( self ): return ( self.size['width'], self.size['height'] / len(self.my_list) )

	def _get_main_rect ( self, pos: Point ):
		return pygame.FRect((0, 0), (self.width, self.size['height'])).move_to(midleft=pos + vector2(20, 0))

	def __set_v_offset ( self ): 
		return 0 if self.index < self.visible_items else (self.index - self.visible_items + 1)

	def __get_text_surface ( self, font: Font, color: ColorLike, text: str ):
		return font.render(text, False, color)

	def draw_list ( self ):
		v_offset = self.__set_v_offset()
		for i , text in enumerate(self.my_list):
			pipe(	
				partial(self.__get_text_surface, self.font, self.colors.height['text']),
				partial(get_rect, center=self.main_rect.midtop + vector2(0, self.height/2 + i * self.height + v_offset)),
				partial(display_item, self.canvas)
			)(text)
