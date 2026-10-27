from settings import *
from pygame import Vector2

from entities.Player import Player
from entities.Entity import Entity
from utils.DialogManager import DialogManager
from utils.Helper import set_truthy
from utils.MyGroup import MyGroup
from utils.Timer import Timer
from utils.Types import DialogStates, States
from utils.MusicManager import MusicManager as Music
from utils.DialogTools import is_dialog_possible, turn_toward_entity

class Character ( Entity ):
	def __init__(
			self, 
			player: Player, 
			state: States, 
			frames: dict[str, list[Surface]], 
			pos: tuple[float, float], 
			datas: dict, 
			radius: int, 
			dialog_manager: DialogManager,
			nurse: bool,
			*groups: MyGroup
		) -> None:

		super().__init__('character', frames, pos, *groups)

		self.player = player
		self.state = state
		self.datas = datas
		self.radius = radius
		self.dialog_manager = dialog_manager
		self.nurse = nurse

		self.collision_rects = self.__get_collisions_rects(groups)
		
		self.is_mobile = False
		self.walk_hitbox = self.hitbox.inflate(10, 10)

		self.can_look_around = len(self.datas['directions']) > 1
		self.turn_index = 0
		self.turn_timer = Timer(1500, self.__turn, autostart=True, loop=True)

		self.has_noticed_player = False
		self.noticed_timer = Timer(500, self.__player_is_noticed)

		self.dialog_state: DialogStates = 'standby'

	def set_dialog_state ( self, state: DialogStates ):
		self.dialog_state = state

	def __get_collisions_rects ( self, groups: tuple[MyGroup, ...] ):
		collision_sprites = next(group for group in groups if group.name == 'collision_sprites')
		return [ sprite.rect for sprite in collision_sprites if sprite is not self ]

	def __turn ( self ):
		self.turn_index = (self.turn_index + 1) % len(self.datas['directions'])
		self.state = self.datas['directions'][self.turn_index]

	def __look_around ( self ):
		if not self.datas['look_around'] or self.__is_still_talking() or self.is_mobile: return
		self.turn_timer.update()

	def __is_still_talking ( self ): return bool(self.dialog_manager.current_dialog)
	
	def __has_line_of_sight ( self ):
		if not self.__is_player_in_range(): return False
		collisions = [ bool(rect.clipline(self.rect.center, self.player.rect.center)) for rect in self.collision_rects ]
		return not any(collisions)
	
	def __is_player_in_range ( self ): return vector2(self.rect.center).distance_to(self.player.rect.center) < self.radius

	def __raycast ( self ):
		match self.dialog_state:
			case 'noticed_player': self.__notice_player()
			case 'player_turns': self.__player_stop_and_turn()
			case 'go_to_player': self.__go_to_player()
			case 'talk': self.__create_dialog()
			case 'standby':
				if self.__is_still_talking(): return 
				if not self.__has_line_of_sight(): return
				if not is_dialog_possible(self, self.player, self.radius): return 
				if self.has_noticed_player: return 
				self.set_dialog_state('noticed_player')


	def __player_is_noticed ( self ):
		self.player.set_is_noticed(False)
		self.set_dialog_state('player_turns')

	def __notice_player ( self ):
		if self.noticed_timer.running: return self.noticed_timer.update()
		self.player.set_is_noticed(True)
		self.player.block()
		self.noticed_timer.start()
		Music.play('notice')

	def __player_stop_and_turn ( self ):
		turn_toward_entity(self.player, self)
		self.player.block()
		self.set_dialog_state('go_to_player')

	def __go_to_player (self):
		if not self.is_mobile: self.unblock()
		self.direction = (Vector2(self.player.rect.center) - Vector2(self.rect.center)).normalize()
		self.walk_hitbox.center = self.rect.center
		if self.player.hitbox.colliderect(self.walk_hitbox): 
			self.block()
			self.set_dialog_state('talk')

		
	def __create_dialog ( self ):
		self.dialog_manager.current_character = self
		self.dialog_manager._create_dialog(self)
		set_truthy(self, 'has_noticed_player')
		self.set_dialog_state('standby')

	def update ( self, dt: float ):
		if self.is_mobile:
			self._set_direction()
			self._set_state()
			self._move(dt)
		self.__look_around()
		self._animate(dt)
		self.__raycast()
