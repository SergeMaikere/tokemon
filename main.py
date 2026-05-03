from gameobj.MonsterIndex import MonsterIndex
from settings import *
from pytmx import TiledMap

from entities.Player import Player
from utils.AllSprites import AllSprites
from utils.BattleManager import BattleManager
from utils.MapTransition import MapTransition
from utils.MapsLoader import MapsLoader
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.DialogManager import DialogManager
from utils.Helper import map_loader, frames_loader, get_layer_by_name, font_loader, images_loader_dict

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.fonts = {
			'regular': font_loader('PixeloidSan', 18),
			'small': font_loader('PixeloidSan', 14),
			'bold': font_loader('dogicapixelbold', 20),
		}

		self.ui_images = images_loader_dict('assets', 'graphics', 'ui')

		self.all_sprites = AllSprites('all_sprites')
		self.collision_sprites = MyGroup('collision_sprites')
		self.character_sprites = MyGroup('character_sprites')
		self.transition_sprites = MyGroup('transition_sprites')
	
		self.player = self.get_player(map_loader('world'), 'house')

		self.monster_manager = MonsterManager()
		
		self.battle_manager = BattleManager(self.player, self.monster_manager, self.fonts)
		
		self.dialog_manager = DialogManager(self.player, self.character_sprites, self.battle_manager, self.all_sprites)

		self.maps_loader = MapsLoader(self.player, self.dialog_manager, self.all_sprites, self.collision_sprites, self.character_sprites, self.transition_sprites)

		self.transition_manager = MapTransition(self.player, self.maps_loader, self.get_player)

		self.monster_index = MonsterIndex(self.player, self.monster_manager, self.fonts, self.ui_images)


	def get_player ( self, tmx_map: TiledMap, player_spawn: str ):
		obj = next( obj for obj in get_layer_by_name(tmx_map, 'Entities') if obj.name == 'Player' and obj.pos == player_spawn )
		if obj:
			return Player(frames_loader('player'), (obj.x, obj.y), self.collision_sprites, self.all_sprites)
		else:
			raise ValueError('Player datas are missing from tmx map')

	def __quit_game ( self ):
		pygame.quit()
		exit()

	def run ( self ):
		
		self.maps_loader.setup(self.maps_loader.maps['world'])

		while True:
			dt = self.clock.tick(60) / 1000

			self.canvas.fill('black')

			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.__quit_game()
			
			self.all_sprites.update(dt)

			self.dialog_manager.update()

			self.all_sprites.draw(self.player)

			self.battle_manager.update(dt)

			self.monster_index.update(dt)
			
			self.transition_manager.handle_transitions(dt)

			pygame.display.update( )



if __name__ == '__main__':
	new_game = Game()
	new_game.run()