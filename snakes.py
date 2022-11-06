from pyllist import dllist
import csv
import pygame
import sys
import random
import time

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

		self.start_cordinates = [500,0]

	

def csv_to_tiles(src):
	with open(src) as file:
		csv_reader = csv.reader(file, delimiter=",")
		line_count = 0
		column_count = 0



		tiles = dllist()
		for row in csv_reader:
			if line_count % 2:
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

		
		line_count=0

		for tile in reversed(tiles):
			if line_count % 2 == 0:
				tile['cordinates'] = [40+column_count*45,40+line_count*45]
				column_count=column_count+1
			else:
				tile['cordinates'] = [40+(9-column_count)*45,40+line_count*45]
				column_count=column_count+1

			if column_count==10:
				line_count=line_count+1
				column_count=0
	

	return tiles


BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


class Player:
	def __init__(self):
		self.settings = Settings
		self.cordinates = self.settings.start_cordinates





class SnakesAndLadders:
	"""Overall class to manage game assets and behavior"""
	def __init__(self):
		""" Initialize the game board and set its starting point."""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, 
			self.settings.screen_height))

		self.tiles = csv_to_tiles("struktura.csv")
		self.font = pygame.font.SysFont('Arial', 15)
		self._add_snakes_and_ladders()




	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			self._check_events()

			self.screen.fill((255, 255, 255))


			self._draw_tiles()

			self._draw_players()

			pygame.display.flip()



	def _add_snakes_and_ladders(self):
		for i in range(1,int(len(self.tiles)/6)):
			self.tiles[random.randint(3,len(self.tiles)-5)]['on_step_move_to'] = random.randint(3,len(self.tiles)-2)

	def _draw_tiles(self):
		for tile in self.tiles:
			TILE_COLOR = (233,233,233)
			if tile['on_step_move_to'] != 0:
				if tile['on_step_move_to']>tile['position']:
					TILE_COLOR = (0,204,0)
				elif tile['on_step_move_to']<tile['position']:
					TILE_COLOR = (204,0,0)
			pygame.draw.rect(self.screen, TILE_COLOR, 
					(tile['cordinates'][0],tile['cordinates'][1], 40,40))

			self.screen.blit(self.font.render(str(tile['position']), True, (120,120,120)), (tile['cordinates'][0],tile['cordinates'][1]))
			if tile['on_step_move_to'] != 0:
				self.screen.blit(self.font.render(f"->{str(tile['on_step_move_to'])}", True, (0,0,0)), (tile['cordinates'][0]+10,tile['cordinates'][1]+20))

	def _draw_players(self):
		pygame.draw.circle(self.screen, BLACK, (20,450), 5)
		pygame.draw.circle(self.screen, RED, (20,470), 5)
		pygame.draw.circle(self.screen, GREEN, (20,490), 5)

	def _update_players(self):
		pass

	def _check_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


if __name__ == '__main__':
	# Make a game instance, and run the game.
	sal = SnakesAndLadders()
	sal.run_game()
