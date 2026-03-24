from settings import *
from entities.Entity import Entity
from utils.Types import States

class Character ( Entity ):
	def __init__(self, state: States, frames: dict[str, list[Surface]], pos: tuple[float, float], *groups: Group) -> None:
		super().__init__(frames, pos, *groups)

		self.state = state