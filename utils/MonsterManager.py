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

		self.monsters_max_stats = self.get_max_stats_value()


	def get_random_monsters ( self, n: int ):
		return { i: monster for i, monster in enumerate([Monster(monster_name, randint(1, 30)) for monster_name in sample([name for name in MONSTER_DATA.keys()], n)]) }
	
	def get_max_stats_value ( self ):
		max_stats = {}
		for monster in MONSTER_DATA.values():
			for stat, value in {prop: val for prop, val in monster['stats'].items() if prop != 'element'}.items():
				max_stats[stat] = value if not stat in max_stats else max(max_stats[stat], value)
		return { stat.replace('max_', ''): value for stat, value in max_stats.items()}