from pygame import Vector2
from entities.Character import Character
from gameobj.Dialog import Dialog
from settings import *
from entities.Player import Player
from utils.AllSprites import AllSprites
from utils.Timer import Timer

class DialogManager:
	def __init__ ( self, player: Player, characters: Group, all_sprites: AllSprites ):

		self.player = player
		self.characters = characters
		self.all_sprites = all_sprites

		self.timer = Timer(500)
		self.current_dialog = None
		

	def input ( self ):
			keys = pygame.key.get_just_pressed()
			if keys[pygame.K_SPACE]:
				for character in self.characters:
					if self.__is_dialog_possible(self.player, character):
						if self.current_dialog: 
							self.current_dialog.update()
						else:
							self.current_dialog = Dialog(character, self.finish_dialog, self.all_sprites)
						self.timer.start()

	def __is_player_facing_character_x ( self, player: Player, relation: Vector2 ):
		state = player.state
		if state == 'left' and relation.x < 0 or state == 'right' and relation.x > 0:
			return True

	def __is_player_facing_character_y ( self, player: Player, relation: Vector2 ):
		state = player.state
		if state == 'up' and relation.y < 0 or state == 'down' and relation.x > 0:
			return True

	def __is_dialog_possible ( self, player: Player, character: Character, radius: int = 100, tolerance: int = 30 ):
		relation = pygame.Vector2(character.rect.center) - pygame.Vector2(player.rect.center)
		if relation.length() <= radius:
			if abs(relation.y) < tolerance and self.__is_player_facing_character_x(player, relation) or \
			abs(relation.x) < tolerance and self.__is_player_facing_character_y(player, relation):
				return True

	def finish_dialog ( self, dialog: Dialog ):
		del dialog
		self.current_dialog = None

	def update ( self ):
		if not self.timer.running:
			self.input()
		self.timer.update()

