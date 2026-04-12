from functools import partial
from settings import *
from pytmx import TiledMap, TiledObject

from entities.Player import Player
from utils.AllSprites import AllSprites
from utils.MapTransition import MapTransition
from utils.MapsLoader import MapsLoader
from utils.MyGroup import MyGroup
from utils.DialogManager import DialogManager
from utils.Helper import map_loader, frames_loader, get_layer_by_name, pipe, voyeur

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.all_sprites = AllSprites('all_sprites')
		self.collision_sprites = MyGroup('collision_sprites')
		self.character_sprites = MyGroup('character_sprites')
		self.transition_sprites = MyGroup('transition_sprites')
	
		self.player = self.get_player(map_loader('world'), 'house')

		self.dialog_manager = DialogManager(self.player, self.character_sprites, self.all_sprites)

		self.maps_loader = MapsLoader(self.player, self.dialog_manager, self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites)

		self.transition_manager = MapTransition(self.player)

	def get_player ( self, tmx_map: TiledMap, player_spawn: str ):
		obj = next( obj for obj in get_layer_by_name(tmx_map, 'Entities') if obj.name == 'Player' and obj.pos == player_spawn )
		if obj:
			return Player(frames_loader('player'), (obj.x, obj.y), self.collision_sprites, self.all_sprites)
		else:
			raise ValueError('Player datas are missing from tmx map')

	def __quit_game ( self ):
		pygame.quit()
		exit()

	def __handle_transition ( self, dt: float ):
		pipe(
			self.transition_manager.check_for_collision,
			partial(self.transition_manager.fade_to_black, dt),
		)(self.transition_sprites)

	def run ( self ):
		
		self.maps_loader.setup(self.maps_loader.maps['world'])

		while True:
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.__quit_game()

			self.canvas.fill('black')
			
			self.all_sprites.update(dt)

			self.dialog_manager.update()

			self.all_sprites.draw(self.player)

			self.__handle_transition(dt)

			pygame.display.update()



if __name__ == '__main__':
	new_game = Game()
	new_game.run()