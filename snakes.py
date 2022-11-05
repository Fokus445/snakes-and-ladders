from pyllist import dllist
import csv
import pygame
import sys

class Settings:
	"""A class to store all settings for Snakes and Ladders"""
	def __init__(self):
		"""Initialize the game settings."""
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (133,133,133)


		#Dice settings
		self.dice_rolling_time = 3
	

def csv_to_dllist(file):
	with open("struktura.csv") as file:
		csv_reader = csv.reader(file, delimiter=",")
		linecount = 0
		lst = dllist()
		for row in csv_reader:
			if linecount % 2:
				[lst.appendleft(i) for i in reversed(row)]
			else:
				[lst.appendleft(i) for i in row]

			linecount=linecount+1
		return lst


BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

class SnakesAndLadders:
	"""Overall class to manage game assets and behavior"""
	def __init__(self):
		""" Initialize the game board and set its starting point."""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, 
			self.settings.screen_height))


	def run_game(self):
		"""Start the main loop for the game"""
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
		
			self.screen.fill((255, 255, 255))
			pygame.draw.rect(self.screen, (0, 0, 255), (250, 250), 75)
			pygame.display.flip()


if __name__ == '__main__':
	# Make a game instance, and run the game.
	sal = SnakesAndLadders()
	sal.run_game()
