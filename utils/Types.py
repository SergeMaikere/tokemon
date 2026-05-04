
from typing import Literal, TypedDict

class Size ( TypedDict ):
	width: float
	height: float

States = Literal[ 'down', 'left', 'right', 'up' ]

Coasts = Literal[ 'grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i' ]

Biomes = Literal[ 'grass', 'grass_ice', 'sand' ]

TransitionState = Literal[ 'check_collision', 'fade_to_black', 'load_map', 'fade_to_light', 'done' ]

FontTypes = Literal[ 'regular', 'small', 'bold', 'dialog' ]

Attacks = Literal[ 'burn', 'heal', 'battlecry', 'spark', 'scratch', 'splash', 'fire', 'explosion', 'annihilate', 'ice' ]

MonsterNames = Literal[ 'Plumette', 'Ivieron', 'Pluma', 'Sparchu', 'Cindrill', 'Charmadillo', 'Finsta', 'Gulfin', 'Finiette', 'Atrox', 'Pouch', 'Draem', 'Larvea', 'Cleaf', 'Jacana', 'Friolera' ]

BattleGrounds = Literal[ 'ice', 'forest', 'sand' ]

Trainers = Literal['player', 'opponent']