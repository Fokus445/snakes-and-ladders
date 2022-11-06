from pyllist import dllist
import csv
import pygame
import sys
import random

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
				row = reversed(row)
			for i in row:
				tiles.appendleft({
					"position":int(i),
					"players_on_tile":[],
					"on_step_move_to":0,
					"cordinates":[],
				})
				column_count=column_count+1
			
			if column_count==10:
				line_count=line_count+1
				column_count=0

		tile_count=0
		line_count=0

		for tile in tiles:
			if line_count % 2 or line_count==0:
				tile['cordinates'] = [40+column_count*45,40+line_count*45]
			else:
				tile['cordinates'] = [40+(10-column_count)*45,40+line_count*45]
			
			column_count=column_count+1
			tile['position'] = len(tiles)-tile_count
			
			if column_count==10:
				line_count=line_count+1
				column_count=0

			tile_count=tile_count+1
	

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
		self.font = pygame.font.SysFont('Arial', 25)


	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
		
			self.screen.fill((255, 255, 255))
			


			TILE_COLOR = (233,233,233)


			

			for tile in self.tiles:

				if tile['on_step_move_to'] != 0:
					if tile['on_step_move_to']>tile['position']:
						TILE_COLOR = (0,204,0)
					elif tile['on_step_move_to']<tile['position']:
						TILE_COLOR = (204,0,0)


				pygame.draw.rect(self.screen, TILE_COLOR, 
					(tile['cordinates'][0],tile['cordinates'][1], 40,40))

				self.screen.blit(self.font.render(str(tile['position']), True, (50,50,50)), (tile['cordinates'][0],tile['cordinates'][1]))

			pygame.display.flip()



	def add_snakes_and_ladders(self):
		for i in range(1,int(len(self.tiles)/6)):
			self.tiles[random.randint(3,len(self.tiles)-5)]['on_step_move_to'] = random.randint(3,len(self.tiles)-2)

if __name__ == '__main__':
	# Make a game instance, and run the game.
	sal = SnakesAndLadders()
	sal.add_snakes_and_ladders()
	sal.run_game()
