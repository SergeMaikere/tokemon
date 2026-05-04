from functools import partial
from pygame import Font

from gameobj.MonsterLevelSprite import MonsterLevelSprite
from gameobj.MonsterNameSprite import MonsterNameSprite
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

		self.monsters: dict[Trainers, list[Monster]] = { 
			'player': self.MM.get_player_battle_monsters(), 
			'opponent': self.MM.get_opponent_battle_monsters(self.opponent_monsters) 
		}

	
		self.level_surface = pygame.Surface((60, 26))

		self.initiate_battle()

	def initiate_battle ( self ):
		for entity, monsters in self.monsters.items():
			for i, monster in enumerate(monsters):
				self.__creates_all_battle_sprites(i, entity, monster)

	def update_battle_sprites ( self, dt: float ):
		self.battle_sprites.update(dt)
		self.battle_sprites.draw(self.canvas)

	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)


	def __creates_all_battle_sprites ( self, i: int, entity: Trainers, monster: Monster ):
		pipe(
			partial(self.__create_monster_sprite, i, entity),
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

	def update ( self, dt: float ):
		self.__draw_battle_ground()
		self.update_battle_sprites(dt)
