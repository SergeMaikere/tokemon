from settings import *
from entities.Entity import Entity
from pygame import Surface
from pygame.sprite import Group

class Player ( Entity ):
	def __init__(self, frames: dict[str, list[Surface]], pos: tuple[float, float], collisions: Group, *groups: Group) -> None:
		super().__init__(frames, pos, *groups)

		self.speed = 250

		self.collision_sprites = collisions

	def _set_direction ( self ):
		keys = pygame.key.get_pressed()
		self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
		self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
		self.direction = self.direction.normalize() if self.direction else self.direction

	def __update_y_order ( self ): self.y_order = self.rect.centery

	def __move_hitbox_x ( self, dt: float ): self.rect.x += self.direction.x * self.speed * dt
	def __move_hitbox_y ( self, dt: float ): self.rect.y += self.direction.y * self.speed * dt

	def __collision_handler_x ( self ):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.rect):
				if self.direction.x > 0: self.rect.right = sprite.rect.left
				if self.direction.x < 0: self.rect.left = sprite.rect.right

	def __collision_handler_y ( self ):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.rect):
				if self.direction.y > 0: self.rect.bottom = sprite.rect.top
				if self.direction.y < 0: self.rect.top = sprite.rect.bottom

	def _move ( self, dt: float ):
		self.__update_y_order()
		self.__move_hitbox_x(dt)
		self.__collision_handler_x()
		self.__move_hitbox_y(dt)
		self.__collision_handler_y()
