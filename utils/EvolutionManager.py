from entities.Player import Player
from settings import *
from utils.BattleManager import BattleManager
from utils.Helper import get_tinted_surface, required, tint
from utils.MyGroup import MyGroup

class EvolutionManager:
	def __init__( self, player: Player, battle_manager: BattleManager, player_monsters_sprites: MyGroup ) -> None:
		self.player = player
		self.BM = battle_manager
		self.player_monsters_sprites = player_monsters_sprites

		self.canvas = required(pygame.display.get_surface())
		self.tinted_surface = get_tinted_surface()


	def __check_for_evolution ( self ):
		return next( (sprite for sprite in self.player_monsters_sprites.sprites() if sprite.monster.evolve and sprite.monster.level == sprite.monster.evolve[1]), None )

	def __handle_evolution ( self ):
		evolving = self.__check_for_evolution()
		if evolving:
			tint(self.canvas, self.tinted_surface)
			if self.BM.battle: 
				self.BM.battle.freeze_all_monsters()
			else:
				self.player.block()

	
	def update ( self ):
		self.__handle_evolution()