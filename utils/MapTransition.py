from typing import Callable, Literal

from settings import *
from entities.Player import Player
from utils.MapsLoader import MapsLoader
from utils.MyGroup import MyGroup


class MapTransition:
	def __init__(self, player: Player, maps_loader: MapsLoader, get_player: Callable) -> None:
		
		self.player = player
		self.maps_loader = maps_loader
		self.get_player = get_player

		self.canvas = pygame.display.get_surface()
		self.tint = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.transition_sprite = None
		self.transition_speed = 600
		self.transparency = 0

		self.state = 'search'


	def __handle_collisions ( self, transition_sprites: MyGroup ):
		self.transition_sprite = self.__check_for_collision(transition_sprites)
		if self.transition_sprite: 
			self.state = 'fade_to_black'
			self.player.block()

	def __check_for_collision ( self, transition_sprites: MyGroup ):
		return next( (sprite for sprite in transition_sprites if sprite.rect.colliderect(self.player.hitbox)), None )

	def __fade_to_black ( self, dt: float ):
		self.__set_transparency(dt, 1)
		self.__set_tint_alpha()
		self.__draw_new_fade()	
		self.__set_state_to_load()	

	def __set_transparency ( self, dt: float, direction: Literal[1, -1] ):
		self.transparency += self.transition_speed * dt * direction
		self.transparency = max(0, min(self.transparency, 255))

	def __set_tint_alpha ( self ): self.tint.set_alpha(round(self.transparency))

	def __draw_new_fade ( self ): self.canvas.blit(self.tint, (0,0))

	def __set_state_to_load ( self ): 
		if self.transparency >= 255: self.state = 'load_map'

	def __load_new_map ( self ):
		if not self.transition_sprite: return
		self.maps_loader.transition_setup(self.maps_loader.maps[self.transition_sprite.target], self.transition_sprite.pos)
		self.transition_sprite = None
		self.state = 'fade_to_light'

	def __fade_to_light ( self, dt: float ):
		self.__set_transparency(dt, -1)
		self.__set_tint_alpha()
		self.__draw_new_fade()	
		self.__set_state_to_done()

	def __set_state_to_done ( self ):
		if self.transparency <= 0: self.state = 'done'

	def __unblock_player ( self ):
		self.player.unblock()
		self.state = 'search'

	# def handle_transitions ( self, dt: float ):
	# 	self.__handle_collisions(self.maps_loader.transition_sprites)
	# 	self.__fade_to_black(dt)
	# 	self.__load_new_map()
	# 	self.__fade_to_light(dt)
	
	def handle_transitions ( self, dt: float ):
		match self.state:
			case 'fade_to_black': return self.__fade_to_black(dt)
			case 'load_map': return self.__load_new_map()
			case 'fade_to_light': return self.__fade_to_light(dt)
			case 'done': return self.__unblock_player()
			case 'search': return self.__handle_collisions(self.maps_loader.transition_sprites)
			case _: raise ValueError('Incorrect state for MapsTransition')
