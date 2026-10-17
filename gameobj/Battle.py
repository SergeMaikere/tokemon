from functools import partial
from os.path import join
from random import choice
from typing import Literal, TypeAlias, cast
from pygame import Font

from settings import *
from assets.data.game_data import ATTACK_DATA
from entities.Monster import Monster
from gameobj.AttackAnimation import AttackAnimation
from gameobj.AttackList import AttackList
from gameobj.SwitchList import SwitchList
from gameobj.TimedSprite import TimedSprite
from gameobj.MonsterSpriteOutline import MonsterSpriteOutline
from gameobj.MonsterLevelSprite import MonsterLevelSprite
from gameobj.MonsterNameSprite import MonsterNameSprite
from gameobj.MonsterStatsSprite import MonsterStatsSprite
from gameobj.MonsterSprite import MonsterSprite
from utils.Helper import display_item, get_rect, kill_sprite, required, get_group, compose, images_loader_dict, cut, set_falsy, set_truthy, start_timer
from utils.MonsterManager import MonsterManager as MM
from utils.MusicManager import MusicManager
from utils.MyGroup import MyGroup
from utils.Timer import Timer
from utils.Types import Elements, FontTypes, LazyDict, Menu, MonsterNames, Pos, Trainers, BattleMode, Attacks


Monsters: TypeAlias = dict[ int, Monster ]

