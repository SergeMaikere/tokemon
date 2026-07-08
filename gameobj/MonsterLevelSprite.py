from pygame.font import Font

from settings import *
from gameobj.MonsterInfoSprite import MonsterInfoSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.MyGroup import MyGroup
from utils.Helper import add_color_to_surface, add_text_to_card, get_progress_bar, get_rect, get_text_surface, compose


class MonsterLevelSprite ( MonsterInfoSprite ):

	def __init__(self, monster_sprite: MonsterSprite, name_rect: FRect, font: Font, *groups: MyGroup) -> None:
		super().__init__(monster_sprite, font, *groups)

		self.name_rect = name_rect

		self.card_surface = pygame.Surface((60, 26))

		self.image, self.rect = self.__set_image_rect()

		self.xp_bar_rect = pygame.FRect(0, self.rect.height - 2, self.rect.width, 2)

	def __set_image_rect (  self ) -> tuple[ Surface, FRect ]:
		return compose( add_color_to_surface, self.__get_card_rect )( self.card_surface )

	def __get_card_rect ( self, card_surface: Surface ) -> tuple[ Surface, FRect ]:
		if self.entity == 'player': return get_rect(card_surface, topleft=self.name_rect.bottomleft)
		return get_rect(card_surface, topright=self.name_rect.bottomright)

	def __add_text ( self ):
		level_surface = get_text_surface(self.font, f'Lvl: {self.monster.level}')
		return add_text_to_card(self.image, level_surface)

	def __display_xp_bar ( self ):
		get_progress_bar(self.image, self.xp_bar_rect, COLORS['white'], COLORS['black'], self.monster.xp, self.monster.level_up)

	def update ( self, _ ):
		self.die_with_monster()
		self.image = self.__add_text()
		self.__display_xp_bar()
	