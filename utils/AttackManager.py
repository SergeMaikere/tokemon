
from os.path import join

from gameobj.MonsterSprite import MonsterSprite
from settings import *
from gameobj.AnimatedSprite import AnimatedSprite
from utils.MonsterManager import MonsterManager
from utils.MyGroup import MyGroup
from utils.Helper import images_loader_dict, compose, cut
from utils.Types import Attacks


class AttackManager ( AnimatedSprite ):
	def __init__(self, monster_manager: MonsterManager, *groups: MyGroup) -> None:

		self.MM = monster_manager
		self.attack_frames = compose(
			images_loader_dict,
			lambda frames: { attack: [cut(image, 0, col, image.width/4, image.height) for col in range(4)] for attack, image in frames.items() }
		)( join('assets', 'graphics', 'attacks') )

		super().__init__('attack_animation', BATTLE_LAYERS['effects'], self.attack_frames['explosion'], *groups, topleft=(0,0))


	def animate_attack ( self, attacker: MonsterSprite, target: MonsterSprite, attack: Attacks ):
		self.frames = self.attack_frames[attack]
		self.rect = self.image.get_frect(center=target.rect.center)

