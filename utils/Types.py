
from typing import Callable, Generic, Literal, TypeVar, TypedDict, cast
from pygame import Vector2
from pytmx.pytmx import ColorLike


States = Literal[ 'down', 'left', 'right', 'up' ]

Coasts = Literal[ 'grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i' ]

Biomes = Literal[ 'grass', 'grass_ice', 'sand' ]

TransitionState = Literal[ 'standby', 'fade_to_black', 'load_scene', 'fade_to_light', 'done' ]

FontTypes = Literal[ 'regular', 'small', 'bold', 'dialog', 'giant' ]

Attacks = Literal[ 'burn', 'heal', 'battlecry', 'spark', 'scratch', 'splash', 'fire', 'explosion', 'annihilate', 'ice' ]

MonsterNames = Literal[ 'Plumette', 'Ivieron', 'Pluma', 'Sparchu', 'Cindrill', 'Charmadillo', 'Finsta', 'Gulfin', 'Finiette', 'Atrox', 'Pouch', 'Draem', 'Larvea', 'Cleaf', 'Jacana', 'Friolera' ]

BattleGrounds = Literal[ 'ice', 'forest', 'sand' ]

BattleStates = Literal[ 'standby', 'ongoing', 'victory', 'defeat', 'back_to_world', 'defeated_enemy_dialog', 'evolution', 'evolution_ongoing', 'go_to_game_over' ]

Trainers = Literal['player', 'opponent']

Icons = Literal[ 'sword', 'shield', 'arrows', 'hand' ]

BattleMode  = Literal[ 'general', 'monster', 'attack', 'switch', 'target' ]

EvolutionSates = Literal[ 'display_current', 'display_evolution' ]

Sounds = Literal[ 'battle', 'evolution', 'fire', 'game_over', 'green', 'ice', 'notice', 'overworld', 'scratch', 'splash' ]

Elements = Literal[ 'fire', 'plant', 'normal', 'water' ]

GameOverStates = Literal[ 'undecided', 'play_again', 'quit' ]

DialogStates = Literal['standby', 'noticed_player', 'player_turns', 'go_to_player', 'talk']

Pos = tuple[ float, float ]

T = TypeVar('T')

class LazyDict ( dict[ str, T | Callable[[], T] ], Generic[T] ):
	def __getitem__(self, key: str) -> T:
		value = super().__getitem__(key)
		if callable(value): 
			func = cast(Callable[[], T], value)
			return func()
		return value

class Size ( TypedDict ):
	width: float
	height: float

class Menu ( TypedDict ):
	pos: Vector2
	icon: Icons

class Colors ( TypedDict ):
	bg: ColorLike
	text: ColorLike
	bg_selected: ColorLike
	text_selected: ColorLike

class GameOverOptions ( TypedDict ):
	text: str
	state: GameOverStates