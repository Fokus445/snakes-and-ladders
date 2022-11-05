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
	

def csv_to_tiles(src):
	with open(src) as file:
		csv_reader = csv.reader(file, delimiter=",")
		line_count = 0
		column_count = 0
		tiles = dllist()
		for row in csv_reader:
			if line_count % 2 or line_count==0:
				[tiles.appendleft({
					"position":i,
					"players_on_tile":[],
					"on_step_move_to":False,
					"cordinates":[10+column_count*15,10+line_count*15],
					}) for i in reversed(row)]
				column_count=column_count+1



			else:
				[tiles.appendleft({
					"position":i,
					"players_on_tile":[],
					"on_step_move_to":False,
					"cordinates":[10+column_count*15,10+line_count*15],
					}) for i in row]
				column_count=column_count+1 
				print(column_count) 
			
			print(line_count) 
			if column_count==10:
				column_count=0
	

		return tiles


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

		self.tiles = csv_to_tiles("struktura.csv")


	def run_game(self):
		"""Start the main loop for the game"""
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
		
			self.screen.fill((255, 255, 255))
			
			i=0
			y=0
			for tile in self.tiles:
				pygame.draw.rect(self.screen, BLACK, 
					(tile['cordinates'][0],tile['cordinates'][1], 10,10))
				print(tile['cordinates'][0], tile['cordinates'][1])
				i=i+1
				if i==10:
					y=y+1
					i=0
			break

			pygame.display.flip()


if __name__ == '__main__':
	# Make a game instance, and run the game.
	sal = SnakesAndLadders()
	sal.run_game()
