from functools import partial
from pygame import Font, display

from settings import *
from utils.Helper import add_color_to_surface, display_item, get_rect, get_text_surface, pipe, required
from utils.MyGroup import MyGroup
from gameobj.MonsterSprite import MonsterSprite

class MonsterStatsSprite ( pygame.sprite.Sprite ):

	def __init__( self, monster_sprite: MonsterSprite, font: Font, *groups: MyGroup ) -> None:
		super().__init__(*groups)

		self.font = font
		self.monster_rect = monster_sprite.rect
		self.monster = monster_sprite.monster

		self.progress_bars_colors = ( (COLORS['red'], COLORS['white']), (COLORS['blue'], COLORS['white']) )
		self.infos = self.monster.get_battle_infos()

		self.image: Surface = pygame.Surface((150, 48))
		self.rect: FRect = self.image.get_frect(midtop=self.monster_rect.midbottom + vector(0, -20))


	def __display_progress_bar ( self, i: int, value: float, max_value: float ):		
		if i > 1: return
		pipe(
			partial(get_rect, midleft=(self.rect.left, self.rect.top + i * self.rect.height/2)),
			partial(display_item, self.image),

		)( get_text_surface(self.font, f'{value}/{max_value}') )


	def update ( self, _ ):
		add_color_to_surface(self.image)		

		for i, (value, max_value) in enumerate(self.infos):
			self.__display_progress_bar(i, value, max_value)
