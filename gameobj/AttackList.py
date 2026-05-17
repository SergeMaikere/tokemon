from typing import Callable
from pygame import Font

from assets.data.game_data import ATTACK_DATA
from settings import *
from gameobj.MyList import MyList
from utils.Helper import compose, get_rect, get_text_surface
from utils.Types import Colors

colors: Colors = {
	'bg': COLORS['white'],
	'text': COLORS['light'],
	'bg_selected': COLORS['dark-white'],
	'text_selected': COLORS['black']
}

class AttackList ( MyList ):
	def __init__(self, my_list: list[str], font: Font, pos: Point, get_index: Callable, colors: Colors = colors) -> None:
		super().__init__(my_list, {'width': 150, 'height': 200}, 4, font, pos, get_index, colors)


	def __get_text_color( self, i: int, text: str ):
		selected = ATTACK_DATA[text]['element']
		return self.colors['text'] if self.get_index() != i else COLORS[selected if selected != 'normal' else 'black']

	def _set_text(self, i: int, text: str, card_rect: FRect):
		if not card_rect: return
		return compose(
			lambda text: get_text_surface(self.font, text, self.__get_text_color(i, text)), 
			lambda surface: get_rect(surface, center=card_rect.center)
		)(text)