from settings import *
from typing import Any, Callable, NoReturn
from pygame import Surface
from os import walk
from os.path import basename
from functools import partial, reduce
from pytmx.util_pygame import load_pygame

from utils.Types import States

pipe = lambda *funcs: lambda arg: reduce(lambda g, f: f(g), funcs, arg)

get_name_from_path = lambda path: basename(path).split('.')[0]

def big_walker ( func: Callable[ [str], Any ], *path: str ):
	obj = {}
	for root, _, files in walk(join(*path)):
		if files:
			obj = reduce( lambda obj, file: {**obj, file.split('.')[0]: func(join(root, file))}, files, obj )
	return obj

def small_walker ( func: Callable[ [str], Any ], path: str, name: str ):
	for _, _, files in walk(path):
		if files:
			basename = next(file for file in files if name in file)
			return func(join(path, basename))
	raise FileNotFoundError()

def cut ( image: Surface, row: int, col: int, width: float, height: float ):
	surf = pygame.Surface((width, height), pygame.SRCALPHA)
	rect = pygame.FRect(width * col, height * row, width, height)
	surf.blit(image, (0, 0), rect)
	return surf

def image_cutter ( rows: int, cols: int, image: Surface ) -> dict[str, list[Surface]]:
	states = States.__args__
	frames = reduce(lambda obj, state: { **obj, state: [] }, states, {})
	width, height = image.width/rows, image.height/cols

	for row in range(rows):
		for col in range(cols):
			surf = cut(image, row, col, width, height)
			frames[states[row]].append(surf)
	return frames



load_image = lambda path: pygame.image.load(path).convert_alpha() 

load_frames = pipe(load_image, partial(image_cutter, 4, 4))

map_loader = partial(small_walker, load_pygame, join('assets', 'data', 'maps'))

frames_loader = partial(small_walker, load_frames, join('assets', 'graphics', 'characters'))

images_loader = partial(big_walker, load_image)

