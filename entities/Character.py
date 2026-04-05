from pygame import Vector2
from entities.Player import Player
from settings import *
from entities.Entity import Entity
from utils.Helper import is_dialog_possible, turn_toward
from utils.Types import States

class Character ( Entity ):
	def __init__(self, player: Player, state: States, frames: dict[str, list[Surface]], pos: tuple[float, float], datas: dict, radius: int, *groups: Group) -> None:
		super().__init__('character', frames, pos, *groups)

		self.player = player
		self.state = state
		self.datas = datas
		self.radius = radius

		self.is_mobile = False
		self.walk_hitbox = self.rect.inflate(10, 10)

	def __raycast ( self ):
		if not is_dialog_possible(self, self.player, self.radius): return None
		self.__player_stop_and_turn()
		self.__go_to_player()
		self.__stop_at_player()

	def __player_stop_and_turn ( self ):
		turn_toward(self.player, self)
		self.player.stop()

	def __go_to_player (self):
		self.unblock()
		self.direction = (Vector2(self.player.rect.center) - Vector2(self.rect.center)).normalize()

	def __stop_at_player ( self ):
		self.walk_hitbox.center = self.rect.center
		if self.player.hitbox.colliderect(self.walk_hitbox): self.stop()

	def update ( self, dt: float ):
		if self.is_mobile:
			self._set_direction()
			self._set_state()
			self._move(dt)
		self._animate(dt)
		self.__raycast()
