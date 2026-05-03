from settings import *
from utils.Helper import required
from utils.MonsterManager import MonsterManager
from utils.Types import MonsterNames

class Battle:
	def __init__( self, battle_ground: Surface, monster_manager: MonsterManager, opponent_monsters: dict[int, tuple[MonsterNames, int]] ) -> None:
		
		self.MM = monster_manager
		self.battle_ground_surface = battle_ground
		self.battle_ground_rect = self.battle_ground_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		self.canvas = required(pygame.display.get_surface())

		self.monsters = { 
			'player': self.MM.get_player_battle_monsters(), 
			'opponent': self.MM.get_opponent_battle_monsters(opponent_monsters) 
		}


	def __draw_battle_ground ( self ):
		self.canvas.blit(self.battle_ground_surface, self.battle_ground_rect)

	def update ( self, dt: float ):
		self.__draw_battle_ground()