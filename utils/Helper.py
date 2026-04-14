from pytmx import TiledMap, TiledObject
from settings import *
from entities.Entity import Entity
from typing import Any, Callable, cast
from pygame import Surface, Vector2
from os import walk
from os.path import basename, join
from functools import partial, reduce
from pytmx.util_pygame import load_pygame

from utils.Types import Coasts, States

def voyeur ( x: Any ):
	print('\n****VOYEUR****')
	print(x)
	print('************\n')
	return x

pipe = lambda *funcs: lambda arg: reduce(lambda g, f: f(g), funcs, arg)

get_name_from_path = lambda path: basename(path).split('.')[0]

def big_walker_dict ( func: Callable[ [str], Any ], *path: str ):
	obj = {}
	for root, _, files in walk(join(*path)):
		if files:
			obj = reduce( lambda obj, file: {**obj, file.split('.')[0]: func(join(root, file))}, files, obj )
	return obj

def big_walker_list ( func: Callable[ [str], Any ], *path: str ):
	my_list = []
	for root, _, files in walk(join(*path)):
		if files:
			my_list = [ func(join(root, file)) for file in files ]
	return my_list

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

get_frames_obj: Callable[ [tuple[Any, ...]], dict[str, Any] ] = lambda my_list: reduce(lambda obj, prop: { **obj, prop: [] }, my_list, {})

get_cut_dimensions: Callable[ [tuple[int, int], Surface], tuple[float, float] ] = lambda dims, image: ( image.width/ dims[1], image.height/dims[0] )

def row_cut ( rows_cols: tuple[int, int], props: tuple[Any, ...], image: Surface ) -> dict[str, list[Surface]]:
	frames = get_frames_obj(props)
	width, height = get_cut_dimensions(rows_cols, image)
	for row, prop in enumerate(frames):
		for col in range(rows_cols[1]):
			surf = cut(image, row, col, width, height)
			frames[prop].append(surf)
	return frames

def col_cut ( rows_cols: tuple[int, int], props: tuple[Any, ...], image: Surface ) -> dict[str, Any]:
	frames = get_frames_obj(props)
	width, height = get_cut_dimensions(rows_cols, image)
	for col, prop in enumerate(frames):
		for row in range(rows_cols[0]):
			surf = cut(image, row, col, width, height)
			frames[prop].append(surf)
	return frames	

def fill_coast_frames_obj ( frames: dict[str, Any] ):
	for coast in frames:
		frames[coast] = partial(col_cut, (1, 3), ('left', '', 'right'))(frames[coast][0])
		for col in frames[coast]:
			frames[coast][col] = partial(row_cut, (4, 1), tuple(range(4)))(frames[coast][col][0])
			props = tuple( f'{level}{col}' for level in ['top', '', 'bottom'] )
			for row in frames[coast][col]:
				frames[coast][col][row] = partial( row_cut, (3, 1), props)(frames[coast][col][row][0])
	return frames

def set_coast_frames_obj ( frames: dict[str, Any] ):
	my_obj = reduce(lambda obj, k: { **obj, k: {}}, Coasts.__args__, {})
	for coast in frames:
		for col in frames[coast]:
			for level in frames[coast][col][0]:
				my_obj[coast][level] = [ frames[coast][col][n][level][0] for n in range(4) ]
	return my_obj

def get_coast_frames_cols (  ):
	coasts =  tuple(Coasts.__args__)
	return partial(col_cut, (1, len(coasts)), coasts)(small_walker(load_image, join('assets', 'graphics', 'tilesets'), 'coast'))

def coasts_image_cutter ():
	return pipe( 
		fill_coast_frames_obj, 
		set_coast_frames_obj, 
	)(get_coast_frames_cols())


def get_layer_by_name ( tmx_map: TiledMap, name: str ) -> list[TiledObject]: 
	return cast(list[TiledObject], tmx_map.get_layer_by_name(name))

def get_layer_by_name_tiles ( tmx_map: TiledMap, name: str ) -> list[tuple[float, float, Surface]]: 
	return tmx_map.get_layer_by_name(name).tiles()


	
load_image = lambda path: pygame.image.load(path).convert_alpha() 

load_font = lambda path, size = 30: pygame.font.Font(path, size)

font_loader = partial(small_walker, load_font, join('assets', 'graphics', 'fonts'))

map_loader: Callable[ [str], TiledMap ] = partial(small_walker, load_pygame, join('assets', 'data', 'maps'))

maps_loader: Callable [ [], dict[str, TiledMap] ] = lambda: big_walker_dict(load_pygame, join('assets', 'data', 'maps'))

images_loader_dict = partial(big_walker_dict, load_image)

images_loader_list = partial(big_walker_list, load_image)

load_frames = pipe(load_image, partial(row_cut, (4, 4), States.__args__))

frames_loader = partial(small_walker, load_frames, join('assets', 'graphics', 'characters'))


