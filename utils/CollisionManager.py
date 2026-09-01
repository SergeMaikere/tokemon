from random import randint
from typing import Callable

from settings import *
from entities.Player import Player
from utils.BattleManager import BattleManager
from utils.MyGroup import MyGroup
from utils.Timer import Timer
from utils.Transition import Transition


class CollisionManager:
	def __init__( self, player: Player, load_map: Callable, battle_manager: BattleManager, transition_sprites: MyGroup, monster_patch_sprites: MyGroup ) -> None:
		self.player = player
		self.BM = battle_manager

		self.transition_sprites = transition_sprites
		self.monster_patch_sprites = monster_patch_sprites

		self.transition_map = Transition(self.player, load_map)
		self.transition_battle = Transition(self.player, self.BM.battle_monsters)

		self.timer = Timer(2500, func=self.__start_transition_battle)


	def __check_transition_map ( self ):
		transition_sprite = self.player.check_for_collision(self.transition_sprites)
		if transition_sprite: 
			self.transition_map.start_scene_transition(transition_sprite)


	def __if_walking_in_monster_patchs ( self, action: Callable ):
		monster_patch_sprite = self.player.check_collision_and_movement(self.monster_patch_sprites)
		if monster_patch_sprite: return action(monster_patch_sprite)

	def __start_timer ( self, _ ):
		self.timer.duration = randint(800, 2500)
		self.timer.start()

	def __check_transition_battle ( self ):
		return self.__if_walking_in_monster_patchs(self.__start_timer)

	def __transition_manager ( self, transition: Transition, transition_checker: Callable, dt: float ):
		if transition.state == 'standby': return transition_checker()
		if transition.state != 'standby': return transition.update(dt)

	def __start_transition_battle ( self ):
		return self.__if_walking_in_monster_patchs(self.transition_battle.start_scene_transition)

	def update ( self, dt: float ):
		if self.BM.battle: return

		self.__transition_manager(self.transition_map, self.__check_transition_map, dt)
		
		if self.timer.running:
			self.timer.update()
		else:
			self.__transition_manager(self.transition_battle, self.__check_transition_battle, dt)