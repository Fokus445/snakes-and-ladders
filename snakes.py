from pyllist import dllist
import csv
import pygame
import sys
import random
import time
from button import Button

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


class Tiles:
	def __init__(self):
		self.tiles = dllist()
		self._csv_to_tiles()
		self._order_tiles()


	def _csv_to_tiles(self):
		with open("struktura.csv") as file:
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

			self.tiles = tiles

	def _order_tiles(self):
			line_count=0
			column_count=0

			for tile in reversed(self.tiles):
				if line_count % 2 == 0:
					tile['cordinates'] = [40+column_count*45,40+line_count*45]
					column_count=column_count+1
				else:
					tile['cordinates'] = [40+(9-column_count)*45,40+line_count*45]
					column_count=column_count+1

				if column_count==10:
					line_count=line_count+1
					column_count=0

	def _add_tile(self, pos):
		self.tiles.insert({
			"position":pos+1,
			"players_on_tile":[],
			"on_step_move_to":0,
			"cordinates":[],
		},self.tiles.nodeat(pos))

	def _delete_tile(self,pos):
		self.tiles.remove(self.tiles.nodeat(int(pos)))

	def _clear_tiles(self):
		while self.tiles:
			self.tiles.pop()

	def _add_snakes_and_ladders(self, pos1, pos2, rand=False):
		if rand==False:
			self.tiles[pos1+1]['on_step_move_to'] = self.tiles[pos2+1]['position']
		else:
			for i in range(1,int(len(self.tiles)/6)):
				self.tiles[random.randint(3,len(self.tiles)-5)]['on_step_move_to'] = random.randint(3,len(self.tiles)-2)



BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)



