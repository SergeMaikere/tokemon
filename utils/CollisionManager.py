from settings import *
from entities.Player import Player
from utils.MyGroup import MyGroup


class CollisionManager:
	def __init__( self, player: Player, collision_sprites: MyGroup ) -> None:
		self.player = player

		self.collision_sprites = collision_sprites


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

	def __player_changes_map ( self ): 
		pass

	def __player_encounter_monster ( self ): 
		pass


	def update ( self, dt: float ):
		self.__player_collides(dt)
		self.__player_changes_map()
		self.__player_encounter_monster()