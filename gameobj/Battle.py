from functools import partial
from pygame import Font, sprite
from pygame.sprite import Sprite

from settings import *
from entities.Monster import Monster
from gameobj.MonsterSpriteOutline import MonsterSpriteOutline
from gameobj.MonsterLevelSprite import MonsterLevelSprite
from gameobj.MonsterNameSprite import MonsterNameSprite
from gameobj.MonsterStatsSprite import MonsterStatsSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.Helper import display_item, get_rect, required, get_group, pipe
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Types import BatlleMode, FontTypes, Menu, MonsterNames, Trainers

class Battle:
	def __init__( self, battle_ground: Surface, monster_manager: MonsterManager, fonts: dict[FontTypes, Font], ui_images: dict[str, Surface], opponent_monsters: dict[int, tuple[MonsterNames, int]], *groups: MyGroup ) -> None:
		
		self.MM = monster_manager
		self.opponent_monsters = opponent_monsters
		self.fonts = fonts
		self.ui_images = ui_images
		self.battle_ground_surface = battle_ground
		self.battle_ground_rect = self.battle_ground_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
		
		self.battle_sprites = get_group(groups, 'battle_sprites')
		self.player_battle_sprites = get_group(groups, 'player_battle_sprites')
		self.opponent_battle_sprites = get_group(groups, 'opponent_battle_sprites')

		self.canvas = required(pygame.display.get_surface())

		self.monsters: dict[Trainers, list[Monster]] = { 
			'player': self.MM.get_player_battle_monsters(), 
			'opponent': self.MM.get_opponent_battle_monsters(self.opponent_monsters) 
		}

		self.indexes = {
			'general': 0,
			'monster': 0,
			'attack': 0,
			'switch': 0,
			'target': 0,
		}

		self.mode, self.current_monster = None, None	

		self.level_surface = pygame.Surface((60, 26))

		self.initiate_battle()


	def initiate_battle ( self ):
		for entity, monsters in self.monsters.items():
			for i, monster in enumerate(monsters):
				self.__creates_all_battle_sprites(i, entity, monster)

	def __creates_all_battle_sprites ( self, i: int, entity: Trainers, monster: Monster ):
		pipe(
			partial(self.__create_monster_sprite, i, entity),
			self.__display_monster_stats,
			self.__display_monster_name,
			self.__display_monster_level,
		)( monster )

	def __create_monster_sprite ( self, i: int, entity: Trainers, monster: Monster ):
		pos = { k: v for k, v in enumerate(BATTLE_POSITIONS['left' if entity == 'player' else 'right'].values()) }[i]
		return MonsterSprite(monster, entity, self.MM.monster_frames[monster.name], pos, self.battle_sprites, self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites)

	def __display_monster_name ( self, monster_sprite: MonsterSprite ):
		return MonsterNameSprite(monster_sprite.entity, monster_sprite.monster, monster_sprite.rect, self.fonts['regular'], self.battle_sprites)

	def __display_monster_level ( self, monster_name: MonsterNameSprite ):
		return MonsterLevelSprite(monster_name.entity, monster_name.monster, monster_name.rect, self.fonts['small'], self.battle_sprites)

	def __display_monster_stats ( self, monster_sprite: MonsterSprite ):
		MonsterStatsSprite(monster_sprite, self.fonts['small'], self.battle_sprites)
		return monster_sprite

	def update_battle_sprites ( self, dt: float ):
		self.battle_sprites.update(dt)
		self.battle_sprites.draw(self.current_monster)

	def __input ( self ):
		if not self.current_monster or not self.mode: return

		keys = pygame.key.get_just_pressed()
		limiter = self.__get_limiter()

		if keys[pygame.K_UP]: 
			self.indexes[self.mode] = (self.indexes[self.mode] - 1) % limiter
		if keys[pygame.K_DOWN]: 
			self.indexes[self.mode] = (self.indexes[self.mode] + 1) % limiter
		if keys[pygame.K_SPACE]:
			match self.mode:
				case 'general': self.__general_selector()
				case _: return

	def __get_limiter ( self ):
		match self.mode:
			case 'general': return len(BATTLE_CHOICES['full'])
			case _: return 0

	def __general_selector ( self ):
		match self.indexes['general']:
			case 0: 
				# self.mode = 'attack'
				print('attack')
			case 1: 
				self.current_monster, self.mode = None, None
				self.indexes['general'] = 0
				self.__unfreeze_all_monsters(self.player_battle_sprites.sprites() + self.opponent_battle_sprites.sprites())
				print('defend')
			case 2: 
				# self.mode = 'switch'
				print('switch')
			case 3: 
				# self.mode = 'monster'
				print('catch')

	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)

	def __get_initiative ( self ):
		if self.mode == 'general': return

		sprites, sprite = self.__give_me_sprites()
		if sprite:
			self.__freeze_all_monsters(sprites)
			self.__update_datas(sprite)
			self.__highlite_monster(sprite)

	def __give_me_sprites ( self ):
		sprites = self.player_battle_sprites.sprites() + self.opponent_battle_sprites.sprites()
		sprite = next( (sprite for sprite in sprites if sprite.monster.initiative >= 100), None )
		return ( sprites, sprite )

	def __freeze_all_monsters ( self, sprites: list[MonsterSprite] ): [ sprite.set_paused(True) for sprite in sprites ]

	def __unfreeze_all_monsters ( self, sprites: list[MonsterSprite] ): [ sprite.set_paused(False) for sprite in sprites ]

	def __update_datas ( self, sprite: MonsterSprite ): 
		self.mode = 'general'
		self.current_monster = sprite
		sprite.monster.initiative = 0
		sprite.start_flash()
		return sprite

	def __highlite_monster ( self, sprite: MonsterSprite ):
		MonsterSpriteOutline(sprite, self.MM.monster_frames_outlines[sprite.monster.name], self.battle_sprites)
		return sprite

	def __display_menus ( self ):
		match self.mode:
			case 'general': self.__display_general()
			case _: return

	def __display_general ( self ):
		for i, (key, data) in enumerate(BATTLE_CHOICES['full'].items()):
			pipe(
				partial(self.__get_general_menu_icon, i),
				partial(self.__set_grayscale_transformation, i),
				partial(get_rect, center=(required(self.current_monster).rect.center) + data['pos']),
				partial(display_item, self.canvas)
			)(data)
			
	def __get_general_menu_icon ( self, i: int, data: Menu ):
		return self.ui_images[f'{data['icon']}_highlight' if self.__is_selected(i) else data['icon']]

	def __set_grayscale_transformation ( self, i: int, icon: Surface ):
		if self.__is_selected(i): return icon 
		return pygame.transform.grayscale(icon)

	def __is_selected ( self, i: int ): return i == self.indexes[required(self.mode)]

	def update ( self, dt: float ):
		self.__input()
		self.__draw_battle_ground()
		self.update_battle_sprites(dt)
		self.__get_initiative()
		self.__display_menus()
