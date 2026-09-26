from settings import *
from utils.Helper import sound_loader
from utils.Types import Attacks, Sounds



class MusicManager:


	@classmethod
	def init ( cls ):
		cls.audios = sound_loader('assets', 'audio')

	@classmethod
	def play (  cls, sound: Sounds ):
		return cls.audios[sound].play()

	@classmethod
	def play_in_loop (  cls, sound: Sounds ):
		return cls.audios[sound].play(-1)

	@classmethod
	def switch (  cls, sound_to_stop: Sounds, sound_to_play: Sounds, loops=-1 ):
		cls.audios[sound_to_stop].stop()
		cls.audios[sound_to_play].play(loops)

	@classmethod
	def play_attack ( cls, attack: Attacks ):
		match attack:
			case 'burn': cls.audios['fire'].play()
			case 'spark': cls.audios['fire'].play()
			case 'heal': cls.audios['green'].play()
			case 'battlecry': cls.audios['green'].play()
			case 'annihilate': cls.audios['explosion'].play()
			case _: cls.audios[attack].play()
			