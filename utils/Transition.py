from typing import Callable, Literal

from gameobj.MonsterPatch import MonsterPatch
from settings import *
from gameobj.Sprite import Sprite
from entities.Player import Player
from utils.Timer import Timer
from utils.Types import TransitionState


class Transition:
	def __init__(self, player: Player, load_new_scene: Callable, callback: Callable | None = None) -> None:
		
		self.player = player
		self.load_new_scene = load_new_scene
		self.callback = callback

		self.canvas = pygame.display.get_surface()
		self.tint = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.transition_sprite = None
		self.transition_speed = 600
		self.transparency = 0

		self.state: TransitionState = 'standby'
		self.temp = None
		self.timer = Timer(500, self.__fade_to_light)


	def start ( self ): self.state = 'fade_to_black'
	
	def ongoing ( self ): return self.state != 'standby'

	def start_scene_transition ( self, sprite: Sprite ):
		if isinstance(sprite, MonsterPatch) and sprite.defeated: return
		self.transition_sprite = sprite
		self.player.block()
		self.start()

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
		self.state = 'fade_to_light' 
		self.transition_sprite = None 
		self.canvas.fill(0) 

	def __fade_to_light ( self, dt: float ):
		self.__set_transparency(dt, -1)
		self.__set_tint_alpha()
		self.__draw_new_fade()	
		self.__set_state_to_done()

	def __set_state_to_done ( self ):
		if self.transparency <= 0: self.state = 'done'

	def __finishing_touch ( self ):
		if self.callback: self.callback()
		self.player.unblock()
		self.state = 'standby'
	
	def update ( self, dt: float ):
		state_stalker('Transition states', self.state, self)
		if self.state == 'standby': return
		match self.state:
			case 'fade_to_black': self.__fade_to_black(dt)
			case 'load_scene': self.__load_new_scene()
			case 'fade_to_light': self.__fade_to_light(dt)
			case 'done': self.__finishing_touch()
