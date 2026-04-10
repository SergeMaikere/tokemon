from settings import *
from functools import partial
from typing import Callable
from pytmx import TiledMap, TiledObject

from assets.data.game_data import TRAINER_DATA
from entities.Character import Character
from entities.Player import Player
from gameobj.CollisionSprite import CollisionSprite
from gameobj.MonsterPatch import MonsterPatch
from gameobj.AnimatedSprite import AnimatedSprite
from gameobj.Sprite import Sprite
from utils.AllSprites import AllSprites
from utils.MyGroup import MyGroup
from utils.DialogManager import DialogManager
from utils.Helper import coasts_image_cutter, get_layer_by_name_tiles, map_loader, images_loader_list, frames_loader, pipe, get_layer_by_name

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.all_sprites = AllSprites('all_sprites')
		self.collision_sprites = MyGroup('collision_sprites')
		self.all_characters = MyGroup('all_characters')

		self.water_frames = images_loader_list('assets', 'graphics', 'tilesets', 'water')
		self.coast_frames = coasts_image_cutter()

		self.terrains = ['Terrain']
		self.player_spawn = 'house'
		self.tmx_map = map_loader('world')
	
		self.player = self.get_player(self.tmx_map)

		self.dialog_manager = DialogManager(self.player, self.all_characters, self.all_sprites)


	def get_player ( self, tmx_map: TiledMap ):
		obj = next( obj for obj in get_layer_by_name(tmx_map, 'Entities') if obj.name == 'Player' and obj.pos == self.player_spawn )
		if obj:
			return self.__set_player(obj)
		else:
			raise ValueError('Player datas are missing from tmx map')

	def __quit_game ( self ):
		pygame.quit()
		exit()

	def __get_layer ( self, name: str, func: Callable, tmx_map: TiledMap ) -> TiledMap:
		for obj in get_layer_by_name(tmx_map, name):
			func(obj)
		return tmx_map

	def __set_terrain ( self, names: list[str], tmx_map: TiledMap ) -> TiledMap:
		for name in names:
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

	def __set_monster_patch ( self, obj: TiledObject ):
		MonsterPatch(obj.biome, obj.level, obj.monsters, obj.image, self.all_sprites, topleft=(obj.x, obj.y))

	def __set_coasts ( self, obj: TiledObject ):
		AnimatedSprite('coast', WORLD_LAYERS['bg'], self.coast_frames[obj.terrain][obj.side], self.all_sprites, topleft=(obj.x, obj.y))

	def __set_collisions_sprites ( self, obj: TiledObject ):
		image = pygame.Surface((obj.width, obj.height))
		Sprite('wall', WORLD_LAYERS['main'], image, self.collision_sprites, topleft=(obj.x, obj.y))
	
	def __set_player ( self, obj: TiledObject ):
		return Player(frames_loader(obj.name.lower()), (obj.x, obj.y), self.collision_sprites, self.all_sprites)

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

	def __setup( self ) -> TiledMap:
		return pipe(
			partial(self.__set_terrain, self.terrains),
			partial(self.__get_layer, 'Objects', self.__set_objects),
			partial(self.__get_layer, 'Water', self.__set_water),
			partial(self.__get_layer, 'Monsters', self.__set_monster_patch),
			partial(self.__get_layer, 'Coast', self.__set_coasts),
			partial(self.__get_layer, 'Collisions', self.__set_collisions_sprites),
			partial(self.__get_layer, 'Entities', self.__set_character),
		)(self.tmx_map)


	def run ( self ):
		
		self.__setup()

		while True:
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.__quit_game()

			self.canvas.fill('black')
			
			self.all_sprites.update(dt)

			self.dialog_manager.update()

			self.all_sprites.draw(self.player)

			pygame.display.update()



if __name__ == '__main__':
	new_game = Game()
	new_game.run()