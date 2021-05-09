from error import Error
from players.player import Player


class PlayerInvalidInputError(Error):
    def __init__(self):
        msg = 'ERROR: The given input is invalid. Please make sure it is formatted correctly.'
        super().__init__(msg)


# verify string made of two coordinates, ex:'B10 C8'
def is_valid_move_input(user_input):
    coords = user_input.split()
    if len(coords) != 2:
        return False
    else:
        return is_valid_coordinate_input(coords[0]) and is_valid_coordinate_input(coords[1])


# takes letter ignoring cases and gets the corresponding number coordinate (ex: c -> 3)
def letter_to_coordinate(letter):
    letter_a_as_int = 65
    return ord(letter.upper()) - letter_a_as_int + 1


def parse_coordinate_from_input(user_input):
    x = letter_to_coordinate(user_input[0])
    y = int(user_input[1:])
    return x, y


# get's the x,y location of token to move and x,y location to move it to
def get_coordinate_for_move(user_input):
    coords = user_input.split()
    x1, y1 = parse_coordinate_from_input(coords[0])
    x2, y2 = parse_coordinate_from_input(coords[1])
    return x1, y1, x2, y2


# verify string made of one character and a number, ex:'D10'
def is_valid_coordinate_input(user_input):
    return user_input[0].isalpha() and user_input[1:].isdigit()


# get's the x,y location the players wants to add a token
def get_coordinate_for_add(user_input):
    x, y = parse_coordinate_from_input(user_input)
    return x, y, None, None


class HumanPlayer(Player):

    def __init__(self, number, icon, num_tokens=Player.DEFAULT_INITIAL_TOKEN_COUNT):
        super().__init__(number, icon, num_tokens)

    def get_label(self):
        return f'Human({self.number}):'

    # prompt for getting human players move
    def get_coordinates(self):
        res = input(f' | PLEASE ENTER A COORDINATE PLAYER {self._number} '
                    f'({self._tokens_left} {self.icon} token{"s" if self._tokens_left != 1 else ""} left to add):\n'
                    f' | examples: (Add token to C5: "C5") (Move token up from C5: "C5 C6")\n'
                    f'   :')

        if res == '':
            raise PlayerInvalidInputError

        if is_valid_coordinate_input(res):
            return get_coordinate_for_add(res)
        elif is_valid_move_input(res):
            return get_coordinate_for_move(res)
        else:
            raise PlayerInvalidInputError
