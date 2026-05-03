from typing import Callable, Literal

from settings import *
from entities.Player import Player
from utils.Helper import required
from utils.Timer import Timer
from utils.MapsLoader import MapsLoader
from utils.MyGroup import MyGroup
from utils.Types import TransitionState


class MapTransition:
	def __init__(self, player: Player, maps_loader: MapsLoader, get_player: Callable) -> None:
		
		self.player = player
		self.maps_loader = maps_loader
		self.get_player = get_player

		self.canvas = required(pygame.display.get_surface())
		self.tint = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.transition_sprite = None
		self.transition_speed = 600
		self.transparency = 0

		self.state: TransitionState = 'check_collision'
		self.timer = Timer(500, self.__fade_to_light)


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
		self.__update_datas_after_map_loaded()

	def __update_datas_after_map_loaded ( self ):
		self.transition_sprite = None # reset transition_sprite so it is ready for next map transition
		self.state = 'fade_to_light' # set next state
		self.canvas.fill(0) # cleanse the display surface otherwise it shows ghosts of the old map

	def __fade_to_light ( self, dt: float ):
		self.__set_transparency(dt, -1)
		self.__set_tint_alpha()
		self.__draw_new_fade()	
		self.__set_state_to_done()

	def __set_state_to_done ( self ):
		if self.transparency <= 0: self.state = 'done'

	def __unblock_player ( self ):
		self.player.unblock()
		self.state = 'check_collision'
	
	def handle_transitions ( self, dt: float ):
		match self.state:
			case 'check_collision': self.__handle_collisions(self.maps_loader.transition_sprites)
			case 'fade_to_black': self.__fade_to_black(dt)
			case 'load_map': self.__load_new_map()
			case 'fade_to_light': self.__fade_to_light(dt)
			case 'done': self.__unblock_player()
			case _: raise ValueError('Incorrect value state for MapsTransition')
