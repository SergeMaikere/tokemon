from typing import Callable

from pygame import Font

from settings import *
from entities.Player import Player
from gameobj.Evolution import Evolution
from utils.Helper import set_none
from utils.MyGroup import MyGroup
from utils.MonsterManager import MonsterManager as MM

class EvolutionManager:
	def __init__( self, player: Player, font: Font, player_monsters_sprites: MyGroup ) -> None:
		self.player = player
		self.font = font
		self.player_monsters_sprites = player_monsters_sprites

		self.evolution = None


	def __check_for_evolution ( self ):
		return next( (monster for monster in MM.monsters.values() if monster.level == monster.evolve[1]), None )

	def __end_evolution ( self ):
		set_none(self, 'evolution')
		self.player.unblock()

	def handle_evolution ( self ):
		monster = self.__check_for_evolution()
		voyeur(f'Evolution Manager check for evolution => {monster}')
		if monster:
			self.player.block()
			self.evolution = Evolution(self.font, monster.name, monster.evolve[0], self.__end_evolution)
	
	def update ( self, dt: float ):
		if not self.evolution: return
		self.evolution.update(dt)