from settings import *
from typing import Callable

class Timer:
	def __init__( self, duration: int, func: Callable | None = None, autostart: bool = False, loop: bool = False ) -> None:
		
		self.duration = duration
		self.func = func
		self.loop = loop

		self.start_time = pygame.time.get_ticks()
		self.running = autostart


	def start ( self ):
		self.running = True
		self.start_time = pygame.time.get_ticks()

	def stop ( self ): 
		self.running = False
		if self.loop: self.start()

	def __is_time_up ( self ): return pygame.time.get_ticks() - self.start_time >= self.duration

	def update ( self ):
		if self.running and self.__is_time_up():
			if self.func: self.func()
			self.stop()
