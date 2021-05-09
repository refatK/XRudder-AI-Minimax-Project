from board import Board, coord_to_string
from players.aiPlayer import AiPlayer
from players.humanPlayer import HumanPlayer
from players.player import Player, PlayerOutOfMovesAndTokensError
from error import Error


class BoardNoMoreMovesError(Error):
    def __init__(self):
        msg = 'ERROR: All moves have been used up. Please add a token instead.'
        super().__init__(msg)


def print_welcome_banner():
    # Used http://patorjk.com/software/taag to generate banner
    s = '''\
┬  ┌─┐┌┬┐┌─┐  ┌─┐┬  ┌─┐┬ ┬
│  ├┤  │ └─┐  ├─┘│  ├─┤└┬┘
┴─┘└─┘ ┴ └─┘  ┴  ┴─┘┴ ┴ ┴                                

 o    o         .oPYo.             8      8              
 `b  d'         8   `8             8      8              
  `bd'         o8YooP' o    o .oPYo8 .oPYo8 .oPYo. oPYo. 
  .PY.   ooooo  8   `b 8    8 8    8 8    8 8oooo8 8  `' 
 .P  Y.         8    8 8    8 8    8 8    8 8.     8     
.P    Y.        8    8 `YooP' `YooP' `YooP' `Yooo' 8     
..::::..::::::::..:::..:.....::.....::.....::.....:..::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::
By: Refat Kamal ( 40028071 )
        '''
    print(s)


def print_error(err):
    print('\n\n==========\n'
          '[' + type(err).__name__ + ']:\n'
                                     '' + err.get_msg(), end='\n==========\n')


def print_skip_turn(err, player):
    print('\n\n==========\n'
          f"[SKIPPING PLAYER {player.number}'S TURN]:\n"
          + err.get_msg(), end='\n==========\n')


class XRudderGame:
    DEFAULT_STARTING_MOVES_LEFT = 30

    def __init__(self, board=Board(), players=None, starting_moves_left=DEFAULT_STARTING_MOVES_LEFT):
        self._board = board
        self._turn = 0
        self._moves_left = starting_moves_left
        self._is_complete = False
        self._prev_move_text = ''
                
        if players is not None:
            if isinstance(players[0], str):
                self._players = [AiPlayer(1, players[0], self), players[1]]
            elif isinstance(players[1], str):
                self._players = [players[0], AiPlayer(2, players[1], self)]
            else:
                self._players = players
        else:
            self._players = [AiPlayer(1, '■', self), AiPlayer(2, '□', self)]




    @property
    def moves_left(self):
        return self._moves_left

    @property
    def players(self):
        return self._players

    @property
    def board(self):
        return self._board

    def print_current_state(self, player):
        print('')
        self.print_game_board()
        if self._prev_move_text != '':
            print('CHANGE - ' + self._prev_move_text)

        print('\n> ' + player.get_label())
        print(f'It is Turn {self._turn}. There are [ {self._moves_left} TOKEN MOVES ] available:')

    def print_winner(self, player):
        print(f'\n\n{player.icon} {player.icon}  '
              f'WINNER IS PLAYER {player.number} after {self._turn} turns. Congrats, here is the final board!'
              f'  {player.icon} {player.icon}')
        print('***************************************')
        self.print_game_board()
        print('***************************************')

    def print_draw(self):
        print(f'\n\nSince no one has any moves left or tokens to add, the game is a DRAW! Here is the final board!')
        print('***************************************')
        self.print_game_board()
        print('***************************************')

    def print_game_board(self):
        self._board.print_board(self._players)

    def no_moves_left(self):
        return self._moves_left == 0

    # True if all players have no tokens to add or moves left to move their tokens
    def all_players_cannot_do_anything(self):
        if self._board.is_full():
            return True
        return all(not player.has_tokens() for player in self._players) and self.no_moves_left()

    # gets players input and updates board accordingly
    def play_turn(self, player):
        if not player.has_tokens() and self.no_moves_left():
            raise PlayerOutOfMovesAndTokensError

        x1, y1, x2, y2 = player.get_coordinates()

        # update board for players add token or move token
        if x2 is None and y2 is None:
            self._board.add_token_to_board(player, x1, y1)
            self._prev_move_text = f'{player.get_label()} added token at {coord_to_string(x1, y1)}' \
                                   f'\n****\n{coord_to_string(x1, y1)}\n****'
        else:
            if self.no_moves_left():
                raise BoardNoMoreMovesError
            self._board.move_token_on_board(player, x1, y1, x2, y2)
            self._moves_left -= 1
            self._prev_move_text = f'{player.get_label()} moved token from {coord_to_string(x1, y1)} to {coord_to_string(x2, y2)}' \
                                   f'\n****\n{coord_to_string(x1, y1)} {coord_to_string(x2, y2)}\n****'

    # The MAIN game loop, pulls everything together to allow players to play the game
    def play(self):
        print_welcome_banner()
        
        while not self._is_complete:
            self._turn += 1

            for player in self._players:
                successful_input = False
                while not successful_input:
                    self.print_current_state(player)

                    # issues can occur base on players input so handle and describe those cases to the players
                    try:
                        self.play_turn(player)
                    # if players is out of options, we have to skip them so they are not stuck doing the impossible
                    except PlayerOutOfMovesAndTokensError as no_options_err:
                        print_skip_turn(no_options_err, player)
                    # for other errors, players gets to try again
                    except Error as err:
                        print_error(err)
                        continue

                    successful_input = True

                # check for a winner
                potential_winners_set = self._board.check_if_someone_won()
                if bool(potential_winners_set):
                    if player.number in potential_winners_set:
                        self.print_winner(player)
                    else:
                        winner = self._players[potential_winners_set.pop() - 1]
                        self.print_winner(winner)
                    self._is_complete = True
                    break

            # if no one can do anything, end game as draw
            if self.all_players_cannot_do_anything():
                self.print_draw()
                self._is_complete = True
                break
