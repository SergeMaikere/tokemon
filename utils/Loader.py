from settings import *
from os import walk
from os.path import join
from functools import reduce
from pytmx.util_pygame import load_pygame

class Loader:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('TOKEMON BLACK --> Gotta catch them all !')

		self.maps = self.map_loader('assets', 'data', 'maps')



	def map_loader ( self, *path: str ):
		maps = {}
		for root, _, files in walk(join(*path)):
			print('SEEEERGE')
			if files: 
				# maps = reduce( lambda obj, file: {**obj, file.split('.')[0]: load_pygame(join(root, file))}, files, maps )
				for file in files:
					print(join(root, file))
					maps[file.split('.')[0]] = load_pygame(join(root, file))
		return maps