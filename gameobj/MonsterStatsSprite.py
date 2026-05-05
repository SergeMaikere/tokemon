from functools import partial
from pygame import Font, display
from pygame.scrap import get_text

from settings import *
from utils.Helper import add_color_to_surface, display_item, get_progress_bar, get_rect, get_text_surface, pipe, required
from utils.MyGroup import MyGroup
from gameobj.MonsterSprite import MonsterSprite

class MonsterStatsSprite ( pygame.sprite.Sprite ):

	def __init__( self, monster_sprite: MonsterSprite, font: Font, *groups: MyGroup ) -> None:
		super().__init__(*groups)

		self.font = font
		self.monster_rect = monster_sprite.rect
		self.monster = monster_sprite.monster

		self.progress_bars_colors = ( (COLORS['red'], COLORS['black']), (COLORS['blue'], COLORS['black']) )
		self.infos = self.monster.get_battle_infos()

		self.image: Surface = pygame.Surface((150, 48))
		self.rect: FRect = self.image.get_frect(midtop=self.monster_rect.midbottom)


	def __display_health_and_energy ( self, i: int, value: float, max_value: float ):	
		if i > 1: return	
		return pipe(
			partial(get_rect, midleft=(5, 10 + i * self.image.height/2)),
			partial(display_item, self.image),
			partial(self.__display_progress_bar, i, value, max_value)
		)( get_text_surface(self.font, f'{int(value)}/{int(max_value)}') )

	def __display_progress_bar ( self, i: int, value: float, max_value: float, text_rect: FRect ):
		rect = pygame.FRect(text_rect.left, text_rect.bottom - 2, self.rect.width - 10, 3)
		colors = self.progress_bars_colors[i]
		get_progress_bar(self.image, rect, colors[1], colors[0], int(value), int(max_value))

	def update ( self, _ ):
		add_color_to_surface(self.image)	

		for i, (value, max_value) in enumerate(self.infos):
			self.__display_health_and_energy(i, value, max_value)
