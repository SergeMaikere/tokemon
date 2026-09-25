from pygame.font import Font

from settings import *
from gameobj.MonsterInfoSprite import MonsterInfoSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.MyGroup import MyGroup
from utils.Helper import add_color_to_surface, add_text_to_card, get_progress_bar, get_rect, get_text_surface, compose


class MonsterLevelSprite ( MonsterInfoSprite ):

	def __init__(self, monster_sprite: MonsterSprite, name_rect: FRect, font: Font, *groups: MyGroup) -> None:
		super().__init__(monster_sprite, font, *groups)

		self.card_surface, self.rect = self.__set_image_datas(name_rect, pygame.Surface((60, 26)))

		self.image = self.card_surface.copy()

		self.xp_bar_rect = pygame.FRect(0, self.rect.height - 2, self.rect.width, 2)

		self.temp_xp = self.monster.xp

	def __set_image_datas (  self, name_rect: FRect, card_surface: Surface ) -> tuple[ Surface, FRect ]:
		return compose( add_color_to_surface, lambda surface: self.__get_card_rect(name_rect, surface) )( card_surface )

	def __get_card_rect ( self, name_rect: FRect, card_surface: Surface ) -> tuple[ Surface, FRect ]:
		if self.entity == 'player': return get_rect(card_surface, topleft=name_rect.bottomleft)
		return get_rect(card_surface, topright=name_rect.bottomright)

	def __add_text ( self ):
		return compose(
			lambda level: get_text_surface(self.font, f'Lvl: {level}'),
			lambda surface: add_text_to_card(self.card_surface, surface) 
		)( self.monster.level )

	def __display_level ( self ):
		self.image.fill('white')
		self.image = self.__add_text()


	def __display_xp_bar ( self ):
		get_progress_bar(self.image, self.xp_bar_rect, COLORS['white'], COLORS['black'], self.monster.xp, self.monster.level_up)

	def update ( self, _ ):
		self.die_with_monster()
		self.__display_level()
		self.__display_xp_bar()
	