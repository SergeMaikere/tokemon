from functools import partial
from pygame import Font

from settings import *
from entities.Monster import Monster
from utils.Helper import add_background_to_text, pipe, get_text_surface
from utils.MyGroup import MyGroup
from utils.Types import Trainers


class MonsterNameSprite ( pygame.sprite.Sprite ):

	def __init__( self, entity: Trainers, monster: Monster, monster_rect: FRect, font: Font, *groups: MyGroup ) -> None:
		super().__init__(*groups)

		self.entity = entity
		self.monster = monster

		self.image = pipe( partial(get_text_surface, font), add_background_to_text )(self.monster.name)
		self.rect = self.image.get_frect(midright=monster_rect.midleft + vector(16, -70)) if self.entity == 'player' else self.image.get_frect(midleft=monster_rect.midright + vector(-16, -70))

	