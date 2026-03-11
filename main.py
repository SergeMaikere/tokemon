from settings import *

class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.clock = pygame.time.Clock()
		self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.all_sprites = pygame.sprite.Group()

		self.running = True

	def run ( self ):
		
		while self.running:

			for event in pygame.event.get():
				self.running = not event.type == pygame.QUIT
			
			self.all_sprites.update()

			self.all_sprites.draw(self.canvas)

			pygame.display.update()

		pygame.quit()


if __name__ == '__main__':
	new_game = Game()
	new_game.run()