from settings import *
from pygame import Font

from entities.Player import Player
from gameobj.Battle import Battle
from utils.MonsterManager import MonsterManager
from utils.Helper import images_loader_dict
from utils.MyGroup import MyGroup
from utils.Types import FontTypes, MonsterNames

class BattleManager:
	def __init__( self, player: Player, monster_manager: MonsterManager, fonts: dict[FontTypes, Font], ui_images: dict[str, Surface], *groups: MyGroup ) -> None:
		self.player = player
		self.MM = monster_manager
		self.fonts = fonts
		self.ui_images = ui_images
		self.groups = groups

		self.battle_grounds = images_loader_dict('assets', 'graphics', 'backgrounds')
		self.battle = None


	def start_battle ( self, battle_ground: Surface, opponent_monsters: dict[int, tuple[MonsterNames, int]] ):
		self.battle = Battle( self.battle_grounds[battle_ground], self.MM, self.fonts, self.ui_images, opponent_monsters, *self.groups )


	def update ( self, dt: float ):
		if not self.battle: return
		self.battle.update(dt)