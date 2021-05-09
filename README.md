# XRudder Ai Game with Minimax and Heuristic Analysis

- [Project Summary](#Project-Summary)
- [Running The Game](#Running-The-Game)
- [How To Play](#How-To-Play)
  - [Winning The Game](#Winning-The-Game)
  - [Player Actions](#Player-Actions)
  - [Rules](#Rules)

---

## Project Summary

This project invloves the implementation of a simple 2-player, zero-sum game with an AI implementation predicated on the Minimax algorithim along with heuristic analysis for the AI's method of determining the best move it can make based on the current game state. The AI is built on the premise that the opponent will also try to make the most optimal moves possible and optimizations were made to allow the AI to make deeper analysis within the Minimax tree while also trying to maintain a fast as possible calculation.

## Running The Game

1. Clone the repo locally using Git.
2. Open Command Line and nagivate to the project folder (folder that contains the file `xrudder.py`).
3. Run the game using `python xrudder.py` in Command Line.

### Note

- If you get an error stating that "numpy module is not found", you will need to install this dependency. You can use `pip install numpy` to do this.
- You can use an IDE or Anaconda Prompt to run the game script instead if preferred.

## How To Play

The game "XRudder" is similar to Tic-Tac-Toe in which 2 player add tokens to a grid and the winner is the one who can get there tokens to match a specific configuration first. In Tic-Tac-Toe that invloves having tokens that are in a row, column, or diagonol of 3, while in XRudder this involves having the tokens in an "X shape".

### Winning The Game

To win the game the player must get their token to match an "X shape" before their opponent does. The "X Shape" must also be made without it being "crossed out" by the opponent's tokens. If neither player is able to reach this by the end of the game, the game results in a tie. Here is an example of a winning state:

![Example where player 1 is the winner.](https://user-images.githubusercontent.com/31963426/117557842-5fb71c80-b045-11eb-82ae-770542d26002.png)

*In this example player 1 with "■" tokens has won by making the "X shape"*.

![Example where player 1 creates an X shappe that is crossed out so they haven't won.](https://user-images.githubusercontent.com/31963426/117558531-58474180-b04c-11eb-8662-59b50d1d7496.png)

*In this example player 1 with "■" tokens has made the "X shape", but player 2 is "crossing" it making the game continue*.

### Player Actions

Players have 2 possible actions they can take:

1. **Add token to the board:**
   - The player specifies the coordinate on the board they want to add the token to.
   - The player can only add a token to a unoccupied space (coordinate that doesn't contain any token).
   - If the player is out of tokens, they are not allowed to take this action.
   - **Example:**

   ![image](https://user-images.githubusercontent.com/31963426/117557977-c38e1500-b046-11eb-8c41-ff4a78d67877.png)
   
   *Player 1 adding a token to the coordinate C6 by inputting `C6`*

2. **Move token on board:**
   - The player can only move their own tokens.
   - The player specifies the coordinate of the token they want to move and the coordinate they want to move the token to.
   - The player can only move a token to an adjacent unoccupied space. This is any unoccupied space that is one space up, down, left, right or diagonol to the current position. This is similar to how a King piece is allowed to move in a game of chess.
   - If the game session is out of moves the player is not allowed to take this action.
   - **Example:**

   ![image](https://user-images.githubusercontent.com/31963426/117558069-9beb7c80-b047-11eb-95d7-4f0a2bf1d00c.png)
   
   *Player 1 moving a token from D4 to D3 by inputting `D4 D3`*

### Rules

- Each player starts with 15 tokens they can add to the board.
- Moving a token can only be done 30 times in total in a game session. This total is shared among both players.
- Player actions are subject to rules as decribed in the [Player Actions](#Player-Actions) section.
- A player wins by matching the conditions described in the [Winning The Game](#Winning-The-Game) section.
- If both players run out tokens to add or move, the game ends in a draw.

### AI Implementation Details

A PDF report was made for this project describing the startegies used when implementing the AI in terms of heuristics and optimizations, as well as it's results when playing against other AIs created by other students for the same project.

The report can be accessed [by clicking here](https://github.com/refatK/XRudder-AI-Minimax-Project/blob/main/Report%20and%20Analysis.pdf).
