# Snake and Ladders Game

Welcome to the Snake and Ladders game! This project is implemented in Python using the Pygame library. It simulates the classic board game of Snake and Ladders, where players roll a dice and move their tokens according to the number they get on the dice.

The game utilizes a double linked list data structure to represent the game board. Each node in the list corresponds to a tile on the game board. These tiles store various attributes:

1. Position: An integer value indicating the position of the tile on the game board.

2. Players_on_tile: A list that stores references to the players currently occupying the tile. This allows for tracking which players are present on each tile.

3. On_step_move_to: An integer value indicating if the tile has a special feature like a snake or a ladder. If a player lands on a tile with a snake or a ladder, they are moved to the position specified by this value.

4. Coordinates: A list containing coordinates or other data necessary for displaying the tile on the game board UI.

By using a double linked list, the game can efficiently navigate between tiles in both forward and backward directions. This data structure allows for easy traversal of the game board and facilitates the implementation of game logic such as player movement, checking for special tile features like snakes and ladders, and updating the positions of players accordingly. Additionally, the inclusion of player lists on each tile enables the game to manage player positioning and interactions effectively.

![Screenshot](img/play.png)

## Installation

    pip install pygame

Run the game:

    python main.py

## How to Play

Upon running the game, you will be presented with a menu where you can customize the game settings and board layout.
Use the menu options to add or remove tiles, add snakes and ladders, and order positions according to your preference.

![Screenshot](img/settings.png)

Once you're satisfied with the settings, start the game from the menu.
Roll the dice by clicking the "Roll the Dice" button.
Your color token automatically moves according to the number rolled on the dice.
The game will switch turns between players, whose turn colored circle will show under the dice.
Continue rolling the dice and moving your colored token until one player reaches the end of the board and wins the game.

## Customization

You can customize various aspects of the game, including the board layout and the number of players. Here are some customization options available:

Add or remove tiles at specific positions on the board.
Add snakes and ladders to create shortcuts or obstacles for the players.
Order positions to arrange the tiles in a specific sequence.
Adjust the number of players participating in the game.

## Credits

This Snake and Ladders game project was created as my Algorithms and Data Structures university module assigment. It utilizes the Pygame library for graphics and user interface.

Feel free to contribute to this project by submitting bug fixes, feature enhancements, or feedback through issues and pull requests.

Enjoy playing Snake and Ladders! 🎲🐍🪜
