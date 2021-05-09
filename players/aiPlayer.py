from ai.gamestate import GameState
from ai.minimax import get_move
from players.player import Player
from board import coord_to_string
import time


def bot_print(msg):
    print(f'BEEP BOOP: {msg}')


class AiPlayer(Player):
    def __init__(self, number, icon, game, num_tokens=Player.DEFAULT_INITIAL_TOKEN_COUNT):
        super().__init__(number, icon, num_tokens)
        self._game = game
        self.depth = 3

    def get_label(self):
        return f'Ai({self.number}):'

    # prompt for getting human players move
    def get_coordinates(self):
        # get state
        bot_print('COMPUTING...')

        p1 = self._game.players[0]
        p2 = self._game.players[1]
        if self._number == 1:
            players = (p1, p2)
        else:
            players = (p2, p1)

        state = GameState(self._game.board, self._game.moves_left, players)

        runtime = time.time()
        action = get_move(state, self.depth)
        runtime = time.time() - runtime
        bot_print(f'TOOK {runtime} SECONDS!!!')

        if runtime >= 4.2:
            self.depth = (self.depth - 1) if self.depth > 2 else 2
        if self.tokens_left == 0:
            self.depth = 2

        self.print_action(action)

        return action

    def print_action(self, action):
        x1, y1, x2, y2 = action
        if x2 is None:
            bot_print(f'ADDING TOKEN TO {coord_to_string(x1, y1)}')
        else:
            bot_print(f'MOVING TOKEN FROM {coord_to_string(x1, y1)} TO {coord_to_string(x2, y2)}')
