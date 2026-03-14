from typing import Any, Callable

from pygame import Surface
from settings import *
from os import walk
from os.path import join, basename
from functools import partial, reduce
from pytmx.util_pygame import load_pygame

pipe = lambda *funcs: lambda arg: reduce(lambda g, f: f(g), funcs, arg)

get_name_from_path = lambda path: basename(path).split('.')[0]

def loader ( func: Callable[ [str], Any ], *path: str ):
	obj = {}
	for root, _, files in walk(join(*path)):
		if files:
			obj = reduce( lambda obj, file: {**obj, file.split('.')[0]: func(join(root, file))}, files, obj )
	return obj

def image_cutter ( rows: int, cols: int, image: Surface ):
	frames = []
	width, height = image.width / rows, image.height / cols
	for row in range(rows):
		for col in range(cols):
			surf = pygame.Surface((width, height), pygame.SRCALPHA)
			rect = pygame.FRect(width * col, height * row, width, height)
			surf.blit(image, (0, 0), rect)
			frames.append(surf)
	return frames



load_image = lambda path: pygame.image.load(path).convert_alpha() 

maps_loader = partial(loader, load_pygame)

frames_loader = partial(loader, pipe(load_image, partial(image_cutter, 4, 4)))

images_loader = partial(loader, load_image)

