from typing import Any, Callable
from settings import *
from os import walk
from os.path import join, basename
from functools import partial, reduce
from pytmx.util_pygame import load_pygame

pipe = lambda *funcs: lambda arg: reduce(lambda g, f: f(g), funcs, arg)

get_filename_from_path = lambda path: basename(path).split('.')[0]
def loader ( func: Callable[ [str], Any ], *path: str ):
	obj = {}
	for root, _, files in walk(join(*path)):
		if files:
			obj = reduce( lambda obj, file: {**obj, file.split('.')[0]: func(join(root, file))}, files, obj )
	return obj

load_image = lambda path: pygame.image.load(path).convert_alpha() 

maps_loader = partial(loader, load_pygame)

images_loader = partial(loader, load_image)

