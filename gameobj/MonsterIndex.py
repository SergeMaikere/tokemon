from functools import partial
from pygame import Font
from pygame.key import ScancodeWrapper
from pygame.typing import Point

from settings import *
from entities.Monster import Monster
from entities.Player import Player
from gameobj.SideList import SideList
from utils.Helper import get_progress_bar, required, pipe
from utils.MonsterManager import MonsterManager
from utils.Types import FontTypes

class MonsterIndex:
	def __init__( self, player: Player, monster_manager: MonsterManager, fonts: dict[str, Font ] ) -> None:
		
		self.player = player
		self.fonts = fonts

		self.MM = monster_manager

		self.canvas: Surface = required(pygame.display.get_surface())
		self.tint_surface = self.__get_tinted_surface()

		self.main_rect = pygame.FRect(0, 0, self.canvas.width * 0.6, self.canvas.height * 0.8).move_to(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.side_list = SideList(self.MM.monsters, self.fonts['regular'], self.main_rect, 6, self.MM.monsters_icons)

		self.top_rect = pygame.FRect(self.main_rect.left + self.side_list.card_width, self.main_rect.top, self.main_rect.width - self.side_list.card_width, self.main_rect.height * 0.4)

		self.health_bar_rect, self.energy_bar_rect = self.__get_progress_bar_rects()

		self.stats_rect = pygame.FRect(self.health_bar_rect.left, self.health_bar_rect.bottom, self.health_bar_rect.width, self.main_rect.bottom - self.health_bar_rect.bottom).inflate(0, -60)

		self.animation_index = 0

		self.open = False

	def __get_progress_bar_rects ( self ):
		health_bar_rect = pygame.FRect((0, 0), (self.top_rect.width * 0.45, 30)).move_to(midtop=(self.top_rect.left + self.top_rect.width/4, self.top_rect.bottom + 10))
		energy_bar_rect = pygame.FRect((0, 0), (self.top_rect.width * 0.45, 30)).move_to(midtop=(self.top_rect.right - self.top_rect.width/4, self.top_rect.bottom + 10))
		return (health_bar_rect, energy_bar_rect)


	def __get_tinted_surface ( self ):
		tint_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		tint_surface.set_alpha(200)
		return tint_surface

	def __input ( self ):
		keys = pygame.key.get_just_pressed()
		self.__display_monster_index(keys)
		self.__up_and_down(keys)
		self.__select(keys)

	def __display_monster_index ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_RETURN]:
			self.player.is_mobile = not self.player.is_mobile
			self.open = not self.open

	def __up_and_down ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_UP]: self.side_list.index -= 1
		if keys[pygame.K_DOWN]: self.side_list.index += 1
		self.side_list.index = self.side_list.index % len(self.MM.monsters)

	def __select ( self, keys: ScancodeWrapper ):
		if keys[pygame.K_SPACE]: self.side_list.select()

	def __draw_main_rect ( self ):
		pygame.draw.rect(self.canvas, COLORS['gray'], self.main_rect)

	def __draw_side_list_shadow ( self ):
		shadow_surface = pygame.Surface((4, self.main_rect.height))
		self.canvas.blit( shadow_surface, (self.main_rect.left + self.side_list.card_width, self.main_rect.top) )
	
	def __tint ( self ): self.canvas.blit(self.tint_surface, (0, 0))

	
	def __draw_top_rect ( self, monster: Monster ):
		pygame.draw.rect(self.canvas, COLORS[monster.element], self.top_rect, 0, 0, 0, 12)
		return monster

	def __display_monster ( self, dt: float, monster: Monster ):
		image = self.__get_monster_frames(dt, monster)
		rect = image.get_frect(center=self.top_rect.center)
		self.canvas.blit(image, rect)
		return monster

	def __get_monster_frames (self, dt: float, monster: Monster ):
		frames = self.MM.monster_frames[monster.name]['idle']
		self.animation_index += ANIMATION_SPEED * dt
		return frames[int(self.animation_index) % len(frames)]


	def __set_text ( self, font_type: FontTypes, text: str, **position: Point ):
		text_surface = self.fonts[font_type].render(text, False, COLORS['white'])
		text_rect = text_surface.get_frect(**position)
		self.canvas.blit(text_surface, text_rect)
		return (text_surface, text_rect)

	def __display_monster_level ( self, monster: Monster ):
		_, rect = self.__set_text( 'regular', f'Lvl: {monster.level}', bottomleft=self.top_rect.bottomleft + vector2(10, -16) )
		get_progress_bar(
			surface=self.canvas,
			rect=pygame.FRect(rect.bottomleft, (100, 4)),
			bg_color=COLORS['dark'],
			color=COLORS['white'],
			value=monster.xp,
			value_max=monster.level_up
		)
		return monster

	def __display_monster_name ( self, monster: Monster ):
		self.__set_text( 'bold', monster.name, topleft=self.top_rect.topleft + vector2(10, 10) )
		return monster

	def __display_monster_element ( self, monster: Monster ):
		self.__set_text('regular', monster.element, bottomright=self.top_rect.bottomright + vector2(-10, -10))
		return monster


	def __display_top ( self, dt: float, monster: Monster ):
		return pipe(
			self.__draw_top_rect,
			partial(self.__display_monster, dt),
			self.__display_monster_name,
			self.__display_monster_level,
			self.__display_monster_element,
		)(monster)
		
	def __display_progress_bars ( self, monster: Monster ):

		health_rect, _ = get_progress_bar(
			surface=self.canvas, 
			rect=self.health_bar_rect,
			bg_color=COLORS['black'],
			color=COLORS['red'],
			value=monster.health,
			value_max=monster.get_stat('max_health'),
			radius=2
		)

		energy_rect, _ = get_progress_bar(
			surface=self.canvas,
			rect=self.energy_bar_rect,
			bg_color=COLORS['gray'],
			color=COLORS['blue'],
			value=monster.energy,
			value_max=monster.get_stat('max_energy'),
			radius=2
		)

		self.__set_text('regular', f'Hp: {int(monster.health)}/{monster.get_stat('max_health')}', midleft=health_rect.midleft + vector2(10, 0))
		self.__set_text('regular', f'Ep: {int(monster.energy)}/{monster.get_stat('max_energy')}', midleft=energy_rect.midleft + vector2(10, 0))

		return monster
		

	def __display_stats ( self, monster: Monster ):
		self.__set_text('regular', 'Stats', bottomleft=self.stats_rect.topleft)[1].inflate(0, -10)
		
		stats = monster.get_stats()
		for i, (stat, value) in enumerate(stats.items()):
			_, text_rect = self.__set_text('regular', stat, topleft=(self.stats_rect.left + 10, self.stats_rect.top + i * self.stats_rect.height/len(stats)))

			get_progress_bar(
				surface=self.canvas,
				rect=pygame.FRect(text_rect.left, text_rect.bottom + 10, self.stats_rect.width * 0.75, 4),
				bg_color=COLORS['black'],
				color=COLORS['white'],
				value=value,
				value_max=self.MM.monsters_max_stats[stat] * monster.level,
			)

		return monster


	def __display ( self, dt: float ):
		if not self.open: return
		self.__tint()
		self.__draw_main_rect()
		self.side_list.display()

		pipe(
			partial(self.__display_top, dt),
			self.__display_progress_bars,
			self.__display_stats,
		)(self.MM.monsters[self.side_list.index])

		self.__draw_side_list_shadow()

	def update ( self, dt: float ):
		self.__input()
		self.__display(dt)		