from settings import *
from functools import partial
from typing import Callable
from pygame import Vector2

from entities.Entity import Entity
from utils.Helper import compose



def is_dialog_possible ( subject: Entity, entity: Entity, radius: int = 100, tolerance: int = 30 ):
	relation = get_relation(subject, entity)
	if relation.length() > radius: return
	return is_on_same_axis_x(relation, tolerance) and is_subject_facing_character_x(subject, relation) or\
		is_on_same_axis_y(relation, tolerance) and is_subject_facing_character_y(subject, relation)

def get_relation ( subject: Entity, entity: Entity, normalize: bool = False ):
	relation = pygame.Vector2(entity.rect.center) - pygame.Vector2(subject.rect.center)
	return relation.normalize() if normalize else relation

is_on_same_axis_x: Callable[ [Vector2, int], bool ] = lambda relation, tolerance: abs(relation.y) < tolerance
is_on_same_axis_y: Callable[ [Vector2, int], bool ] = lambda relation, tolerance: abs(relation.x) < tolerance

def is_subject_facing_character_x ( subject: Entity, relation: Vector2 ):
	return (subject.state == 'left' and relation.x < 0) or (subject.state == 'right' and relation.x > 0)
			
def is_subject_facing_character_y ( subject: Entity, relation: Vector2 ):
	return (subject.state == 'up' and relation.y < 0) or (subject.state == 'down' and relation.y > 0)

def turn_toward_entity (  subject: Entity, entity: Entity ):
	return compose( 
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

round_vector2: Callable[ [Vector2], Vector2 ] = lambda v: pygame.Vector2( round(v.x), round(v.y) )

def change_subject_state ( subject: Entity ):
	subject._set_state()
	return subject