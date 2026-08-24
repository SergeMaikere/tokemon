from typing import Callable, Literal

from gameobj.MonsterPatch import MonsterPatch
from settings import *
from gameobj.Sprite import Sprite
from entities.Player import Player
from utils.Helper import required
from utils.Timer import Timer
from utils.Types import TransitionState


class Transition:
	def __init__(self, player: Player, load_new_scene: Callable) -> None:
		
		self.player = player
		self.load_new_scene = load_new_scene

		self.canvas = required(pygame.display.get_surface())
		self.tint = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.transition_sprite = None
		self.transition_speed = 600
		self.transparency = 0

		self.state: TransitionState = 'standby'
		self.timer = Timer(500, self.__fade_to_light)


	def start_scene_transition ( self, sprite: Sprite ):
		if isinstance(sprite, MonsterPatch) and sprite.defeated: return
		self.transition_sprite = sprite
		self.state = 'fade_to_black'

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
		if self.transparency >= 255: self.state = 'load_scene'
	
	def __load_new_scene ( self ):
		self.load_new_scene(self.transition_sprite)
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
		self.state = 'standby'
	
	def update ( self, dt: float ):
		if self.state == 'standby': return
		match self.state:
			case 'fade_to_black': self.__fade_to_black(dt)
			case 'load_scene': self.__load_new_scene()
			case 'fade_to_light': self.__fade_to_light(dt)
			case 'done': self.__unblock_player()
