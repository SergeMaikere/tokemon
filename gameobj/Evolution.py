from typing import Callable

from pygame import Font

from settings import *
from utils.Helper import add_background_to_text, compose, display_item, get_rect, get_tinted_surface, tint, required
from utils.MonsterManager import MonsterManager as MM
from utils.Timer import Timer
from utils.Types import EvolutionSates, MonsterNames, Pos

class Evolution:
	def __init__( self, font: Font, monster_name: MonsterNames, evolution_name: MonsterNames, end_evolution: Callable ) -> None:
		self.current_surface = pygame.transform.scale2x(MM.monster_frames[monster_name]['idle'][0])
		self.evolution_surface = pygame.transform.scale2x(MM.monster_frames[evolution_name]['idle'][0])

		self.silhouete_surface = self.__set_silhouete_surface()
		self.mask_tint, self.tint_speed = 0, 80

		self.current_text_surface = self.__set_text_surface(font, f'{monster_name} is evolving!')
		self.evolution_text_surface = self.__set_text_surface(font, f'{monster_name} evolved into {evolution_name}!')

		self.canvas = required(pygame.display.get_surface())
		self.tinted_surface = get_tinted_surface()

		self.state = 'standby'

		self.timers = {
			'start delay': Timer(800, autostart=True, func=lambda: self.set_state('display_current')),
			'show evolution': Timer(1800, func=end_evolution)
		}

	def __set_silhouete_surface ( self ):
		surface = pygame.mask.from_surface(self.current_surface).to_surface()
		surface.set_colorkey('black')
		return surface

	def __set_text_surface ( self, font: Font, text: str ):
		return compose(
			lambda text: font.render(text, False, COLORS['black']),
			lambda surface: add_background_to_text(surface, 20)
		)( text )

	def set_state ( self, state: EvolutionSates ):
		self.state = state

	def __display_current ( self, pos: Pos ):
		return compose(
			lambda pos: get_rect(self.current_surface, center=pos),
			lambda datas: display_item(self.canvas, datas)
		)( (WINDOW_WIDTH/2, WINDOW_HEIGHT/2) )

	def __set_tint ( self, dt: float, rect: FRect ):
		self.mask_tint += self.tint_speed * dt
		self.silhouete_surface.set_alpha(int(self.mask_tint))
		return ( self.silhouete_surface, rect )

	def __display_silhouete ( self, dt: float, rect: FRect ):
		return compose(
			lambda rect: self.__set_tint(dt, rect),
			lambda datas: display_item(self.canvas, datas)
		)( rect )

	def __display_text ( self, rect: FRect ):
		return compose(
			lambda rect: get_rect(self.current_text_surface, midtop=rect.midbottom + vector2(0, 20)),
			lambda datas: display_item(self.canvas, datas)
		)( rect )

	def __handle_display_current ( self, dt: float ):
		compose(
			self.__display_current,
			lambda rect: self.__display_silhouete(dt, rect),
			self.__display_text
		)( (WINDOW_WIDTH/2, WINDOW_HEIGHT/2) )


	def update ( self, dt: float ):
		tint(self.canvas, self.tinted_surface)

		for timer in self.timers.values(): timer.update()

		match self.state:
			case 'display_current': self.__handle_display_current(dt)