class SnakesAndLadders:
	"""Overall class to manage game assets and behavior"""
	def __init__(self):
		""" Initialize the game board and set its starting point."""
		self.tileClass = Tiles()
		pygame.init()



		self.tiles = self.tileClass.tiles


		self.number_of_players = int(input("Enter number of players: "))


		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_width, 
			self.settings.screen_height))

		self.font = pygame.font.SysFont('Arial', 15)

		# Make the Play button.
		self.play_button = Button(self, "Play")
		self.dice_button = Button(self, "Roll the Dice",dice=True)

		self.rolling_dice = False
		self.number_rolled = 0

		if self.number_of_players==2:
			self.player1_position = 0
			self.player2_position = 0
			self.player_turn = random.randint(1,2)	
		else:
			self.player1_position = 0
			self.player2_position = 0
			self.player3_position = 0
			self.player_turn = random.randint(1,3)

		self.game_active = False
		self.game_won = False

		



	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			self._check_events()

			self.screen.fill((255, 255, 255))
			
			if not self.game_active:
				self.play_button.draw_button()
				print("--------TILE MENU---------")
				print("1. ADD NEW TILE ")
				print("2. DELETE TILE AT POSTION X ")
				print("3. DELETE ALL TILES ")
				print("4. CONTINUE")

				
				choice = input("ENTER CHOICE: ")
				if choice == '1':
					pos = int(input("Where to insert tile (position): "))
					self.tileClass_add_tile(pos)
					self.tileClass_order_tiles()
				elif choice == '2':
					pos = int(input("Where to DELETE tile (position): "))
					self.tileClass_delete_tile(pos-1)
					self.tileClass_order_tiles()
				elif choice == '3':
					self.tileClass_clear_tiles()
				else:
					pass
				self._draw_tiles()



			if self.game_active:

				self.screen.fill((255, 255, 255))

				if self.player_turn == 1:
					pygame.draw.circle(self.screen, RED , (800,230),50)
				if self.player_turn == 2:
					pygame.draw.circle(self.screen, GREEN, (800,230), 50)
				if self.player_turn == 3:
					pygame.draw.circle(self.screen, BLACK , (800,230), 50)
				self.dice_button.draw_button()

				self._draw_tiles()


				self._update_players()

			pygame.display.flip()



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


	def _update_players(self):
		if self.number_of_players == 2:
			if self.player1_position == 0:
				pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]-30,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
			else:
				pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]+20,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
			if self.player2_position == 0:
				pygame.draw.circle(self.screen, GREEN, (self.tiles[self.player2_position]['cordinates'][0]-30,self.tiles[self.player2_position]['cordinates'][1]+10), 5)
			else:
				pygame.draw.circle(self.screen, GREEN, (self.tiles[self.player2_position]['cordinates'][0]+20,self.tiles[self.player2_position]['cordinates'][1]+10), 5)
		
		if self.number_of_players ==3:
			if self.player1_position == 0:
				pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]-30,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
			else:
				pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]+20,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
			if self.player2_position == 0:
				pygame.draw.circle(self.screen, GREEN, (self.tiles[self.player2_position]['cordinates'][0]-30,self.tiles[self.player2_position]['cordinates'][1]+10), 5)
			else:
				pygame.draw.circle(self.screen, GREEN, (self.tiles[self.player2_position]['cordinates'][0]+20,self.tiles[self.player2_position]['cordinates'][1]+10), 5)
			if self.player3_position == 0:
				pygame.draw.circle(self.screen, BLACK, (self.tiles[self.player3_position]['cordinates'][0]-30,self.tiles[self.player3_position]['cordinates'][1]+30), 5)
			else:
				pygame.draw.circle(self.screen, BLACK, (self.tiles[self.player3_position]['cordinates'][0]+20,self.tiles[self.player3_position]['cordinates'][1]+30), 5)

		if self.rolling_dice==True:
			if self.number_rolled!=0:

				if self.player_turn == 1:
					self.player1_position=self.player1_position+self.number_rolled
					if self.player1_position >= len(self.tiles):
						self.player1_positon = len(self.tiles)-1
						print("RED WON! GAME STOPS")
						self.game_won = True
					elif self.tiles[self.player1_position]['on_step_move_to'] != 0:
						print(f"MOVING RED TO {self.tiles[self.player1_position]['on_step_move_to']}")
						self.player1_position = self.tiles[self.player1_position]['on_step_move_to']-1

				elif self.player_turn == 2:
					self.player2_position=self.player2_position+self.number_rolled
					if self.player1_position >= len(self.tiles):
						self.player2_positon = len(self.tiles)-1
						print("GREEN WON! GAME STOPS")
						self.game_won = True
					elif self.tiles[self.player2_position]['on_step_move_to'] != 0:
						print(f"MOVING GREEN TO {self.tiles[self.player2_position]['on_step_move_to']}")
						self.player2_position = self.tiles[self.player2_position]['on_step_move_to']-1
				elif self.player_turn == 3:

					self.player3_position=self.player3_position+self.number_rolled
					if self.player3_position >= len(self.tiles):
						self.player3_positon = len(self.tiles)-1
						print("BLACK WON! GAME STOPS")
						self.game_won = True
					elif self.tiles[self.player3_position]['on_step_move_to'] != 0: 
						print(f"MOVING BLACK TO {self.tiles[self.player3_position]['on_step_move_to']}")
						self.player3_position = self.tiles[self.player3_position]['on_step_move_to']-1

				self.player_turn=self.player_turn+1
				if self.player_turn>self.number_of_players:
					self.player_turn=1
				self.rolling_dice=False

	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
				if self.game_won == False:
					self._check_dice_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.game_active:
			self.game_active = True

	def _check_dice_button(self, mouse_pos):
		button_clicked = self.dice_button.rect.collidepoint(mouse_pos)
		if button_clicked:
			self._roll_the_dice()

	def _roll_the_dice(self):
		self.rolling_dice = True
		self.number_rolled = random.randint(1,6)
		print(f"Number rolled: {self.number_rolled}")

	def _delete_tile(self,pos):
		self.tiles.remove(self.tiles.nodeat(pos))

	def _clear_tiles(self):
		while self.tiles:
			self.tiles.popleft()


if __name__ == '__main__':
	# Make a game instance, and run the game.
	sal = SnakesAndLadders()
	sal.run_game()
