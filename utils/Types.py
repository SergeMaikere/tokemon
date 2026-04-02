
from typing import Literal, TypedDict

class Size ( TypedDict ):
	width: float
	height: float

States = Literal[ 'down', 'left', 'right', 'up' ]

Coasts = Literal[ 'grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i' ]

Biomes = Literal[ 'grass', 'grass_ice', 'sand' ]
