from typing import Callable
from settings import *
from gameobj.AnimatedSprite import AnimatedSprite
from functools import partial
from pytmx import TileFlags, TiledMap, TiledObject
from entities.Player import Player
from utils.AllSprites import AllSprites
from utils.Helper import coasts_image_cutter, map_loader, images_loader_dict, images_loader_list, frames_loader, pipe
from gameobj.Sprite import Sprite

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.all_sprites = AllSprites()

		self.map = map_loader('world')
		self.terrains = ['Terrain']
		self.player_spawn = 'house'


		self.objects_images = images_loader_dict('assets', 'graphics', 'objects')
		self.water_frames = images_loader_list('assets', 'graphics', 'tilesets', 'water')
		self.coast_frames = coasts_image_cutter()

	def __quit_game ( self ):
		pygame.quit()
		exit()

	def __get_layer ( self, name: str, func: Callable, maps: TiledMap ) -> TiledMap:
		for obj in maps.get_layer_by_name(name):
			func(obj)
		return maps

	def __set_terrain ( self, names: list[str], maps: TiledMap ) -> TiledMap:
		for name in names:
			for x, y, image in maps.get_layer_by_name(name).tiles():
				Sprite('terrain', image, self.all_sprites, topleft=(x * TILE_SIZE, y * TILE_SIZE))
		return maps

	def __set_objects ( self, obj: TiledObject ):
		Sprite('object', obj.image, self.all_sprites, center=(obj.x, obj.y))

	def __set_water ( self, obj: TiledObject ):
		for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
			for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
				AnimatedSprite('water', self.water_frames, self.all_sprites, topleft=(x, y))

	def __set_coasts ( self, obj: TiledObject ):
		AnimatedSprite('coast', self.coast_frames[obj.terrain][obj.side], self.all_sprites, topleft=(obj.x, obj.y))

	def __set_Player ( self, obj: TiledObject ):
		if obj.name == 'Player' and obj.pos == self.player_spawn: 
			self.player = Player(frames_loader(obj.name.lower()), (obj.x, obj.y), self.all_sprites)
		return obj


	def __set_entities ( self, obj: TiledObject ):
		self.__set_Player(obj)


	def __setup( self ):
		pipe(
			partial(self.__set_terrain, self.terrains),
			partial(self.__get_layer, 'Objects', self.__set_objects),
			partial(self.__get_layer, 'Water', self.__set_water),
			partial(self.__get_layer, 'Coast', self.__set_coasts),
			partial(self.__get_layer, 'Entities', self.__set_entities)
		)(self.map)

	
	def run ( self ):

		self.__setup()
		
		while True:
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.__quit_game()

			self.canvas.fill('black')
			
			self.all_sprites.update(dt)

			self.all_sprites.draw(self.player.rect.center)

			pygame.display.update()



if __name__ == '__main__':
	new_game = Game()
	new_game.run()