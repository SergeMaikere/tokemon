from typing import Literal
from entities.Monster import Monster
from gameobj.MonsterSprite import MonsterSprite
from settings import *
from utils.Helper import required, get_group
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Types import MonsterNames

class Battle:
	def __init__( self, battle_ground: Surface, monster_manager: MonsterManager, opponent_monsters: dict[int, tuple[MonsterNames, int]], *groups: MyGroup ) -> None:
		
		self.MM = monster_manager
		self.opponent_monsters = opponent_monsters

		self.battle_sprites = get_group(groups, 'battle_sprites')
		self.player_battle_sprites = get_group(groups, 'player_battle_sprites')
		self.opponent_battle_sprites = get_group(groups, 'opponent_battle_sprites')

		self.battle_ground_surface = battle_ground
		self.battle_ground_rect = self.battle_ground_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.canvas = required(pygame.display.get_surface())

		self.monsters = { 
			'player': self.MM.get_player_battle_monsters(), 
			'opponent': self.MM.get_opponent_battle_monsters(self.opponent_monsters) 
		}

		self.player_monster_sprites = self.__get_monster_sprites('player')
		self.opponent_monster_sprites = self.__get_monster_sprites('opponent')


	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)

	def __get_monster_sprites ( self, entity: Literal[ 'player', 'opponent' ] ):
		return [ self.__create_monster_sprite(monster, entity, i) for i, monster in enumerate(self.monsters[entity]) ]

	def __create_monster_sprite ( self, monster: Monster, entity: Literal[ 'player', 'opponent' ], i: int ):
		pos = { k: v for k, v in enumerate(BATTLE_POSITIONS['left' if entity == 'player' else 'right'].values()) }[i]
		groups = ( self.battle_sprites, self.player_battle_sprites if entity == 'player' else self.opponent_battle_sprites )
		return MonsterSprite(monster, entity, self.MM.monster_frames[monster.name], pos, *groups)

	def __update_monsters ( self ):
		self.monsters['player'] = self.MM.get_player_battle_monsters()
		for sprite in self.player_monster_sprites: sprite.kill()
		self.player_monster_sprites = self.__get_monster_sprites('player')

	def __display_monsters ( self, dt: float ):
		self.battle_sprites.update(dt)
		self.battle_sprites.draw(self.canvas)

	def update ( self, dt: float ):
		self.__draw_battle_ground()
		self.__update_monsters()
		self.__display_monsters(dt)
		