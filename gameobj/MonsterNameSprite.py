from functools import partial
from pygame import Font

from settings import *
from gameobj.MonsterInfoSprite import MonsterInfoSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.Helper import add_background_to_text, compose, get_text_surface
from utils.MyGroup import MyGroup
from utils.Types import Trainers


class MonsterNameSprite ( MonsterInfoSprite ):

	def __init__(self, monster_sprite: MonsterSprite, monster_rect: FRect, font: Font, *groups: MyGroup) -> None:
		super().__init__(monster_sprite, font, *groups)

		self.image = compose( partial(get_text_surface, font), add_background_to_text )(self.monster.name)
		self.rect: FRect = self.image.get_frect(midright=monster_rect.midleft + vector(40, -60)) if self.entity == 'player' else self.image.get_frect(midleft=monster_rect.midright + vector(-40, -60))

	def update ( self, _ ):
		self.die_with_monster()