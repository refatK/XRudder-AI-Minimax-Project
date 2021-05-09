import numpy as np
from error import Error
from players.player import PlayerOutOfTokensError


class BoardOutOfBoundError(Error):
    def __init__(self):
        msg = 'ERROR: The coordinate you entered is beyond the bounds of the board. Try again.'
        super().__init__(msg)


class BoardAlreadyOccupiedError(Error):
    def __init__(self, num):
        msg = f'ERROR: The coordinate you entered is already occupied by Player {num}. Try again.'
        super().__init__(msg)


class BoardNotPlayerTokenError(Error):
    def __init__(self, num):
        msg = 'ERROR: There is no token in that location for you to move. Try again.'
        if num > 0:
            msg = f"ERROR: You cannot move Player {num}'s token. Try again."

        super().__init__(msg)


class BoardInvalidMoveError(Error):
    def __init__(self):
        msg = 'ERROR: The token must be moved by one space in any of the eight directions. You cannot keep it\n' \
              'where it is and you can not move it any further around the board. Try again.'
        super().__init__(msg)


def move_is_valid(x1, y1, x2, y2):
    # can't move to same position
    if x1 == x2 and y1 == y2:
        return False
    # movement is only +- 1 at most in either x or y direction
    return (x1 - 1 <= x2 <= x1 + 1) and (y1 - 1 <= y2 <= y1 + 1)


# takes x, y coordinate and prints it in the boards format
def coord_to_string(x, y):
    letter_a_as_int = 65
    x_coord_as_letter = chr(letter_a_as_int + x - 1)
    return f'{x_coord_as_letter}{y}'


