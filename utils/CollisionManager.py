from typing import Callable

from settings import *
from entities.Player import Player
from utils.BattleManager import BattleManager
from utils.MyGroup import MyGroup
from utils.Transition import Transition


class CollisionManager:
	def __init__( self, player: Player, load_map: Callable, battle_manager: BattleManager, transition_sprites: MyGroup, monster_patch_sprites: MyGroup ) -> None:
		self.player = player
		self.BM = battle_manager

		self.transition_sprites = transition_sprites
		self.monster_patch_sprites = monster_patch_sprites

		self.transition_map = Transition(self.player, load_map)
		self.transition_battle = Transition(self.player, self.BM.battle_monsters)


	def __check_transition ( self, transition_manager: Transition, collision_group: MyGroup ):
		transition_sprite = self.player.check_for_collision(collision_group)
		if transition_sprite: 
			transition_manager.start_scene_transition(transition_sprite)


	def __transition_triggered_by_collision ( self, transition_manager: Transition, collision_group: MyGroup, dt: float ):
		if transition_manager.state == 'standby': return self.__check_transition(transition_manager, collision_group)
		if transition_manager.state != 'standby': return transition_manager.update(dt)


	def update ( self, dt: float ):
		if self.BM.battle: return

		self.__transition_triggered_by_collision(self.transition_map, self.transition_sprites, dt)
		self.__transition_triggered_by_collision(self.transition_battle, self.monster_patch_sprites, dt)
