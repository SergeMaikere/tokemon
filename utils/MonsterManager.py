from os.path import join
from random import randint, sample

from assets.data.game_data import ATTACK_DATA, MONSTER_DATA
from gameobj.MonsterSprite import MonsterSprite
from settings import *
from entities.Monster import Monster
from utils.Helper import get_frame_outline, images_loader_dict, monsters_frames_loader, required
from utils.Types import Attacks, MonsterNames, Trainers



class MonsterManager:
		
	monsters = None

	monster_frames = None

	monster_frames_outlines = None

	monsters_icons = None

	monsters_max_stats = None

	@classmethod
	def init ( cls ):
		cls.monsters = cls.get_random_monsters(2)

		cls.monster_frames = monsters_frames_loader(join('assets', 'graphics', 'monsters'))

		cls.monster_frames_outlines = get_frame_outline(cls.monster_frames, 4)

		cls.monsters_icons = images_loader_dict('assets', 'graphics', 'icons')

		cls.monsters_max_stats = cls.get_max_stats_value()

	@classmethod
	def get ( cls, key ):
		if key in cls.__dict__:
			return required(getattr(cls, key))
		raise KeyError(key)

	@classmethod
	def get_random_monsters ( cls, n: int ):
		# return { i: monster for i, monster in enumerate([Monster(monster_name, randint(1, 5)) for monster_name in sample([name for name in MONSTER_DATA.keys()], n)]) }
		# return { i: monster for i, monster in enumerate([Monster(monster_name, randint(1, 50)) for monster_name in sample([name for name in MONSTER_DATA.keys()], n)]) }
		return { i: monster for i, monster in enumerate([Monster(name, 30) for name in [name for name, data in MONSTER_DATA.items() if len(data['abilities']) > 4]]) }
	
	@classmethod	
	def get_monster_list ( cls ): return [ monster for monster in cls.monsters.values() ]

	@classmethod
	def get_attack_data ( cls, attack: Attacks, data: str ): return ATTACK_DATA[attack][data]

	@classmethod
	def get_max_stats_value ( cls ):
		max_stats = {}
		for monster in MONSTER_DATA.values():
			for stat, value in {prop: val for prop, val in monster['stats'].items() if prop != 'element'}.items():
				max_stats[stat] = value if not stat in max_stats else max(max_stats[stat], value)
		return { stat.replace('max_', ''): value for stat, value in max_stats.items()}

	@classmethod
	def get_player_battle_monsters ( cls ): return [ monster for monster in cls.monsters.values() ]
	
	@classmethod	
	def get_opponent_battle_monsters ( cls, opponent_monsters: dict[int, tuple[MonsterNames, int]] ): 
		return [ Monster(data[0], data[1]) for data in  opponent_monsters.values() ]

	@classmethod
	def remove_monster ( cls, sprite: MonsterSprite ):
		cls.monsters = { i: m for i, m in cls.monsters.items() if m != sprite.monster }
		return sprite

	@classmethod
	def heal_player_monsters ( cls ):
		for monster in cls.monsters.values():
			monster.health = monster.get_stat('max_health')


