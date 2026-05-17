from typing import Callable
from pygame import Font

from settings import *
from entities.Monster import Monster
from gameobj.MyList import MyList
from utils.MonsterManager import MonsterManager
from utils.Types import Colors
from utils.Helper import compose, display_item, get_rect, get_text_surface

colors: Colors = {
	'bg': COLORS['white'],
	'text': COLORS['light'],
	'bg_selected': COLORS['dark-white'],
	'text_selected': COLORS['black']
}

class SwitchList ( MyList ):
	def __init__(self, monster_manager: MonsterManager, font: Font, pos: Point, get_index: Callable, colors: Colors = colors ) -> None:
		super().__init__([monster for monster in monster_manager.monsters.values()], {'width': 300, 'height': 400}, 4, font, pos, get_index, colors)

		self.MM = monster_manager



	def _set_icon ( self, monster: Monster, card_rect: FRect ):
		if not card_rect: return
		compose( 
			lambda surface: get_rect(surface, midleft=card_rect.midleft + vector2(10)),
			lambda datas: display_item(self.canvas, datas) 
		)( self.MM.monsters_icons[monster.name] )	
		return card_rect	


	def _set_text ( self, i: int, text: str, card_rect: FRect ):
		if not card_rect: return
		return compose(
			lambda text: get_text_surface(self.font, text, self.colors['text' if self.get_index() != i else 'text_selected']), 
			lambda surface: get_rect(surface, midleft=card_rect.midleft + vector2(90, 0)),
			lambda datas: display_item(self.canvas, datas)
		)(text)

	def _draw_list ( self ):
		self._draw_main_rect()

		for i, monster in self.MM.monsters.items():
			compose(	
				self._get_card_rect,
				self._is_card_visible,
				lambda card_rect: self._draw_card_text(i, card_rect),
				lambda card_rect: self._set_icon(monster, card_rect),
				lambda card_rect: self._set_text(i, monster.name, card_rect),
			)(i)