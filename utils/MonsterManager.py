from os.path import join
from random import randint, sample

from assets.data.game_data import MONSTER_DATA
from settings import *
from entities.Monster import Monster
from utils.Helper import images_loader_dict, monsters_frames_loader

class MonsterManager :
	def __init__(self) -> None:
		
		self.monsters = self.get_random_monsters(8)

		self.monster_frames = monsters_frames_loader(join('assets', 'graphics', 'monsters'))

		self.monsters_icons = images_loader_dict('assets', 'graphics', 'icons')


	def get_random_monsters ( self, n: int ):
		return { i: monster for i, monster in enumerate([Monster(monster_name, randint(1, 99)) for monster_name in sample([name for name in MONSTER_DATA.keys()], n)]) }
	