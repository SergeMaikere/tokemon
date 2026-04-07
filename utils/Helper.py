from settings import *
from entities.Entity import Entity
from typing import Any, Callable
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

def is_dialog_possible ( subject: Entity, entity: Entity, radius: int = 100, tolerance: int = 30 ):
	relation = get_relation(subject, entity)
	if relation.length() > radius: return
	return is_on_same_axis_x(relation, tolerance) and is_subject_facing_character_x(subject, relation) or\
		is_on_same_axis_y(relation, tolerance) and is_subject_facing_character_y(subject, relation)

def get_relation ( subject: Entity, entity: Entity, normalize: bool = False ):
	relation = Vector2(entity.rect.center) - Vector2(subject.rect.center)
	return relation.normalize() if normalize else relation

is_on_same_axis_x: Callable[ [Vector2, int], bool ] = lambda relation, tolerance: abs(relation.y) < tolerance
is_on_same_axis_y: Callable[ [Vector2, int], bool ] = lambda relation, tolerance: abs(relation.x) < tolerance

def is_subject_facing_character_x ( subject: Entity, relation: Vector2 ):
	return (subject.state == 'left' and relation.x < 0) or (subject.state == 'right' and relation.x > 0)
			
def is_subject_facing_character_y ( subject: Entity, relation: Vector2 ):
	return (subject.state == 'up' and relation.y < 0) or (subject.state == 'down' and relation.y > 0)

def turn_toward_entity (  subject: Entity, entity: Entity ):
	return pipe( 
		partial(get_subject_direction, entity=entity), 
		round_subject_direction, 
		change_subject_state 
	)(subject)

def get_subject_direction ( subject: Entity, entity: Entity ):
	subject.direction = partial( get_relation, entity=entity, normalize=True )(subject)
	return subject

def round_subject_direction ( subject: Entity ):
	subject.direction = round_vector2(subject.direction)
	return subject

def change_subject_state ( subject: Entity ):
	subject._set_state()
	return subject

round_vector2: Callable[ Vector2, Vector2 ] = lambda v: Vector2( round(v.x), round(v.y) )

	
load_image = lambda path: pygame.image.load(path).convert_alpha() 

load_font = lambda path, size = 30: pygame.font.Font(path, size)

font_loader = partial(small_walker, load_font, join('assets', 'graphics', 'fonts'))

map_loader = partial(small_walker, load_pygame, join('assets', 'data', 'maps'))

images_loader_dict = partial(big_walker_dict, load_image)

images_loader_list = partial(big_walker_list, load_image)

load_frames = pipe(load_image, partial(row_cut, (4, 4), States.__args__))

frames_loader = partial(small_walker, load_frames, join('assets', 'graphics', 'characters'))


