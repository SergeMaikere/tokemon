from functools import partial
from pygame import FRect, Font
from pygame.key import ScancodeWrapper
from pygame.typing import Point

from settings import *
from entities.Monster import Monster
from entities.Player import Player
from gameobj.AnimatedSprite import AnimatedSprite
from gameobj.SideList import SideList
from utils.Helper import required
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Types import FontTypes

class MonsterIndex:
	def __init__( self, player: Player, monster_manager: MonsterManager, fonts: dict[str, Font ], all_sprites: MyGroup ) -> None:
		
		self.player = player
		self.fonts = fonts
		self.all_sprites = all_sprites

		self.MM = monster_manager

		self.canvas = required(pygame.display.get_surface())
		self.tint_surface = self.__get_tinted_surface()

		self.main_rect = pygame.FRect(0, 0, self.canvas.width * 0.6, self.canvas.height * 0.8).move_to(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.side_list = SideList(self.MM.monsters, self.fonts['regular'], self.main_rect, 6, self.MM.monsters_icons)

		self.top_rect = pygame.FRect(self.main_rect.left + self.side_list.card_width, self.main_rect.top, self.main_rect.width - self.side_list.card_width, self.main_rect.height * 0.4)
		self.animation_index = 0

		self.open = False

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
		pygame.draw.rect(self.canvas, COLORS['light-gray'], self.main_rect)

	def __draw_side_list_shadow ( self ):
		shadow_surface = pygame.Surface((4, self.main_rect.height))
		self.canvas.blit( shadow_surface, (self.main_rect.left + self.side_list.card_width, self.main_rect.top) )
	
	def __tint ( self ): self.canvas.blit(self.tint_surface, (0, 0))

	
	def __draw_top_rect ( self, monster: Monster ):
		pygame.draw.rect(self.canvas, COLORS[monster.element], self.top_rect, 0, 0, 0, 12)
		return monster

	def __display_monster ( self, dt: float, monster: Monster ):
		image = self.__get_frame(dt, monster)
		rect = image.get_frect(center=self.top_rect.center)
		self.canvas.blit(image, rect)

	def __get_frame (self, dt: float, monster: Monster ):
		frames = self.MM.monster_frames[monster.name]['idle']
		self.animation_index += ANIMATION_SPEED * dt
		return frames[int(self.animation_index) % len(frames)]


	def __set_text ( self, font_type: FontTypes, text: str, **position: Point ):
		text_surface = self.fonts[font_type].render(text, False, COLORS['white'])
		text_rect = text_surface.get_frect(**position)
		self.canvas.blit(text_surface, text_rect)


	def __display_top ( self, dt: float ):
		monster = self.MM.monsters[self.side_list.index]
		self.__draw_top_rect(monster)
		# self.__display_monster(dt, monster)
		self.__set_text( 'bold', monster.name, topleft=self.top_rect.topleft + vector2(10, 10) )
		self.__set_text( 'regular', f'Lvl: {monster.level}', bottomleft=self.top_rect.bottomleft + vector2(10, -10) )
		self.__set_text('regular', monster.element, bottomright=self.top_rect.bottomright + vector2(-10, -10))
		

	def __display ( self, dt: float ):
		if not self.open: return
		self.__tint()
		# self.__draw_main_rect()
		self.side_list.display()
		self.__draw_side_list_shadow()
		self.__display_top(dt)

	def update ( self, dt: float ):
		self.__input()
		self.__display(dt)		