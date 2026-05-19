from functools import partial
from os.path import join
from pygame import Font

from assets.data.game_data import ATTACK_DATA
from gameobj.AttackAnimation import AttackAnimation
from gameobj.AttackList import AttackList
from gameobj.MyList import MyList
from gameobj.SwitchList import SwitchList
from settings import *
from entities.Monster import Monster
from gameobj.MonsterSpriteOutline import MonsterSpriteOutline
from gameobj.MonsterLevelSprite import MonsterLevelSprite
from gameobj.MonsterNameSprite import MonsterNameSprite
from gameobj.MonsterStatsSprite import MonsterStatsSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.Helper import display_item, get_rect, required, get_group, compose, images_loader_dict, cut
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Types import FontTypes, Menu, MonsterNames, Trainers, BattleMode, Attacks

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

		self.attack_frames = compose(
			images_loader_dict,
			lambda frames: { attack: [cut(image, 0, col, image.width/4, image.height) for col in range(4)] for attack, image in frames.items() }
		)( join('assets', 'graphics', 'attacks') )

		self.indexes = {
			'general': 0,
			'monster': 0,
			'attack': 0,
			'switch': 0,
			'target': 0,
		}

		self.mode: BattleMode | None = None 
		self.current_monster: MonsterSprite | None = None 
		self.attack: Attacks | None = None 
		self.target: Trainers | None = None 
		self.targeted_monster: MonsterSprite | None = None 
		self.attack_list: MyList | None = None 
		self.switch_list: MyList | None = None

		self.attacker: Trainers = 'player'

		self.level_surface = pygame.Surface((60, 26))

		self.initiate_battle()


	def initiate_battle ( self ):
		for entity, monsters in self.monsters.items():
			for i, monster in enumerate(monsters):
				self.__creates_all_battle_sprites(i, entity, monster)

	def __creates_all_battle_sprites ( self, i: int, entity: Trainers, monster: Monster ):
		compose(
			partial(self.__create_monster_sprite, i, entity),
			self.__display_monster_stats,
			lambda sprite: self.__create_monster_outline(sprite),
			self.__display_monster_name,
			self.__display_monster_level,
		)( monster )

	def __create_monster_sprite ( self, i: int, entity: Trainers, monster: Monster ):
		pos = { k: v for k, v in enumerate(BATTLE_POSITIONS['left' if entity == 'player' else 'right'].values()) }[i]
		return MonsterSprite(monster, entity, self.MM.monster_frames[monster.name], self.MM.monster_frames_outlines[monster.name], pos, self.battle_sprites, self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites)

	def __create_monster_outline ( self, sprite: MonsterSprite ):
		MonsterSpriteOutline(sprite, self.battle_sprites)
		return sprite

	def __display_monster_name ( self, monster_sprite: MonsterSprite ):
		return MonsterNameSprite(monster_sprite.entity, monster_sprite.monster, monster_sprite.rect, self.fonts['regular'], self.battle_sprites)

	def __display_monster_level ( self, monster_name: MonsterNameSprite ):
		return MonsterLevelSprite(monster_name.entity, monster_name.monster, monster_name.rect, self.fonts['small'], self.battle_sprites)

	def __display_monster_stats ( self, monster_sprite: MonsterSprite ):
		MonsterStatsSprite(monster_sprite, self.fonts['small'], self.battle_sprites)
		return monster_sprite

	def update_battle_sprites ( self, dt: float ):
		self.battle_sprites.update(dt)
		self.battle_sprites.draw_all(self.current_monster, self.targeted_monster, self.is_player_targeted)

	def __reinitialize_all_indexes ( self ): self.indexes = { mode: 0 for mode in self.indexes.keys() }

	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)

	def __get_initiative ( self ):
		if self.mode: return

		sprites, sprite = self.__give_me_sprites()
		if sprite:
			self.__freeze_all_monsters(sprites)
			self.__update_datas(sprite)

	def __give_me_sprites ( self ):
		sprites = self.player_battle_sprites.sprites() + self.opponent_battle_sprites.sprites()
		sprite = next( (sprite for sprite in sprites if sprite.monster.initiative >= 100), None )
		return ( sprites, sprite )

	def __freeze_all_monsters ( self, sprites: list[MonsterSprite] ): [ sprite.set_paused(True) for sprite in sprites ]

	def __unfreeze_all_monsters ( self ): 
		[ sprite.set_paused(False) for sprite in self.player_battle_sprites.sprites() + self.opponent_battle_sprites.sprites() ]

	def __update_datas ( self, sprite: MonsterSprite ): 
		sprite.monster.initiative = 0
		self.mode = 'general'
		self.attacker = 'player' if self.player_battle_sprites.has(sprite) else 'opponent'
		self.current_monster = sprite
		sprite.start_flash()
		return sprite


	def __display_menus ( self ):
		if self.attacker == 'opponent': return
		match self.mode:
			case 'general': self.__display_general()
			case 'attack': self.__display_attack()
			case 'switch': self.__display_switch()
			case _: return

	def __display_general ( self ):
		for i, (_, data) in enumerate(BATTLE_CHOICES['full'].items()):
			compose(
				partial(self.__get_general_menu_icon, i),
				partial(self.__set_grayscale_transformation, i),
				partial(get_rect, center=(required(self.current_monster).rect.center) + data['pos']),
				partial(display_item, self.canvas)
			)(data)
	
	def __display_attack ( self ):
		if self.attack_list:
			self.attack_list.update()
		else:
			self.attack_list = AttackList( 
			my_list=required(self.current_monster).monster.get_abilities(all_of_them=False), 
			font=self.fonts['regular'],
			pos=required(self.current_monster).rect.midright, 
			get_index=lambda: self.indexes['attack']
		)

	def __display_switch ( self ):
		if self.switch_list:
			self.switch_list.update()
		else:
			self.switch_list = SwitchList(
				monster_manager=self.MM,
				font=self.fonts['regular'],
				pos=required(self.current_monster).rect.midright,
				get_index=lambda: self.indexes['switch']
			)


	def __get_general_menu_icon ( self, i: int, data: Menu ):
		return self.ui_images[f'{data['icon']}_highlight' if self.__is_selected(i) else data['icon']]

	def __set_grayscale_transformation ( self, i: int, icon: Surface ):
		if self.__is_selected(i): return icon 
		return pygame.transform.grayscale(icon)

	def __is_selected ( self, i: int ): return i == self.indexes[required(self.mode)]

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
				case 'attack': self.__attack_selector()
				case 'target': self.__target_selector()
				case _: return

	def __get_limiter ( self ):
		match self.mode:
			case 'general': return len(BATTLE_CHOICES['full'])
			case 'attack': return len(required(self.current_monster).monster.get_abilities())
			case 'switch': return len(self.MM.monsters)
			case 'target': return len(self.monsters['player' if self.target == 'player' else 'opponent'])
			case _: return 0

	def __general_selector ( self ):
		match self.indexes['general']:
			case 0: 
				self.mode = 'attack'
				print('attack')
			case 1: 
				self.__defend()
				print('defend')
			case 2: 
				self.mode = 'switch'
				print('switch')
			case 3: 
				# self.mode = 'monster'
				print('catch')

	def __defend ( self ):
		self.current_monster, self.mode = None, None
		self.indexes['general'] = 0
		self.__unfreeze_all_monsters()

	def __attack_selector ( self ):
		self.mode = 'target'
		self.attack = required(self.current_monster).monster.get_abilities(all_of_them=False)[self.indexes['attack']]
		self.target = ATTACK_DATA[self.attack]['target']
		print(self.attack)

	def is_player_targeted ( self ): return self.mode == 'target' and self.target == 'player'

	def __target_selector ( self ):
		AttackAnimation(self.attack_frames[self.attack], self.targeted_monster.rect.center, self.battle_sprites)
		self.mode, self.current_monster, self.targeted_monster, self.attack, self.target = None, None, None, None, None
		self.__unfreeze_all_monsters()
		self.__reinitialize_all_indexes()

	def __hilghlight_target ( self ):
		if self.mode != 'target': return
		sprites = self.player_battle_sprites if self.target == 'player' else self.opponent_battle_sprites
		self.targeted_monster = sprites.sprites()[self.indexes['target']]

	def update ( self, dt: float ):
		self.__input()
		self.__draw_battle_ground()
		self.__get_initiative()
		self.__hilghlight_target()
		self.update_battle_sprites(dt)
		self.__display_menus()