class Battle:
	def __init__( self, battle_ground: Surface, fonts: dict[FontTypes, Font], ui_images: dict[str, Surface], opponent_monsters: dict[int, tuple[MonsterNames, int]], *groups: MyGroup ) -> None:
		
		self.fonts = fonts
		self.ui_images = ui_images
		self.battle_ground_surface = battle_ground
		self.battle_ground_rect = self.battle_ground_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
		
		self.battle_sprites = get_group(groups, 'battle_sprites')
		self.player_battle_sprites = get_group(groups, 'player_battle_sprites')
		self.opponent_battle_sprites = get_group(groups, 'opponent_battle_sprites')

		self.canvas = required(pygame.display.get_surface())

		self.monsters = LazyDict[Monsters](
			{ 
				'player': lambda: MM.get('monsters'), 
				'opponent': MM.get_opponent_battle_monsters(opponent_monsters) 
			}
		)

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

		self.catch, self.victory, self.defeat = False, False, False

		self.variables_none = [ 'mode', 'current_monster', 'attack', 'target', 'targeted_monster', 'attack_list', 'switch_list' ]

		self.level_surface = pygame.Surface((60, 26))

		self.max_fighting_monsters = 3

		self.__initiate_battle()


	
	
	# DISPLAY MONSTERS

	def __initiate_battle ( self ):
		for entity in self.monsters:
			monsters = self.monsters[entity]
			self.__draw_trainer_monsters(cast(Trainers, entity), monsters)

	def __draw_trainer_monsters ( self, entity: Trainers, monsters: Monsters ):
		for i, monster in monsters.items():
			if i < self.max_fighting_monsters: 
				compose(
					lambda i: self.__get_position(i, entity),
					lambda pos: self.__create_battle_sprite(pos, entity, monster)
				)( i )

	def __get_position ( self, i: int, entity: Trainers ):
		return { k: v for k, v in enumerate(BATTLE_POSITIONS['left' if entity == 'player' else 'right'].values()) }[i]

	def __create_battle_sprite ( self, pos: Pos, entity: Trainers, monster: Monster ):
		compose(
			partial(self.__create_monster_sprite, pos, entity),
			self.__display_monster_stats,
			lambda sprite: self.__create_monster_outline(sprite),
			self.__display_monster_name,
			self.__display_monster_level,
		)( monster )
		return monster

	def __create_monster_sprite ( self, pos: Pos, entity: Trainers, monster: Monster ):
		return MonsterSprite(monster, entity, MM.get('monster_frames')[monster.name], MM.get('monster_frames_outlines')[monster.name], pos, self.__handle_attack, self.battle_sprites, self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites)

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

	def __update_battle_sprites ( self, dt: float ):
		self.battle_sprites.update(dt)
		self.battle_sprites.draw_all(self.current_monster, self.targeted_monster, self.is_player_targeted)


	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)

	

	
	# INITIATIVE

	def __get_initiative ( self ):
		if self.mode: return

		sprite = self.__give_me_sprite()
		if sprite:
			self.freeze_all_monsters()
			compose(
				self.__reset_defense,
				self.__update_datas,
				self.__opponent_play,
			)( sprite )

	def __reset_player_initiative ( self ):
		for sprite in self.player_battle_sprites.sprites():
			sprite.monster.initiative = 0

	def __reset_defense ( self, sprite: MonsterSprite ):
		set_falsy(sprite.monster, 'is_defending')
		return sprite

	def __give_me_sprite ( self ):
		return next( (sprite for sprite in self.__get_all_fighters_sprites() if sprite.monster.initiative >= 100), None )

	def __update_datas ( self, sprite: MonsterSprite ): 
		sprite.monster.initiative = 0
		self.mode = 'general'
		self.target = 'opponent' if self.player_battle_sprites.has(sprite) else 'player'
		self.current_monster = sprite
		sprite.start_flash()
		return sprite

	def __opponent_play ( self, sprite: MonsterSprite ):
		if self.target == 'opponent': return
		self.__target_player_monster(sprite)
		start_timer(self.timers['delayed attack'])
	
	def __target_player_monster ( self, sprite: MonsterSprite ):
		self.targeted_monster = choice(self.player_battle_sprites.sprites())
		self.attack = choice([attack for attack in sprite.monster.get_abilities(False) if attack != 'heal' and attack != 'battlecry'])
		return sprite

	

	
	# DISPLAY MENUS

	def __display_menus ( self ):
		if self.target == 'player': return
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

	


	
	# INPUT

	# Input navigation
	def __input ( self ):
		if not self.current_monster or not self.mode: return
		keys = pygame.key.get_just_pressed()
		limiter = self.__get_limiter()

		if keys[pygame.K_UP]: return self.__set_indexes('up', limiter) 
		if keys[pygame.K_DOWN]: return self.__set_indexes('down', limiter) 
		if keys[pygame.K_SPACE]: return self.__action_input()
		if keys[pygame.K_ESCAPE]: return self.__back_input()

	def __set_indexes ( self, direction: Literal['up', 'down'], limiter: int ):
		if not self.mode: return
		if direction == 'up': self.indexes[self.mode] = (self.indexes[self.mode] - 1) % limiter
		if direction == 'down': self.indexes[self.mode] = (self.indexes[self.mode] + 1) % limiter

	def __get_limiter ( self ):
		match self.mode:
			case 'general': return len(BATTLE_CHOICES['full'])
			case 'attack': return len(required(self.current_monster).monster.get_abilities())
			case 'switch': return len(MM.get('monsters'))
			case 'target': return self.__get_group_size(required(self.target))
			case _: return 0

	def __back_input ( self ):
		match self.mode:
			case 'switch': self.mode = 'general'
			case 'attack': self.mode = 'general'
			case 'target': self.__attack_or_catch()
			case _: return
		self.__reset_indexes()

	def __attack_or_catch ( self ):
		if self.catch: 
			self.mode = 'general'
		else: 
			self.mode = 'attack'
			self.catch = False

	
	
	# Input selection
	## General
	def __action_input ( self ):
		match self.mode:
			case 'general': return self.__general_selector()
			case 'attack': return self.__attack_selector()
			case 'target': return self.__target_selector()
			case 'switch': return self.__switch_selector()
			case _: return

	def __general_selector ( self ):
		match self.indexes['general']:
			case 0: self.mode = 'attack'
			case 1: self.__defend()
			case 2: self.mode = 'switch'
			case 3: 
				self.mode = 'target'
				self.catch = True
		self.__reset_indexes()
  
	## Defend
	def __defend ( self ):
		set_truthy(required(self.current_monster).monster, 'is_defending')
		self.__resume_battle()

	## Select a target
	def __target_selector ( self ):
		if not self.current_monster: return
		self.current_monster.index = 0
		if self.catch: return self.__catch_a_monster()
		if not self.catch: return self.current_monster.set_state('attack')


	## Catch
	def __handle_monster_catch ( self ):
		compose(
			lambda catched: self.__bury_the_opponent_monster(catched),
			MM.add_monster,
		)(self.targeted_monster)
		self.__reset_batlle_sprites()

	def __reset_batlle_sprites ( self ):
		self.__kill_all_fighters_sprites()
		self.__initiate_battle()

	def __catch_a_monster ( self ):
		if not self.targeted_monster: return

		if self.targeted_monster.monster.is_catchable():
			self.__handle_monster_catch()
		else: 
			TimedSprite(1000, self.ui_images['cross'], self.battle_sprites, center=self.targeted_monster.rect.center)

		set_falsy(self, 'catch')
		self.__resume_battle()

	## Attack
	def __attack_selector ( self ):
		self.mode = 'target'
		self.attack = required(self.current_monster).monster.get_abilities(all_of_them=False)[self.indexes['attack']]
		self.target = ATTACK_DATA[self.attack]['target']

	def __handle_attack ( self ):
		if not self.attack: return
		print(self.attack)
		compose(
			self.__animate_attack,
			self.__update_health,
			self.__update_energy
		)( self.attack )
		self.__resume_battle()

	def __animate_attack ( self, attack: Attacks ):
		if not self.targeted_monster: return
		AttackAnimation(self.attack_frames[ATTACK_DATA[attack]['animation']], self.targeted_monster.rect.center, self.battle_sprites)
		MusicManager.play_attack(attack)
		return attack

	def __update_energy ( self, attack: Attacks ):
		if not self.current_monster: return
		self.current_monster.monster.lose_energy(attack)
		return attack

	def __update_health ( self, attack: Attacks ):
		if not self.targeted_monster: return
		elememt_datas = ( ATTACK_DATA[attack]['element'], self.targeted_monster.monster.base_stats['element'] )
		compose(
			lambda attack: required(self.targeted_monster).monster.get_attack_amount(attack),
			lambda amount: self.__halve(elememt_datas, amount),
			lambda amount: self.__double(elememt_datas, amount),
			self.targeted_monster.monster.take_damage
		)( attack )
		return attack


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

	## Switch
	def __switch_selector ( self ): 
		if not self.switch_list: return
		self.switch_list.select()
		self.__check_for_switch()
		self.__reset_indexes()

	def __check_for_switch ( self ):
		if not self.switch_list or not self.switch_list.switched: return
		for sprite in self.player_battle_sprites.sprites(): sprite.kill()
		self.monsters['player'] = MM.get('monsters')
		self.__draw_trainer_monsters('player', self.monsters['player'])
		self.switch_list.switched, self.mode = None, None
		self.__unfreeze_all_monsters()

	## Target	
	def __select_target ( self ):
		if self.mode != 'target' or not self.target: return
		sprites = { s.pos_index: s for s in sorted(self.__get_battle_sprites(self.target), key=lambda s: s.pos_index) }
		self.targeted_monster = sprites[ list(sprites.keys())[self.indexes['target']] ]



	
	# MONSTER DEATH
	
	def __check_death ( self ):
		if self.timers['delayed death'].running or \
		   all([sprite.monster.health > 0 for sprite in self.__get_all_fighters_sprites()]): 
			return
		self.freeze_all_monsters()
		self.timers['delayed death'].start()

	def __get_dead_monster ( self ):
		return next( (sprite for sprite in self.__get_all_fighters_sprites() if sprite.monster.health <= 0), None )

	def __bury_monster ( self ):
		dying = self.__get_dead_monster()
		if not dying: return
		if self.opponent_battle_sprites in dying.groups(): 
			self.__bury_the_opponent_monster(dying)
		else: 
			self.__bury_the_player_monster(dying)
		self.__unfreeze_all_monsters()

	def __bury_the_opponent_monster ( self, dying: MonsterSprite ):
		return compose(
			lambda dying: kill_sprite(dying),
			lambda dying: self.__remove_monster(dying, 'opponent'),
			lambda dying: self.__add_monster_to_battle('opponent', dying),
			self.__add_xp
		)( dying )

	def __bury_the_player_monster ( self, dying: MonsterSprite ):
		return compose( 
			lambda dying: kill_sprite(dying),
			lambda dying: MM.remove_monster(dying),
			lambda dying: self.__add_monster_to_battle('player', dying),
		)( dying )
		
	def __remove_monster ( self, dying: MonsterSprite, entity: Trainers ):
		self.monsters[entity] = { i: monster for i, monster in self.monsters[entity].items() if monster != dying.monster }
		return dying

	def __add_monster_to_battle ( self, entity: Trainers, dying: MonsterSprite ):
		if len(self.monsters[entity]) < self.max_fighting_monsters: return dying
		new_guy = self.__get_next_monster(entity)
		self.__create_battle_sprite(dying.pos, entity, new_guy)
		return dying

	def __add_xp ( self, dying: MonsterSprite ):
		amount = (dying.monster.level * 100) / len(self.player_battle_sprites)
		for sprite in self.player_battle_sprites: 
			sprite.monster.update_xp(amount)
		return dying

	def __get_next_monster ( self, entity: Trainers ):
		monster_sprites = [sprite.monster for sprite in self.__get_battle_sprites(entity).sprites()] 
		return required(next((monster for monster in self.monsters[entity].values() if monster not in monster_sprites), None))


	# END OF BATTLE

	def __check_for_end_of_battle ( self ):
		if self.victory or self.defeat: return
		if len(self.player_battle_sprites.sprites()) == 0: return self.__battle_lost()
		if len(self.opponent_battle_sprites.sprites()) == 0: return self.__battle_won()

	def __kill_player_sprites ( self ):
		for sprite in self.player_battle_sprites: 
			sprite.kill()

	def __battle_won ( self ):
		set_truthy(self, 'victory')
		self.__reset_player_initiative()
		self.__kill_player_sprites()

	def __battle_lost ( self ):
		voyeur('Battle, __battle_lost')
		set_truthy(self, 'defeat')
		self.freeze_all_monsters()


	
	# UTILS

	def freeze_all_monsters ( self ): 
		[ sprite.set_paused(True) for sprite in self.__get_all_fighters_sprites() ]

	def __unfreeze_all_monsters ( self ): 
		[ sprite.set_paused(False) for sprite in self.__get_all_fighters_sprites() ]

	def __reset_indexes ( self ): 
		self.indexes = { k: 0 for k in self.indexes }

	def __reset_variables_to_none ( self, names: list[str] ):
		for name in names: setattr(self, name, None)

	def __resume_battle ( self ):
		self.__reset_indexes()
		self.__unfreeze_all_monsters()
		self.__reset_variables_to_none(self.variables_none)

	def __update_timers ( self ):
		for timer in self.timers.values(): timer.update()

	def __get_battle_sprites ( self, entity: Trainers ):
		return self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites

	def __get_all_fighters_sprites ( self ): return self.player_battle_sprites.sprites() + self.opponent_battle_sprites.sprites()

	def __kill_all_fighters_sprites ( self ):
		for sprite in self.battle_sprites.sprites(): 
			kill_sprite(sprite)

	def __get_group_size ( self, entity: Trainers ): 
		return len( self.__get_battle_sprites(entity).sprites() )

	def is_player_targeted ( self ): return self.mode == 'target' and self.target == 'player'
	

	
	# UPDATE

	def update ( self, dt: float ):
		self.__update_timers()
		self.__check_for_end_of_battle()
		self.__check_death()
		self.__draw_battle_ground()
		self.__get_initiative()
		self.__input()
		self.__select_target()
		self.__update_battle_sprites(dt)
		self.__display_menus()
