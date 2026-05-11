from os.path import join
from random import randint, sample

from assets.data.game_data import ATTACK_DATA, MONSTER_DATA
from settings import *
from entities.Monster import Monster
from utils.Helper import get_frame_outline, images_loader_dict, monsters_frames_loader
from utils.Types import Attacks, MonsterNames

class MonsterManager :
	def __init__(self) -> None:
		
		self.monsters = self.get_random_monsters(8)

		self.monster_frames = monsters_frames_loader(join('assets', 'graphics', 'monsters'))

		self.monster_frames_outlines = get_frame_outline(self.monster_frames, 4)

		self.monsters_icons = images_loader_dict('assets', 'graphics', 'icons')

		self.monsters_max_stats = self.get_max_stats_value()


	def get_random_monsters ( self, n: int ):
		return { i: monster for i, monster in enumerate([Monster(monster_name, randint(1, 50)) for monster_name in sample([name for name in MONSTER_DATA.keys()], n)]) }
	
	def get_attack_data ( self, attack: Attacks, data: str ): return ATTACK_DATA[attack][data]

	def get_max_stats_value ( self ):
		max_stats = {}
		for monster in MONSTER_DATA.values():
			for stat, value in {prop: val for prop, val in monster['stats'].items() if prop != 'element'}.items():
				max_stats[stat] = value if not stat in max_stats else max(max_stats[stat], value)
		return { stat.replace('max_', ''): value for stat, value in max_stats.items()}

	def get_player_battle_monsters ( self ): 
		return [ monster for key, monster in self.monsters.items() if key < 3 ]

	def get_opponent_battle_monsters ( self, opponent_monsters: dict[int, tuple[MonsterNames, int]] ): 
		return [ Monster(data[0], data[1]) for i, data in  opponent_monsters.items() if i < 3 ] 