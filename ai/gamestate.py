import numpy as np
import random

from board import Board


class GameState:
    board: Board

    MAX_SCORE = 99999999999999
    MIN_SCORE = -99999999999999

    def __init__(self, board, moves_left, players):
        self.board = board
        self.moves_left = moves_left
        self.players = players

    @property
    def ai(self):
        return self.players[0]

    @property
    def opp(self):
        return self.players[1]

    def get_all_possible_actions(self, p_pos, is_ai):
        actions = []

        # if first move, just put token in center
        if not self.ai.used_tokens:
            base = [(6, 5, None, None)] if not self.out_of_bounds_or_occupied(6, 5) else [(3, 5, None, None)]
            return base

        # get possible add to boards (where board is empty)
        if self.players[p_pos].tokens_left > 0 and self.moves_left > 0:
            empty_coords = self.get_adds_in_token_diags_first()
            actions.extend(empty_coords)

        # get possible move on boards
        if (self.moves_left > 0 and not self.players[p_pos].has_tokens()) \
                or (is_ai and self.moves_left > 0 and self.players[p_pos].tokens_left <= 8):
            for coord in self.players[p_pos].used_tokens:
                x, y = coord
                # actions.extend(self.get_all_possible_moves(x, y))
                actions = self.get_all_possible_moves(x, y) + actions

        return actions

    def get_all_possible_adds(self):
        empty_spaces = np.where(self.board.np_board == 0)
        empty_coords = list(zip(*empty_spaces))
        empty_coords = [(c[0] + 1, c[1] + 1, None, None) for c in empty_coords if True]
        return empty_coords

    def get_adds_in_token_radius(self, radius):
        coords = set()
        used_tokens = self.ai.used_tokens + self.opp.used_tokens
        for c in used_tokens:
            for x in range(c[0] - radius, c[0] + radius + 1):
                for y in range(c[1] - radius, c[1] + radius + 1):
                    if not self.out_of_bounds_or_occupied(x, y) and not self.board.token_is_lonely(x, y):
                        coords.add((x, y, None, None))
        return coords

    def get_adds_in_token_diags_first(self):
        coords = set()
        used_tokens = self.ai.used_tokens + self.opp.used_tokens
        for c in used_tokens:
            x = c[0]
            y = c[1]
            lef = x - 1
            r = x + 1
            u = y + 1
            d = y - 1
            for xi, yi in [(lef, u), (r, u), (lef, d), (r, d)]:
                if not self.out_of_bounds_or_occupied(xi, yi) and not self.board.token_is_lonely(xi, yi):
                    coords.add((xi, yi, None, None))

        return coords

    def get_all_possible_moves(self, x, y):
        # set up the 8 possible coordinate moves
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x + 1, y + 1), (x - 1, y - 1),
                 (x + 1, y - 1)]

        possible_moves = [(x, y, m[0], m[1]) for m in moves if not self.out_of_bounds_or_occupied(m[0], m[1])]
        return possible_moves

    def out_of_bounds_or_occupied(self, x, y):
        out_of_bounds = self.board.coordinates_not_in_bounds(x, y)
        if out_of_bounds:
            return True
        else:
            return self.board.coordinate_already_occupied(x, y)

    def copy(self):
        return GameState(self.board.copy(), self.moves_left, (self.ai.copy(), self.opp.copy()))

    def new_state_from_action(self, action, p_pos):
        x1, y1, x2, y2 = action
        new_state = self.copy()

        # ADD
        if x2 is None and y2 is None:
            new_state.add_token_at(p_pos, x1, y1)
        # MOVE
        else:
            new_state.move_token(p_pos, x1, y1, x2, y2)

        return new_state

    def add_token_at(self, p_pos, x, y):
        # place token on board and reduce token count
        player = self.players[p_pos]
        self.board.add_token_to_board(player, x, y)

        #  TODO: disable checks
        # self.board.np_board[x - 1][y - 1] = player.number
        # player.use_token((x, y))

    def move_token(self, p_pos, x1, y1, x2, y2):
        # open the original position and take new position
        player = self.players[p_pos]
        self.board.move_token_on_board(player, x1, y1, x2, y2)

        # self.board.np_board[x1 - 1][y1 - 1] = Board.OPEN_SPACE
        # self.board.np_board[x2 - 1][y2 - 1] = player.number

        # muse update max moves in game
        self.moves_left -= 1

    def game_over(self):
        winner_set = set()
        # winner_set = self.board.check_if_someone_won()
        used_tokens = self.ai.used_tokens + self.opp.used_tokens
        winner_set = self.board.check_if_someone_won_using_tokens(used_tokens)
        # for player in self.players:
        #     is_win = any(self.is_win_coord(token_coord) for token_coord in player.used_tokens)
        #     if is_win:
        #         winner_set.add(player.number)

        # check winners
        if bool(winner_set):
            if self.ai.number in winner_set:
                return GameState.MAX_SCORE
            else:
                return GameState.MIN_SCORE
        # check draw
        elif all(not player.has_tokens() for player in self.players) and self.moves_left == 0:
            return 0
        # game keeps going
        else:
            return None

    def get_heuristic_score(self):
        max_score = 0
        for token_coords in self.ai.used_tokens:
            max_score += 1
            if self.ai.tokens_left <= 8:
                max_score -= 20 * len(self.ai.used_tokens)
            max_score += self.possible_wins(token_coords, self.ai)

        max_score += self.find_win_strat(self.ai.number) * 300

        min_score = 0
        for token_coords in self.opp.used_tokens:
            min_score += 1
            min_score += self.possible_wins(token_coords, self.opp)

        if self.ai.number == 1:
            max_score *= 1
        else:
            min_score *= 1

        dif = max_score - min_score
        return dif

    def possible_wins(self, coords, player):
        x = coords[0]
        y = coords[1]

        score = 0
        score += self.get_score_as_top_right(x, y, player)
        score += self.get_score_as_top_left(x, y, player)
        score += self.get_score_as_bottom_right(x, y, player)
        score += self.get_score_as_bottom_left(x, y, player)
        score += self.get_score_as_middle(x, y, player)
        return score

    def get_score_as_middle(self, x, y, player):
        top_left = (x - 1, y + 1)
        top_right = (x + 1, y + 1)
        bot_left = (x - 1, y - 1)
        bot_right = (x + 1, y - 1)
        return self.evaluate_coords([top_left, top_right, bot_left, bot_right], player)

    def get_score_as_top_right(self, x, y, player):
        top_left = (x - 2, y)
        middle = (x - 1, y - 1)
        bot_left = (x - 2, y - 2)
        bot_right = (x, y - 2)
        return self.evaluate_coords([top_left, middle, bot_left, bot_right], player)

    def get_score_as_top_left(self, x, y, player):
        bot_right = (x + 2, y - 2)
        middle = (x + 1, y - 1)
        bot_left = (x, y - 2)
        top_right = (x + 2, y)
        return self.evaluate_coords([bot_right, middle, bot_left, top_right], player)

    def get_score_as_bottom_right(self, x, y, player):
        top_left = (x - 2, y + 2)
        middle = (x - 1, y + 1)
        bot_left = (x - 2, y)
        top_right = (x, y + 2)
        return self.evaluate_coords([top_left, middle, bot_left, top_right], player)

    def get_score_as_bottom_left(self, x, y, player):
        top_left = (x, y + 2)
        middle = (x + 1, y + 1)
        bot_right = (x + 2, y)
        top_right = (x + 2, y + 2)
        return self.evaluate_coords([top_left, middle, bot_right, top_right], player)

    def find_win_strat(self, p_num):
        score = self.board.win_strat_found(p_num)
        return score

    def evaluate_coords(self, coords, player):
        score = 0
        i = 20
        j = 15
        for coor in coords:
            a = coor[0]
            b = coor[1]

            if self.board.coordinates_not_in_bounds(a, b):
                score -= 4
            elif self.board.coordinate_already_occupied(a, b):
                if self.board.is_players_token(player, a, b):
                    score += i
                    i += i
                else:
                    score -= j
                    j *= j
            # empty space
            else:
                score += i

        return score
