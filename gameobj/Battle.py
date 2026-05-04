from functools import partial
from pygame import Font

from settings import *
from entities.Monster import Monster
from gameobj.MonsterSprite import MonsterSprite
from utils.Helper import add_background_to_text, add_color_to_surface, add_text_to_card, display_item, get_rect, get_sized_surface, get_text_surface, required, get_group, pipe, voyeur
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Types import FontTypes, MonsterNames, Trainers

class Battle:
	def __init__( self, battle_ground: Surface, monster_manager: MonsterManager, fonts: dict[FontTypes, Font], opponent_monsters: dict[int, tuple[MonsterNames, int]], *groups: MyGroup ) -> None:
		
		self.MM = monster_manager
		self.opponent_monsters = opponent_monsters
		self.fonts = fonts
		self.battle_ground_surface = battle_ground
		self.battle_ground_rect = self.battle_ground_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
		
		self.battle_sprites = get_group(groups, 'battle_sprites')
		self.player_battle_sprites = get_group(groups, 'player_battle_sprites')
		self.opponent_battle_sprites = get_group(groups, 'opponent_battle_sprites')

		self.canvas = required(pygame.display.get_surface())

		self.monsters = { 
			'player': self.MM.get_player_battle_monsters(), 
			'opponent': self.MM.get_opponent_battle_monsters(self.opponent_monsters) 
		}

		self.monster_sprites: dict[ Trainers, list[MonsterSprite] ] = {
			'player': self.__get_monster_sprites('player'),
			'opponent': self.__get_monster_sprites('opponent')
		}

		self.level_surface = pygame.Surface((60, 26))

	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)

	def __get_monster_sprites ( self, entity: Trainers ):
		return [ self.__create_monster_sprite(monster, entity, i) for i, monster in enumerate(self.monsters[entity]) ]

	def __create_monster_sprite ( self, monster: Monster, entity: Trainers, i: int ):
		pos = { k: v for k, v in enumerate(BATTLE_POSITIONS['left' if entity == 'player' else 'right'].values()) }[i]
		groups = ( self.battle_sprites, self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites )
		return MonsterSprite(monster, entity, self.MM.monster_frames[monster.name], pos, *groups)

	def __display_monsters ( self, dt: float ):
		self.battle_sprites.update(dt)
		self.battle_sprites.draw(self.canvas)

	def __display_infos ( self ):
		for entity, sprites in self.monster_sprites.items():
			for sprite in sprites:
				pipe(
					partial(self.__display_name, entity),
					partial(self.__display_level, entity, sprite)
				)( sprite )

	def __display_name ( self, entity: Trainers, sprite: MonsterSprite ):
		return pipe(
			add_background_to_text,
			partial(self.__get_text_rect, entity, sprite),
			partial(display_item, self.canvas)
		)( get_text_surface(self.fonts['regular'], sprite.monster.name) )

	def __get_text_rect ( self, entity: Trainers, sprite: MonsterSprite, text_surface: Surface ):
		if entity == 'player': return get_rect(text_surface, midtop=sprite.rect.midleft + vector( 16, -70))
		if entity == 'opponent': return get_rect(text_surface, midtop=sprite.rect.midright + vector( -16, -70))

	def __display_level ( self, entity: Trainers, sprite: MonsterSprite, name_rect: FRect ):
		pipe(
			partial(self.__create_level_card, entity, sprite)
		)(name_rect)

	def __create_level_card ( self, entity: Trainers, sprite: MonsterSprite, name_rect: FRect ):
		pipe(
			add_color_to_surface,
			partial(self.__place_level_card, entity, name_rect),
			partial(self.__add_text_to_card, sprite),
			partial(display_item, self.canvas)
		)( self.level_surface )

	def __place_level_card ( self, entity: Trainers, name_rect: FRect, level_surface: Surface ):
		if entity == 'player': return get_rect(level_surface, topleft=name_rect.bottomleft)
		if entity == 'opponent': return get_rect(level_surface, topright=name_rect.bottomright)

	def __add_text_to_card ( self, sprite: MonsterSprite, datas: tuple[ Surface, FRect ] ):
		card_surface, card_rect = datas
		text_surface = get_text_surface(self.fonts['small'], f'Lvl: {sprite.monster.level}') 
		return (add_text_to_card(card_surface, text_surface), card_rect)

	def update ( self, dt: float ):
		self.__draw_battle_ground()
		self.__display_monsters(dt)
		self.__display_infos()
		