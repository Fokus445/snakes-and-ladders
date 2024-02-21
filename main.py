import random
import sys

import pygame

from button import Button
from tiles import Tiles

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


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


class SnakesAndLadders:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """ Initialize the game board and set its starting point."""
        self.tileClass = Tiles()
        self.tiles = self.tileClass.tiles
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
            self.settings.screen_height))
        self.font = pygame.font.SysFont('Arial', 15)

        self.number_of_players = 0

        # Make the button.
        self.dice_button = Button(self, "Roll the Dice",700,300)
        self.restart_button = Button(self, "Back to Menu",700,600, color="red")

        self.rolling_dice = False
        self.number_rolled = 0
        self.player_color = ""


        self.player1_position = 0
        self.player2_position = 0
        self.player3_position = 0
        self.player_turn = 0


        self.game_active = False
        self.game_won = False

        dice1 = pygame.image.load("img/dice1.png")
        dice2 = pygame.image.load("img/dice2.png")
        dice3 = pygame.image.load("img/dice3.png")
        dice4 = pygame.image.load("img/dice4.png")
        dice5 = pygame.image.load("img/dice5.png")
        dice6 = pygame.image.load("img/dice6.png")
        self.dices = [dice1,dice2,dice3,dice4,dice5,dice6]

    # MENU
    def _game_setting(self):
        while True:
            self.screen.fill((255,255,255))
            self._check_events()
            self._draw_tiles()
            pygame.display.flip()

            
            print("--------TILE MENU---------")
            print("1. ADD NEW TILE ")
            print("2. DELETE TILE AT POSTION X ")
            print("3. DELETE ALL TILES ")
            print("4. Order positions")
            print("5. Continue to snakes and ladders menu")
            print("6. QUIT")


            choice = input("ENTER CHOICE: ")
            if choice == '1':
                pos = int(input("Where to insert tile (position): "))
                self.tileClass.add_tile(pos-1)
                self.tileClass.order_tiles()
                pygame.display.flip()
                continue
            elif choice == '2':
                pos = int(input("Where to DELETE tile (position): "))
                self.tileClass.delete_tile(pos-1)
                self.tileClass.order_tiles()
                self._draw_tiles()
                continue
            elif choice == '3':
                self.tileClass.clear_tiles()
                continue
            elif choice == '4':
                self.tileClass.order_positions()
                continue
            elif choice == '5':
                pass
            elif choice == '6':
                sys.exit()

            while True:
                self.screen.fill((255,255,255))
                self._check_events()
                self._draw_tiles()
                pygame.display.flip()

                print("-----------SNAKES AND LADDERS SETTINGS------------")
                print("1. Add snakes and ladders ")
                print("2. START THE GAME")
                print("3. QUIT")
                choice = input("ENTER CHOICE: ")


                if choice == '1':
                    pos1 = int(input("Where to add snakes or ladder (pos): "))
                    pos2 = int(input("To where (pos): "))
                    self.tileClass.add_snakes_and_ladders(pos1,pos2)
                    continue
                elif choice == '2':
                    break
                elif choice == '3':
                    sys.exit()
            break

        self.number_of_players = int(input("Enter number of players: "))
        self.player_turn = random.randint(1,self.number_of_players)
        self.player1_position = 0
        self.player2_position = 0
        self.player3_position = 0
        self.game_won = False
        self.game_active = True



    # Main game loop
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.screen.fill((255, 255, 255))
        
            if self.game_active == False:
                self._game_setting()
            else:
                self.screen.fill((255, 255, 255))
                if self.game_won==False:
                    if self.player_turn == 1:
                        pygame.draw.circle(self.screen, RED , (800,230),50)
                    if self.player_turn == 2:
                        pygame.draw.circle(self.screen, GREEN, (800,230), 50)
                    if self.player_turn == 3:
                        pygame.draw.circle(self.screen, BLACK , (800,230), 50)
                    self.dice_button.draw_button()
                    self._update_dice()
                self.restart_button.draw_button()
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
        if self.rolling_dice==True:
            if self.number_rolled!=0:
                if self.player_turn == 1:
                    old_pos = self.player1_position+1
                    self.player1_position=self.player1_position+self.number_rolled
                    if self.player1_position >= len(self.tiles)-1:
                        self.player1_position = len(self.tiles)-1
                        print("RED WON! GAME STOPS")
                        self.game_won = True
                    print(f"MOVING {self.player_color} player from {old_pos} to {self.player1_position+1}")
                    if self.tiles[self.player1_position]['on_step_move_to'] != 0:
                        print(f"MOVING RED TO {self.tiles[self.player1_position]['on_step_move_to']}")
                        self.player1_position = self.tiles[self.player1_position]['on_step_move_to']-1

                elif self.player_turn == 2:
                    old_pos = self.player2_position+1
                    self.player2_position=self.player2_position+self.number_rolled
                    if self.player2_position >= len(self.tiles)-1:
                        self.player2_position = len(self.tiles)-1
                        print("GREEN WON! GAME STOPS")
                        self.game_won = True
                    print(f"MOVING {self.player_color} player from {old_pos} to {self.player2_position+1}")
                    if self.tiles[self.player2_position]['on_step_move_to'] != 0:
                        print(f"MOVING GREEN TO {self.tiles[self.player2_position]['on_step_move_to']}")
                        self.player2_position = self.tiles[self.player2_position]['on_step_move_to']-1
                elif self.player_turn == 3:
                    old_pos = self.player3_position+1
                    self.player3_position=self.player3_position+self.number_rolled
                    if self.player3_position >= len(self.tiles)-1:
                        self.player3_position = len(self.tiles)-1
                        print("BLACK WON! GAME STOPS")
                        self.game_won = True
                    print(f"MOVING {self.player_color} player from {old_pos} to {self.player3_position+1}")
                    if self.tiles[self.player3_position]['on_step_move_to'] != 0: 
                        print(f"MOVING BLACK TO {self.tiles[self.player3_position]['on_step_move_to']}")
                        self.player3_position = self.tiles[self.player3_position]['on_step_move_to']-1

                self.player_turn=self.player_turn+1
                if self.player_turn>self.number_of_players:
                    self.player_turn=1
                self.rolling_dice=False

        if self.number_of_players == 1:
            if self.player1_position == 0:
                pygame.draw.circle(self.screen, RED, (650, 310), 5)
            else:
                pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]+20,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
        if self.number_of_players == 2:
            if self.player1_position == 0:
                pygame.draw.circle(self.screen, RED, (650, 310), 5)
            else:
                pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]+20,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
            if self.player2_position == 0:
                pygame.draw.circle(self.screen, GREEN, (650, 330), 5)
            else:
                pygame.draw.circle(self.screen, GREEN, (self.tiles[self.player2_position]['cordinates'][0]+20,self.tiles[self.player2_position]['cordinates'][1]+10), 5)
        if self.number_of_players ==3:
            if self.player1_position == 0:
                pygame.draw.circle(self.screen, RED, (650, 310), 5)
            else:
                pygame.draw.circle(self.screen, RED, (self.tiles[self.player1_position]['cordinates'][0]+20,self.tiles[self.player1_position]['cordinates'][1]+20), 5)
            if self.player2_position == 0:
                pygame.draw.circle(self.screen, GREEN, (650, 330), 5)
            else:
                pygame.draw.circle(self.screen, GREEN, (self.tiles[self.player2_position]['cordinates'][0]+20,self.tiles[self.player2_position]['cordinates'][1]+10), 5)
            if self.player3_position == 0:
                pygame.draw.circle(self.screen, BLACK, (650, 350), 5)
            else:
                pygame.draw.circle(self.screen, BLACK, (self.tiles[self.player3_position]['cordinates'][0]+20,self.tiles[self.player3_position]['cordinates'][1]+30), 5)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_dice_button(mouse_pos)
                self._check_restart_button(mouse_pos)

    def _check_restart_button(self, mouse_pos):
        button_clicked = self.restart_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.game_active = False

    def _update_dice(self):
        self.screen.blit(self.dices[self.number_rolled-1], (750, 50))

    def _check_dice_button(self, mouse_pos):
        if self.game_active:
            button_clicked = self.dice_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self._roll_the_dice()

    def _roll_the_dice(self):
        self.rolling_dice = True
        self.number_rolled = random.randint(1,6)
        if self.player_turn == 1:
            self.player_color = 'RED'
        elif self.player_turn == 2:
            self.player_color = 'GREEN'
        elif self.player_turn == 3:
            self.player_color = 'BLACK'
        print(f"Number rolled: {self.number_rolled} for player {self.player_color}")



if __name__ == '__main__':
    # Make a game instance, and run the game.
    sal = SnakesAndLadders()
    sal.run_game()