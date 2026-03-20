from functools import partial
from pytmx import TiledMap, load_pygame
from entities.Player import Player
from settings import *
from utils.AllSprites import AllSprites
from utils.Helper import map_loader, images_loader, frames_loader, pipe, get_name_from_path
from gameobj.Sprite import Sprite

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.all_sprites = AllSprites()

		self.map = map_loader('world')
		self.objects_images = images_loader('assets', 'graphics', 'objects')

		self.player_spawn = 'house'
		self.terrains = ['Terrain']


	def __quit_game ( self ):
		pygame.quit()
		exit()

	def __set_terrain ( self, names: list[str], maps: TiledMap ) -> TiledMap:
		for name in names:
			for x, y, image in maps.get_layer_by_name(name).tiles():
				Sprite('terrain', image, self.all_sprites, topleft=(x * TILE_SIZE, y * TILE_SIZE))
		return maps

	def __set_entities ( self, maps: TiledMap ) -> TiledMap:
		for obj in maps.get_layer_by_name('Entities'):
			if obj.name == 'Player' and obj.pos == self.player_spawn: 
				self.player = Player(frames_loader(obj.name.lower()), (obj.x, obj.y), self.all_sprites)
		return maps

	def __set_objects ( self, maps: TiledMap ) -> TiledMap:
		for obj in maps.get_layer_by_name('Objects'):
			Sprite('object', self.objects_images[get_name_from_path(obj.source)], self.all_sprites, center=(obj.x, obj.y))
		return maps
	
	def __setup( self ):
		pipe(
			partial(self.__set_terrain, self.terrains),
			self.__set_objects,
			self.__set_entities,
		)(self.map)

	def run ( self ):

		self.__setup()
		
		while True:
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.__quit_game()
			
			self.all_sprites.update(dt)

			self.all_sprites.draw(self.player.rect.center)

			pygame.display.update()



if __name__ == '__main__':
	new_game = Game()
	new_game.run()