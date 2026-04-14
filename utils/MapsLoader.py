from functools import partial
from typing import Callable
from pytmx import TiledMap, TiledObject

from gameobj.TransitionSprite import TransitionSprite
from settings import *
from assets.data.game_data import TRAINER_DATA
from entities.Character import Character
from entities.Player import Player
from gameobj.MonsterPatch import MonsterPatch
from gameobj.Sprite import Sprite
from gameobj.AnimatedSprite import AnimatedSprite
from gameobj.CollisionSprite import CollisionSprite
from utils.DialogManager import DialogManager
from utils.Helper import pipe, get_layer_by_name, get_layer_by_name_tiles, maps_loader, images_loader_list, coasts_image_cutter, frames_loader
from utils.MyGroup import MyGroup

class MapsLoader:
	def __init__(self, player: Player, dialog_manager: DialogManager, *groups: MyGroup) -> None:
		
		self.player = player
		self.dialog_manager = dialog_manager

		self.maps = maps_loader()
		self.water_frames = images_loader_list('assets', 'graphics', 'tilesets', 'water')
		self.coast_frames = coasts_image_cutter()

		self.groups = groups
		self.all_sprites, self.collision_sprites, self.all_characters, self.transition_sprites = self.groups


	def __get_layer ( self, name: str, func: Callable, tmx_map: TiledMap ) -> TiledMap:
		for obj in get_layer_by_name(tmx_map, name):
			func(obj)
		return tmx_map

	def __set_terrain ( self, name: str, tmx_map: TiledMap ) -> TiledMap:
		for x, y, image in get_layer_by_name_tiles(tmx_map, name):
			Sprite('terrain', WORLD_LAYERS['bg'], image, self.all_sprites, topleft=(x * TILE_SIZE, y * TILE_SIZE))
		return tmx_map

	def __set_objects ( self, obj: TiledObject ):
		CollisionSprite( 
			WORLD_LAYERS['main' if obj.name != 'top' else 'top'],
			obj.image, 
			self.collision_sprites, 
			self.all_sprites, 
			topleft=(obj.x, obj.y)
		)

	def __set_water ( self, obj: TiledObject ):
		for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
			for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
				AnimatedSprite('water', WORLD_LAYERS['water'], self.water_frames, self.all_sprites, topleft=(x, y))

	def __set_transition ( self, obj: TiledObject ):
		TransitionSprite(pygame.Surface((obj.width, obj.height)), obj.target, obj.pos, self.transition_sprites, center=(obj.x, obj.y))

	def __set_monster_patch ( self, obj: TiledObject ):
		MonsterPatch(obj.biome, obj.level, obj.monsters, obj.image, self.all_sprites, topleft=(obj.x, obj.y))

	def __set_coasts ( self, obj: TiledObject ):
		AnimatedSprite('coast', WORLD_LAYERS['bg'], self.coast_frames[obj.terrain][obj.side], self.all_sprites, topleft=(obj.x, obj.y))

	def __set_collisions_sprites ( self, obj: TiledObject ):
		image = pygame.Surface((obj.width, obj.height))
		Sprite('wall', WORLD_LAYERS['main'], image, self.collision_sprites, topleft=(obj.x, obj.y))
	
	def __set_player ( self, player_spawn_pos: str, obj: TiledObject ):
		if obj.name == 'Player' and obj.pos == player_spawn_pos:
			self.player.rect.center = (obj.x, obj.y)
			self.all_sprites.add(self.player)
		return obj

	def __set_character ( self, obj: TiledObject ):
		if obj.name == 'Character':
			Character(
				self.player,
				obj.direction, 
				frames_loader(obj.graphic), 
				(obj.x, obj.y), 
				TRAINER_DATA[obj.character_id],
				int(obj.radius), 
				self.dialog_manager,
				self.collision_sprites, self.all_characters, self.all_sprites
			)
		return obj

	def __set_entities ( self, player_spawn_pos: str, obj: TiledObject ):
		pipe(
			partial(self.__set_player, player_spawn_pos),
			self.__set_character,
		)(obj)

	def __kill_all_sprites ( self ):
		for group in self.groups: group.empty()

	def setup( self, tmx_map: TiledMap ) -> TiledMap:
		return pipe(
			partial(self.__set_terrain, 'Terrain'),
			partial(self.__set_terrain, 'Terrain Top'),
			partial(self.__get_layer, 'Water', self.__set_water),
			partial(self.__get_layer, 'Transition', self.__set_transition),
			partial(self.__get_layer, 'Collisions', self.__set_collisions_sprites),
			partial(self.__get_layer, 'Objects', self.__set_objects),
			partial(self.__get_layer, 'Monsters', self.__set_monster_patch),
			partial(self.__get_layer, 'Coast', self.__set_coasts),
			partial(self.__get_layer, 'Entities', self.__set_character),
		)(tmx_map)

	def transition_setup( self, tmx_map: TiledMap, player_spawn_pos: str ):
		self.__kill_all_sprites()
		return pipe(
			partial(self.__set_terrain, 'Terrain'),
			partial(self.__set_terrain, 'Terrain Top'),
			partial(self.__get_layer, 'Water', self.__set_water),
			partial(self.__get_layer, 'Transition', self.__set_transition),
			partial(self.__get_layer, 'Collisions', self.__set_collisions_sprites),
			partial(self.__get_layer, 'Objects', self.__set_objects),
			partial(self.__get_layer, 'Monsters', self.__set_monster_patch),
			partial(self.__get_layer, 'Coast', self.__set_coasts),
			partial(self.__get_layer, 'Entities', partial(self.__set_entities, player_spawn_pos)),
		)(tmx_map)
