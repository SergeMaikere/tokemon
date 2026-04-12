from typing import Callable
from settings import *
from gameobj.Sprite import Sprite
from entities.Player import Player
from utils.MapsLoader import MapsLoader
from utils.MyGroup import MyGroup


class MapTransition:
	def __init__(self, player: Player, maps_loader: MapsLoader, get_player: Callable) -> None:
		
		self.player = player
		self.maps_loader = maps_loader

		self.canvas = pygame.display.get_surface()
		self.tint = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.transition_speed = 600
		self.transparency = 0
		self.direction = 1


	def check_for_collision ( self, transition_sprites: MyGroup ):
		try:
			return next( sprite for sprite in transition_sprites if sprite.rect.colliderect(self.player.hitbox) )
		except:
			return None

	def fade_to_black ( self, dt: float, transition_sprite: Sprite ):
		if not transition_sprite: return

		self.__set_transparency(dt)
		self.__set_tint_alpha()
		self.__draw_new_fade()		
		return transition_sprite

	def __set_transparency ( self, dt: float ):
		self.transparency += self.transition_speed * dt * self.direction
		self.transparency = max(0, min(self.transparency, 255))

	def __set_tint_alpha ( self ): self.tint.set_alpha(int(self.transparency))

	def __draw_new_fade ( self ): self.canvas.blit(self.tint, (0,0))

	def charge_map ( self, transition_sprite: Sprite ):
		if not transition_sprite or self.transparency < 255: return
		self.__kill_all_sprites()
		self.maps_loader.setup(self.maps_loader.maps[transition_sprite.target])

	def __kill_all_sprites ( self ):
		for group in self.maps_loader.groups:
			group.empty()

