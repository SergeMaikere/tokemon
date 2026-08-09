from typing import Callable

from settings import *
from entities.Player import Player
from utils.MyGroup import MyGroup
from utils.Transition import Transition


class CollisionManager:
	def __init__( self, player: Player, load_scene: Callable, collision_sprites: MyGroup, transition_sprites: MyGroup ) -> None:
		self.player = player

		self.collision_sprites = collision_sprites
		self.transition_sprites = transition_sprites

		self.transition_map = Transition(self.player, load_scene)


	def __move_hitbox_x ( self, dt: float ): self.player.hitbox.centerx += self.player.direction.x * self.player.speed * dt
	def __move_hitbox_y ( self, dt: float ): self.player.hitbox.centery += self.player.direction.y * self.player.speed * dt
	
	def __collision_handler_x ( self ):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.player.hitbox):
				if self.player.direction.x > 0: self.player.hitbox.right = sprite.hitbox.left
				if self.player.direction.x < 0: self.player.hitbox.left = sprite.hitbox.right

	def __collision_handler_y ( self ):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.player.hitbox):
				if self.player.direction.y > 0: self.player.hitbox.bottom = sprite.hitbox.top
				if self.player.direction.y < 0: self.player.hitbox.top = sprite.hitbox.bottom
		
	def __player_collides ( self, dt: float ):
		self.__move_hitbox_x(dt)
		self.__collision_handler_x()
		self.__move_hitbox_y(dt)
		self.__collision_handler_y()

	def __check_for_collision_with_transition_sprite ( self, transition_sprites: MyGroup ):
		return next( (sprite for sprite in transition_sprites if sprite.rect.colliderect(self.player.hitbox)), None )

	def __check_or_do_transition ( self ):
		transition_sprite = self.__check_for_collision_with_transition_sprite(self.transition_sprites)
		if transition_sprite: 
			self.transition_map.start_scene_transition(transition_sprite)
			self.player.block()


	def __player_changes_map ( self, dt: float ):
		if self.transition_map.state == 'standby': return self.__check_or_do_transition()
		if self.transition_map.state != 'standby': return self.transition_map.update(dt)

	def __player_encounter_monster ( self ): 
		pass


	def update ( self, dt: float ):
		self.__player_collides(dt)
		self.__player_changes_map(dt)
		self.__player_encounter_monster()