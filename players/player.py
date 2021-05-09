from error import Error


class PlayerOutOfTokensError(Error):
    def __init__(self):
        msg = 'ERROR: You have no more tokens left to add to the board. Please move a token instead.'
        super().__init__(msg)


class PlayerOutOfMovesAndTokensError(Error):
    def __init__(self):
        msg = 'You have no tokens to add or moves available. Therefore your turn will be skipped!'
        super().__init__(msg)


class Player:
    DEFAULT_INITIAL_TOKEN_COUNT = 15

    def __init__(self, number, icon, num_tokens=DEFAULT_INITIAL_TOKEN_COUNT, used_tokens=None):
        if used_tokens is None:
            used_tokens = []

        self._number = number
        self._icon = icon
        self._tokens_left = num_tokens
        self._used_tokens = used_tokens

    @property
    def number(self):
        return self._number

    @property
    def icon(self):
        return self._icon

    @property
    def tokens_left(self):
        return self._tokens_left

    @property
    def used_tokens(self):
        return self._used_tokens

    def has_tokens(self):
        return self._tokens_left > 0

    def use_token(self, coord):
        self._tokens_left -= 1
        self._used_tokens.append(coord)

    def update_moved_token(self, x1, y1, x2, y2):
        self._used_tokens.remove((x1, y1))
        self._used_tokens.append((x2, y2))

    def copy(self):
        return Player(self._number, self._icon, self._tokens_left, self._used_tokens.copy())

    def get_label(self):
        pass

    # returns
    # x, y, None, None for add_token
    # x1, y1, x2, y2 for move_token from (x1, y1) to (x2, y2)
    def get_coordinates(self):
        pass
