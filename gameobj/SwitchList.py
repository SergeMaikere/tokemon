from typing import Callable
from pygame import Font

from settings import *
from entities.Monster import Monster
from gameobj.MyList import MyList
from utils.MonsterManager import MonsterManager
from utils.Types import Colors
from utils.Helper import compose, display_item, get_progress_bar, get_rect, get_text_surface, required

colors: Colors = {
	'bg': COLORS['white'],
	'text': COLORS['light'],
	'bg_selected': COLORS['dark-white'],
	'text_selected': COLORS['black']
}

class SwitchList ( MyList ):
	def __init__(self, monster_manager: MonsterManager, font: Font, pos: Point, get_index: Callable, colors: Colors = colors ) -> None:
		super().__init__(monster_manager.get_monster_list(), {'width': 300, 'height': 350}, 4, font, pos, get_index, colors)

		self.MM = monster_manager
		self.bg_padding = 90
		self.selected_index, self.switched = None, None


	def _set_icon ( self, monster: Monster, card_rect: FRect ):
		if not card_rect: return
		compose( 
			lambda surface: get_rect(surface, midleft=card_rect.midleft + vector2(10, 0)),
			lambda datas: display_item(self.canvas, datas) 
		)( self.MM.monsters_icons[monster.name] )	
		return card_rect	


	def _set_text ( self, i: int, text: str, card_rect: FRect ):
		if not card_rect: return
		return compose(
			lambda text: get_text_surface(self.font, text, self.colors['text' if self.get_index() != i else 'text_selected']), 
			lambda surface: get_rect(surface, midleft=card_rect.midleft + vector2(self.bg_padding, -10)),
			lambda datas: display_item(self.canvas, datas)
		)(text)

	def __set_health_progress_bar ( self, monster: Monster, text_rect: FRect ):
		if not text_rect: return
		health_rect = pygame.FRect(text_rect.left, text_rect.bottom + 10, self.width * 0.5, 4)
		get_progress_bar(self.canvas, health_rect, self.colors['bg'], COLORS['red'], monster.health, monster.get_stat('max_health'))
		return health_rect

	def __set_energy_progress_bar ( self, monster: Monster, health_rect: FRect ):
		if not health_rect: return
		energy_rect = pygame.FRect(health_rect.left, health_rect.bottom + 3, self.width * 0.5, 4)
		get_progress_bar(self.canvas, energy_rect, self.colors['bg'], COLORS['blue'], monster.energy, monster.get_stat('max_energy'))
		return energy_rect

	def _draw_list ( self ):
		self._draw_main_rect()

		for i, monster in self.MM.monsters.items():
			compose(	
				self._get_card_rect,
				self._is_card_visible,
				lambda card_rect: self._draw_card_text(i, card_rect),
				lambda card_rect: self._set_icon(monster, card_rect),
				lambda card_rect: self._set_text(i, f'{monster.name} ({monster.level})', card_rect),
				lambda card_rect: self.__set_health_progress_bar(monster, card_rect),
				lambda card_rect: self.__set_energy_progress_bar(monster, card_rect)
			)(i)

	def __select_item ( self ): self.selected_index = self.get_index()

	def __swith_item_with_selected ( self ):
		if self.selected_index == self.get_index(): return
		i = required(self.selected_index)
		
		selected_item = self.MM.monsters[i]
		current_item = self.MM.monsters[self.get_index()]
		
		self.MM.monsters[self.get_index()] = selected_item
		self.MM.monsters[i] = current_item
		
		self.selected_index = None
		self.switched = True

	def select ( self ):
		if self.selected_index is None:
			self.__select_item()
		else:
			self.__swith_item_with_selected()