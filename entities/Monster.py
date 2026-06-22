from random import randint

from settings import *
from assets.data.game_data import ATTACK_DATA, MONSTER_DATA
from utils.Types import Attacks
from utils.Helper import min_number

class Monster:
	def __init__( self, name: str, level: int ) -> None:
		self.name, self.level = name, level

		self.base_stats = MONSTER_DATA[name]['stats']
		self.element = self.base_stats['element']
		self.abilities = MONSTER_DATA[name]['abilities']

		self.xp = randint(0, 1000)
		self.level_up = self.level * 150
		self.initiative = 0

		self._health = max(0, self.get_stat('max_health'))
		self._energy = max(0, self.get_stat('max_energy'))

	@property
	def health ( self ): return min_number(0, self._health)
	@health.setter
	def health ( self, v: float ): self._health = v

	@property
	def energy ( self ): return min_number(0, self._energy)
	@energy.setter
	def energy ( self, v: float ): self._energy = v

	def get_stat ( self, stat: str ): return self.base_stats[stat] * self.level

	def get_stats ( self ):
		return { stat.replace('max_', ''): value * self.level for stat, value in {stat: value for stat, value in self.base_stats.items() if stat != 'element'}.items() }

	def get_battle_infos ( self ):
		return (
			( self.health, self.get_stat('max_health') ),
			( self.energy, self.get_stat('max_energy') ),
			( self.initiative, 100 )
		)

	def get_attack_amount ( self, attack: Attacks ):
		return self.get_stat('attack') * ATTACK_DATA[attack]['amount']
			
	def get_abilities ( self, all_of_them: bool = True ) -> list[Attacks]:
		if all_of_them: return [ ability for level, ability in self.abilities.items() if self.level >= level ]
		return [ ability for level, ability in self.abilities.items() if self.level >= level and self.energy > ATTACK_DATA[ability]['cost'] ]

	def increment_initiative ( self, dt: float ):
		self.initiative += self.get_stat('speed') * dt

	def take_damage ( self, amount: float ):
		defense = max( 0, min(1, 1 - self.get_stat('defense') / 2000) )
		self.health -= amount * defense

	def is_catchable ( self ): return self.health <= self.get_stat('max_health') * 0.1
		
