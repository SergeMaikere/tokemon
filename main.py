from functools import partial
from pytmx import TiledMap
from settings import *
from utils.Helper import maps_loader, images_loader, pipe, get_filename_from_path
from gameobj.Sprite import Sprite

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.all_sprites = pygame.sprite.Group()

		self.maps = maps_loader('assets', 'data', 'maps')
		self.objects_images = images_loader('assets', 'graphics', 'objects')


	def __quit_game ( self ):
		pygame.quit()
		exit()

	def __set_terrain ( self, name: str, maps: TiledMap ) -> TiledMap:
		for x, y, image in maps.get_layer_by_name('Terrain').tiles():
			Sprite(image, self.all_sprites, topleft=(x * TILE_SIZE, y * TILE_SIZE))
		return maps

	def __set_objects ( self, maps: TiledMap ) -> TiledMap:
		for obj in maps.get_layer_by_name('Objects'):
			Sprite(self.objects_images[get_filename_from_path(obj.source)], self.all_sprites, topleft=(obj.x, obj.y))
		return maps
	

	def __setup( self ):
		pipe(
			partial(self.__set_terrain, 'Terrain'),
			self.__set_objects
		)(self.maps['world'])

	def run ( self ):

		self.__setup()
		
		while True:

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.__quit_game()
			
			self.all_sprites.update()

			self.all_sprites.draw(self.canvas)

			pygame.display.update()



if __name__ == '__main__':
	new_game = Game()
	new_game.run()