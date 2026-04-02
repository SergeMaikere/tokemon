from settings import *
from pygame import Vector2
from entities.Character import Character
from gameobj.Dialog import Dialog
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
		

	def input ( self, dt: float ):
			keys = pygame.key.get_just_pressed()
			if keys[pygame.K_SPACE]:
				self.__update_current_dialog()
				self.__initiate_dialog()
				self.timer.start()

	def __update_current_dialog ( self ):
		if not self.current_dialog: return 
		self.current_dialog.update()

	def __initiate_dialog ( self ):
		if self.current_dialog: return
		for character in self.characters:
			if self.__is_dialog_possible(self.player, character):
				self.__set_character_direction(character)
				self.__create_dialog(character)
				self.__immobilize_player()

	def __is_dialog_possible ( self, player: Player, character: Character, radius: int = 100, tolerance: int = 30 ):
		relation = pygame.Vector2(character.rect.center) - pygame.Vector2(player.rect.center)
		if relation.length() <= radius:
			if abs(relation.y) < tolerance and self.__is_player_facing_character_x(player, relation) or \
			abs(relation.x) < tolerance and self.__is_player_facing_character_y(player, relation):
				return True

	def __is_player_facing_character_x ( self, player: Player, relation: Vector2 ):
		return (player.state == 'left' and relation.x < 0) or (player.state == 'right' and relation.x > 0)
			

	def __is_player_facing_character_y ( self, player: Player, relation: Vector2 ):
		return (player.state == 'up' and relation.y < 0) or (player.state == 'down' and relation.x > 0)
			

	def __set_character_direction ( self, character: Character ):
		if self.player.state == 'left': character.state = 'right'
		if self.player.state == 'right': character.state = 'left'
		if self.player.state == 'up': character.state = 'down'
		if self.player.state == 'down': character.state = 'up'
		return character
		

	def __create_dialog ( self, character: Character ):
		self.current_dialog = Dialog(character, self.finish_dialog, self.all_sprites)

	def __immobilize_player ( self ): self.player.is_mobile = False

	def finish_dialog ( self, dialog: Dialog ):
		del dialog
		self.current_dialog = None
		self.player.is_mobile = True

	def update ( self, dt: float ):
		if not self.timer.running: self.input(dt)
		self.timer.update()

