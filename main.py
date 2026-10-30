from typing import Callable

from pygame import Font
from pytmx import TiledMap
from pytmx.pytmx import TiledObject

from entities.Character import Character
from entities.Entity import Entity
from settings import *
from gameobj.MonsterIndex import MonsterIndex
from entities.Player import Player
from utils.AllSprites import AllSprites
from utils.CollisionManager import CollisionManager
from utils.BattleManager import BattleManager
from utils.BattleSprites import BattleSprites
from utils.EvolutionManager import EvolutionManager
from utils.GameOverManager import GameOverManager
from utils.MapsLoader import MapsLoader
from utils.MonsterManager import MonsterManager
from utils.MusicManager import MusicManager
from utils.MyGroup import MyGroup
from utils.DialogManager import DialogManager
from utils.Helper import map_loader, frames_loader, get_layer_by_name, font_loader, images_loader_dict, quit_game, set_falsy, compose
from utils.Types import FontTypes

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.fonts: dict[FontTypes, Font] = {
			'regular': font_loader('PixeloidSan', 18),
			'small': font_loader('PixeloidSan', 14),
			'bold': font_loader('dogicapixelbold', 20),
			'giant': font_loader('dogicapixelbold', 96)
		}

		self.ui_images = images_loader_dict('assets', 'graphics', 'ui')

		self.all_sprites = AllSprites('all_sprites')
		self.collision_sprites = MyGroup('collision_sprites')
		self.character_sprites = MyGroup('character_sprites')
		self.transition_sprites = MyGroup('transition_sprites')
		self.monster_patch_sprites = MyGroup('monster_patch_sprites')
		self.battle_sprites = BattleSprites()
		self.player_battle_sprites = MyGroup('player_battle_sprites')
		self.opponent_battle_sprites = MyGroup('opponent_battle_sprites')
		
		self.overworld_map = map_loader('world')
		self.player = self.access_player(self.overworld_map, 'house', self.create_player)

		MonsterManager.init()
		MusicManager.init()
		
		self.game_over_manager = GameOverManager(self.player, lambda: self.reset_entity_pos(self.player), self.reset_characters)
		
		self.evolution_manager = EvolutionManager(self.player, self.fonts['bold'], self.player_battle_sprites)
		
		self.battle_manager = BattleManager(self.player, self.fonts, self.ui_images, self.game_over_manager, self.evolution_manager, self.battle_sprites, self.player_battle_sprites, self.opponent_battle_sprites)
		
		self.dialog_manager = DialogManager(self.player, self.character_sprites, self.battle_manager, self.all_sprites)

		self.maps_loader = MapsLoader(self.player, self.dialog_manager, self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites, self.monster_patch_sprites)
 
		self.monster_index = MonsterIndex(self.player, self.fonts, self.ui_images)

		self.collision_manager = CollisionManager(self.player, self.maps_loader.transition_setup, self.battle_manager, self.transition_sprites, self.monster_patch_sprites)
	
	def access_player ( self, tmx_map: TiledMap, player_spawn: str, func: Callable ):
		obj = next( obj for obj in get_layer_by_name(tmx_map, 'Entities') if obj.name == 'Player' and obj.pos == player_spawn )
		if obj:
			return func(obj)
		else:
			raise ValueError('Player datas are missing from tmx map')
	
	def create_player ( self, obj: TiledObject ):
		return Player(frames_loader('player'), (obj.x, obj.y), self.collision_sprites, self.all_sprites)

	def reset_entity_pos ( self, entity: Entity ):
		entity.rect.center = entity.hitbox.center = entity.original_pos
		return entity

	def __reset_character_defeated ( self, character: Character ):
		set_falsy(character.datas, 'defeated')
		return character

	def reset_characters ( self ):
		for character in self.character_sprites.sprites():
			compose(
				self.reset_entity_pos,
				self.__reset_character_defeated,
				lambda character: set_falsy(character, 'has_noticed_player'),
			)( character )

	def run ( self ):
		
		self.maps_loader.setup(self.maps_loader.maps['world'])
		MusicManager.play_in_loop('overworld')

		while True:
			dt = self.clock.tick(60) / 1000

			self.canvas.fill((0, 0, 0, 0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT: quit_game()

			self.all_sprites.update(dt)

			self.all_sprites.draw(self.player)

			self.dialog_manager.update()

			self.battle_manager.update(dt)

			self.collision_manager.update(dt)

			self.monster_index.update(dt)

			self.evolution_manager.update(dt)

			self.game_over_manager.update(dt)
				
			pygame.display.update( )


if __name__ == '__main__':
	new_game = Game()
	new_game.run()