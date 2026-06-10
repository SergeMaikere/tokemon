from functools import partial
from os.path import join
from random import choice
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
from utils.Helper import display_item, get_rect, required, get_group, compose, images_loader_dict, cut, start_timer, voyeur
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Timer import Timer
from utils.Types import Elements, FontTypes, Menu, MonsterNames, Trainers, BattleMode, Attacks

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

		self.timers = {
			'delayed death': Timer(900, func=self.__bury_monster),
			'delayed attack': Timer(900, func=self.__target_selector)
		}

		self.mode: BattleMode | None = None 
		self.current_monster: MonsterSprite | None = None 
		self.attack: Attacks | None = None 
		self.target: Trainers | None = None 
		self.targeted_monster: MonsterSprite | None = None 
		self.attack_list: AttackList | None = None 
		self.switch_list: SwitchList | None = None

		self.variables_none = [ 'mode', 'current_monster', 'attack', 'target', 'targeted_monster', 'attack_list', 'switch_list' ]

		self.attacker: Trainers = 'player'

		self.level_surface = pygame.Surface((60, 26))

		self.max_fighting_monsters = 3

		self.__initiate_battle()


	def __update_timers ( self ):
		for timer in self.timers.values(): timer.update()

	def __get_all_fighters_sprites ( self ): return self.player_battle_sprites.sprites() + self.opponent_battle_sprites.sprites()

	def __initiate_battle ( self ):
		for entity, monsters in self.monsters.items():
			self.__draw_trainer_monsters(entity, monsters)

	def __draw_trainer_monsters ( self, entity: Trainers, monsters: list[Monster] ):
		for i, monster in enumerate(monsters):
			if i < self.max_fighting_monsters: 
				compose(
					lambda i: self.__get_position(i, entity),
					lambda pos: self.__creates_battle_sprites(pos, entity, monster)
				)( i )



	def __creates_battle_sprites ( self, pos: Point, entity: Trainers, monster: Monster ):
		compose(
			partial(self.__create_monster_sprite, pos, entity),
			self.__display_monster_stats,
			lambda sprite: self.__create_monster_outline(sprite),
			self.__display_monster_name,
			self.__display_monster_level,
		)( monster )

	def __get_position ( self, i: int, entity: Trainers ):
		return { k: v for k, v in enumerate(BATTLE_POSITIONS['left' if entity == 'player' else 'right'].values()) }[i]

	def __create_monster_sprite ( self, pos: Point, entity: Trainers, monster: Monster ):
		return MonsterSprite(monster, entity, self.MM.monster_frames[monster.name], self.MM.monster_frames_outlines[monster.name], pos, self.__handle_attack, self.battle_sprites, self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites)

	def __create_monster_outline ( self, sprite: MonsterSprite ):
		MonsterSpriteOutline(sprite, self.battle_sprites)
		return sprite

	def __display_monster_name ( self, monster_sprite: MonsterSprite ):
		monster_name_sprite = MonsterNameSprite(monster_sprite, monster_sprite.rect, self.fonts['regular'], self.battle_sprites)
		return ( monster_sprite, monster_name_sprite )

	def __display_monster_level ( self, datas: tuple[MonsterSprite, MonsterNameSprite] ):
		monster_sprite, monster_name_sprite = datas
		return MonsterLevelSprite(monster_sprite, monster_name_sprite.rect, self.fonts['small'], self.battle_sprites)

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
			self.__opponent_play(sprite)

	def __give_me_sprites ( self ):
		sprites = self.__get_all_fighters_sprites()
		sprite = next( (sprite for sprite in sprites if sprite.monster.initiative >= 100), None )
		return ( sprites, sprite )

	def __freeze_all_monsters ( self, sprites: list[MonsterSprite] ): [ sprite.set_paused(True) for sprite in sprites ]

	def __unfreeze_all_monsters ( self ): 
		[ sprite.set_paused(False) for sprite in self.__get_all_fighters_sprites() ]

	def __update_datas ( self, sprite: MonsterSprite ): 
		sprite.monster.initiative = 0
		self.mode = 'general'
		self.attacker = 'player' if self.player_battle_sprites.has(sprite) else 'opponent'
		self.current_monster = sprite
		sprite.start_flash()
		return sprite

	def __opponent_play ( self, sprite: MonsterSprite ):
		if self.attacker == 'player': return
		self.__target_player_monster(sprite)
		start_timer(self.timers['delayed attack'])

	def __target_player_monster ( self, sprite: MonsterSprite ):
		self.target = 'player'
		self.targeted_monster = choice(self.player_battle_sprites.sprites())
		self.attack = choice(sprite.monster.get_abilities(False))
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
		if not self.current_monster or not self.mode or self.attacker == 'opponent': return

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
				case 'switch': self.__switch_selector()
				case _: return
		if keys[pygame.K_ESCAPE]:
			match self.mode:
				case 'switch': self.mode = 'general'
				case 'attack': self.mode = 'general'
				case 'target': self.mode = 'attack'
				case _: return

	def __get_limiter ( self ):
		match self.mode:
			case 'general': return len(BATTLE_CHOICES['full'])
			case 'attack': return len(required(self.current_monster).monster.get_abilities())
			case 'switch': return len(self.MM.monsters)
			case 'target': return self.max_fighting_monsters
			case _: return 0

	def __general_selector ( self ):
		match self.indexes['general']:
			case 0: self.mode = 'attack'
			case 1: self.__defend()
			case 2: self.mode = 'switch'
			case 3: return

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
		if not self.current_monster: return
		self.current_monster.index = 0
		self.current_monster.set_state('attack')

	def __handle_attack ( self ):
		self.__animate_attack()
		self.__update_health()
		self.__reset_variables_to_none()
		self.__unfreeze_all_monsters()
		self.__reinitialize_all_indexes()

	def __animate_attack ( self ):
		AttackAnimation(self.attack_frames[ATTACK_DATA[self.attack]['animation']], self.targeted_monster.rect.center, self.battle_sprites)

	def __update_health ( self ):
		elememt_datas = ( ATTACK_DATA[self.attack]['element'], self.targeted_monster.monster.base_stats['element'] )
		compose(
			lambda attack: self.targeted_monster.monster.get_attack_amount(attack),
			lambda amount: self.__halve(elememt_datas, amount),
			lambda amount: self.__double(elememt_datas, amount),
			self.targeted_monster.monster.take_damage
		)(self.attack)

	def __halve ( self, element_datas: tuple[Elements, Elements], amount: float ):
		attack, monster = element_datas
		if attack == 'fire' and monster == 'water' or \
		   attack == 'water' and monster == 'plant' or \
		   attack == 'plant' and monster == 'fire':
			return amount * 0.5
		return amount

	def __double ( self, element_datas: tuple[Elements, Elements], amount: float ):
		attack, monster = element_datas
		if attack == 'fire' and monster == 'plant' or \
		   attack == 'plant' and monster == 'water' or \
		   attack == 'water' and monster == 'fire':
			return amount * 2
		return amount


	def __reset_variables_to_none ( self ):
		for name in self.variables_none: setattr(self, name, None)

	def __switch_selector ( self ): 
		if not self.switch_list: return
		self.switch_list.select()
		
	def __hilghlight_target ( self ):
		if self.mode != 'target': return
		sprites = self.player_battle_sprites if self.target == 'player' else self.opponent_battle_sprites
		self.targeted_monster = sprites.sprites()[self.indexes['target']]

	def __check_death ( self ):
		if self.timers['delayed death'].running or \
		   all([sprite.monster.health > 0 for sprite in self.__get_all_fighters_sprites()]): 
			return
		self.__get_dead_monster().dead = True
		self.timers['delayed death'].start()

	def __get_dead_monster ( self ):
		return next( (sprite for sprite in self.__get_all_fighters_sprites() if sprite.monster.health <= 0) )

	def __bury_monster ( self ):
		dying = self.__get_dead_monster()
		if self.opponent_battle_sprites in dying.groups(): return self.__bury_the_opponent_monster(dying)
		return self.__bury_the_player_monster(dying)

	def __bury_the_opponent_monster ( self, dying: MonsterSprite ):
		compose(
			self.__add_opponent_monster,
			self.__remove_opponent_monster,
			lambda dying: dying.kill()
		)( dying )

	def __bury_the_player_monster ( self, dying: MonsterSprite ):
		if self.player_battle_sprites not in dying.groups(): return
		
	def __remove_opponent_monster ( self, dying: MonsterSprite ):
		self.monsters['opponent'] = [ monster for monster in self.monsters['opponent'] if monster != dying.monster ]
		return dying

	def __add_opponent_monster ( self, dying: MonsterSprite ):
		if len(self.monsters['opponent']) <= self.max_fighting_monsters: return dying
		monster = self.__get_next_opponent_monster()
		self.__creates_battle_sprites(dying.pos, 'opponent', monster)
		return dying

	def __get_next_opponent_monster ( self ):
		return required(next((monster for monster in self.monsters['opponent'] if monster not in [sprite.monster for sprite in self.opponent_battle_sprites.sprites()]), None))

	def __check_for_switch ( self ):
		if not self.switch_list or not self.switch_list.switched: return
		for sprite in self.player_battle_sprites.sprites(): sprite.kill()
		self.monsters['player'] = self.MM.get_monster_list()
		self.__draw_trainer_monsters('player', self.monsters['player'])
		self.switch_list.switched, self.mode = None, None
		self.__unfreeze_all_monsters()

	def update ( self, dt: float ):
		self.__input()
		self.__update_timers()
		self.__check_death()
		self.__draw_battle_ground()
		self.__check_for_switch()
		self.__get_initiative()
		self.__hilghlight_target()
		self.update_battle_sprites(dt)
		self.__display_menus()
