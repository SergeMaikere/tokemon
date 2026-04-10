from entities.Player import Player
from settings import *
from os.path import join
from pygame.sprite import Sprite

from entities.Entity import Entity
from utils.Helper import load_image
from utils.MyGroup import MyGroup

class AllSprites ( MyGroup ):
	def __init__(self, name: str, *sprites: Sprite) -> None:
		super().__init__(name, *sprites)

		self.canvas = pygame.display.get_surface()
		self.shadow = load_image(join('assets', 'graphics', 'other', 'shadow.png'))
		self.notice = load_image(join('assets', 'graphics', 'ui', 'notice.png'))

		self.offset = pygame.Vector2()
		self.shadow_offset = pygame.Vector2(40, 110)

	def __get_offset ( self, player: Player ):
		self.offset.x = -(player.rect.centerx - WINDOW_WIDTH/2)
		self.offset.y = -(player.rect.centery - WINDOW_HEIGHT/2)

	def __get_layers ( self ):
		bg = [ sprite for sprite in self if sprite.z < WORLD_LAYERS['main'] ]
		main = sorted( [sprite for sprite in self if sprite.z == WORLD_LAYERS['main']], key=lambda sprite: sprite.y_order )
		top = [ sprite for sprite in self if sprite.z > WORLD_LAYERS['main'] ]
		return ( bg, main, top )

	def draw ( self, player: Player ):
		self.__get_offset(player)

		for layer in self.__get_layers():
			for sprite in layer:
				if isinstance(sprite, Entity): 
					self.canvas.blit(self.shadow, sprite.rect.topleft + self.offset + self.shadow_offset)

				self.canvas.blit(sprite.image, sprite.rect.topleft + self.offset)
				
				if sprite == player and player.is_noticed:
					rect = self.notice.get_frect(midbottom=sprite.rect.midtop)
					self.canvas.blit(self.notice, rect.topleft + self.offset)

		