class Board:
    DEFAULT_BOARD_WIDTH = 12
    DEFAULT_BOARD_HEIGHT = 10

    # There is no players 0, so 0 in the Matrix implies an open space
    OPEN_SPACE = 0

    def __init__(self, width=DEFAULT_BOARD_WIDTH, height=DEFAULT_BOARD_HEIGHT, board=None):
        if board is None:
            self._width = width
            self._height = height
            # create the board as 2d Matrix
            self._board = np.zeros((width, height), dtype=int)
        else:
            self._width = board.width
            self._height = board.height
            self._board = board.np_board.copy()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def np_board(self):
        return self._board

    def coordinates_not_in_bounds(self, x, y):
        return x < 1 or x > self._width or y < 1 or y > self._height

    def coordinate_already_occupied(self, x, y):
        return self._board[x - 1][y - 1] > 0

    def is_players_token(self, player, x, y):
        return self._board[x - 1][y - 1] == player.number

    # compute players adding a token and check all possible errors
    def add_token_to_board(self, player, x, y):
        if self.coordinates_not_in_bounds(x, y):
            raise BoardOutOfBoundError
        if self.coordinate_already_occupied(x, y):
            raise BoardAlreadyOccupiedError(self._board[x - 1][y - 1])
        if not player.has_tokens():
            raise PlayerOutOfTokensError

        # place players token on board and reduce their token count
        self._board[x - 1][y - 1] = player.number
        player.use_token((x, y))

    # compute players moving a token and check all possible errors
    def move_token_on_board(self, player, x1, y1, x2, y2):
        if self.coordinates_not_in_bounds(x1, y1) or self.coordinates_not_in_bounds(x2, y2):
            raise BoardOutOfBoundError
        if not self.is_players_token(player, x1, y1):
            raise BoardNotPlayerTokenError(self._board[x1 - 1][y1 - 1])
        if self.coordinate_already_occupied(x2, y2):
            raise BoardAlreadyOccupiedError(self._board[x2 - 1][y2 - 1])
        if not move_is_valid(x1, y1, x2, y2):
            raise BoardInvalidMoveError

        # open the original position and take new position
        self._board[x1 - 1][y1 - 1] = Board.OPEN_SPACE
        self._board[x2 - 1][y2 - 1] = player.number
        player.update_moved_token(x1, y1, x2, y2)

    # used to visualize the board in command line
    def print_board(self, players):
        result = ''
        # show board
        for y in range(self._height):
            # got string formatting from here: https://stackoverflow.com/questions/8450472
            # number label
            row = '{0: <2}  |'.format(str(y + 1))
            # the board itself
            for x in range(self._width):
                if self._board[x][y] == 0:
                    row += '   |'
                else:
                    row += f' {players[self._board[x][y] - 1].icon} |'
            result = f'{row}\n' \
                     f'{result}'
        # add letters
        result += '      '
        letter_a_as_int = 65
        for i in range(self._width):
            result += chr(i + letter_a_as_int) + '   '
        print(result)

    def get_player_num_in_coord(self, x, y):
        if self.coordinates_not_in_bounds(x, y):
            raise BoardOutOfBoundError
        return self._board[x - 1][y - 1]

    def there_is_an_x_at(self, x, y):
        num = self._board[x][y]
        top_left = self._board[x - 1][y + 1]
        top_right = self._board[x + 1][y + 1]
        bottom_left = self._board[x - 1][y - 1]
        bottom_right = self._board[x + 1][y - 1]
        for coord in [top_left, top_right, bottom_left, bottom_right]:
            if coord != num:
                return False
        # if loop passed, there's an x
        return True

    def x_is_strikethroughed(self, x, y):
        num = self._board[x][y]
        left = self._board[x - 1][y]
        right = self._board[x + 1][y]
        return left > 0 and left != num and right > 0 and right != num

    def there_is_win_at_using_coords(self, x, y):
        try:
            num = self.get_player_num_in_coord(x, y)

            left = self.get_player_num_in_coord(x - 1, y)
            right = self.get_player_num_in_coord(x + 1, y)
            if left > 0 and left != num and right > 0 and right != num:
                return False

            top_left = self.get_player_num_in_coord(x - 1, y + 1)
            top_right = self.get_player_num_in_coord(x + 1, y + 1)
            bottom_left = self.get_player_num_in_coord(x - 1, y - 1)
            bottom_right = self.get_player_num_in_coord(x + 1, y - 1)
            for coord in [top_left, top_right, bottom_left, bottom_right]:
                if coord != num:
                    return False
            return True
        except BoardOutOfBoundError as e:
            return False

    def check_if_someone_won_using_tokens(self, coords):
        winner_set = set()
        for c in coords:
            if self.there_is_win_at_using_coords(c[0], c[1]):
                winner_set.add(self._board[c[0] - 1][c[1] - 1])
        return winner_set

    def check_if_someone_won(self):
        winner_set = set()
        # Note: we ignore the edges since an X shape can not be made with them as the center
        for y in range(1, self._height - 1):
            for x in range(1, self._width - 1):
                if self._board[x][y] > 0:
                    if self.there_is_an_x_at(x, y) and (not self.x_is_strikethroughed(x, y)):
                        # save players number
                        winner_set.add(self._board[x][y])
        # no one won yet
        return winner_set

    def copy(self):
        return Board(board=self)

    def is_full(self):
        return len(np.where(self._board != 0)[0]) == 0

    def token_is_lonely(self, x, y):
        surround = 0
        for xi in range(x - 1, x + 2):
            for yi in range(y - 1, y + 2):
                if not self.coordinates_not_in_bounds(xi, yi) and self.coordinate_already_occupied(xi, yi):
                    surround += 1
        if surround > 0:
            return False
        return True

    def win_strat_found(self, num):
        score = self.found_h_win_strat(num)
        return score

    def found_h_win_strat(self, num):
        score = 0
        for y in range(0, self._height - 3):
            for x in range(0, self._width - 5):
                if self._board[x][y] == num and self._board[x + 2][y] == num and self._board[x + 4][y] == num:
                    score += 5000
                    if self._board[x + 1][y + 1] == num and self._board[x + 3][y + 1] == num:
                        score += 20000
                        if self._board[x + 2][y + 2] == num:
                            score += 999999
                    elif self._board[x + 1][y + 1] == num or self._board[x + 3][y + 1] == num:
                        score += 80000
                elif self._board[x][y] == num and self._board[x + 2][y] == num:
                    score += 1000
                elif self._board[x + 2][y] == num and self._board[x + 4][y] == num:
                    score += 1000
        return score
