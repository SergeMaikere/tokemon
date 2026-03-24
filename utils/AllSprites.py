from settings import *
from pygame.sprite import Sprite

class AllSprites ( pygame.sprite.Group ):
	def __init__(self, *sprites: Sprite) -> None:
		super().__init__(*sprites)

		self.canvas = pygame.display.get_surface()
		self.offset = pygame.Vector2()

	def __get_offset ( self, player_pos: tuple[float, float] ):
		self.offset.x = -(player_pos[0] - WINDOW_WIDTH/2)
		self.offset.y = -(player_pos[1] - WINDOW_HEIGHT/2)

	def draw ( self, player_pos: tuple[float, float] ):
		self.__get_offset(player_pos)

		terrain = [ sprite for sprite in self if sprite.type in ['terrain', 'water', 'coast'] ]
		objects = [ sprite for sprite in self if sprite.type not in ['terrain', 'water', 'coast'] ]

		for layer in [ terrain, objects ]:
			for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
				self.canvas.blit(sprite.image, sprite.rect.center + self.offset)

		