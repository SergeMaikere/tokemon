from settings import *
from entities.Entity import Entity
from pygame import Surface
from utils.Helper import voyeur
from utils.MyGroup import MyGroup
from pygame.sprite import Group

class Player ( Entity ):
	def __init__(self, frames: dict[str, list[Surface]], pos: tuple[float, float], collision_sprites: MyGroup, *groups: MyGroup) -> None:
		super().__init__('player', frames, pos, *groups)

		self.collision_sprites = collision_sprites
		self.speed = 250
		self.is_noticed = False


	def __update_y_order ( self ): self.y_order = self.rect.centery

	def set_is_noticed ( self, noticed: bool ): self.is_noticed = noticed

	def _set_direction ( self ):
		keys = pygame.key.get_pressed()
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
		self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
		self.direction = self.direction.normalize() if self.direction else self.direction

	def __move_hitbox_x ( self, dt: float ): self.hitbox.centerx += self.direction.x * self.speed * dt
	def __move_hitbox_y ( self, dt: float ): self.hitbox.centery += self.direction.y * self.speed * dt
	
	def __collision_handler_x ( self ):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
				if self.direction.x < 0: self.hitbox.left = sprite.hitbox.right

	def __collision_handler_y ( self ):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
				if self.direction.y < 0: self.hitbox.top = sprite.hitbox.bottom
		
	def _move ( self, dt: float ):
		self.__update_y_order()
		self.__collision_handler_x()
		self.__move_hitbox_x(dt)
		self.__collision_handler_y()
		self.__move_hitbox_y(dt)
		self.rect.center = self.hitbox.center
