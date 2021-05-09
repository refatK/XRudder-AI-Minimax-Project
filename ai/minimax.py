from ai.gamestate import GameState


def get_move(state, depth):
    root_minimax = MiniMax(state, True, depth)
    root_minimax_with_result = root_minimax.run()
    print(f'found score of {root_minimax_with_result.score}')

    next_action = root_minimax_with_result.next_best_node.action
    return next_action


class MiniMax:
    is_ai: bool
    state: GameState
    DEFAULT_DEPTH = 3

    def __init__(self, state: GameState, is_ai, depth=DEFAULT_DEPTH, action=None, a=GameState.MIN_SCORE,
                 b=GameState.MAX_SCORE):
        self.state = state
        self.is_ai = is_ai
        self.depth = depth
        self.action = action
        self.a = a
        self.b = b

        self.actions = []
        self.p_pos = 0 if is_ai else 1
        # Start with worst possible score
        self.score = GameState.MIN_SCORE if is_ai else GameState.MAX_SCORE
        self.next_best_node = None

    @property
    def players(self):
        return self.state.players

    def gen_child(self, action, a, b):
        next_possible_state = self.state.new_state_from_action(action, self.p_pos)
        return MiniMax(next_possible_state, not self.is_ai, self.depth - 1, action, a, b)

    # def gen_children(self, a, b):
    #     self.actions = self.state.get_all_possible_actions(self.p_pos, self.is_ai)
    #     for action in self.actions:
    #         next_possible_state = self.state.new_state_from_action(action, self.p_pos)
    #         self.children.append(MiniMax(next_possible_state, not self.is_ai, self.depth - 1, action, a, b))

    def run(self):
        # FIRST HANDLE BASE CASES
        # check for game end due to win or draw
        game_over_score = self.state.game_over()
        if game_over_score is not None:
            self.score = game_over_score
            return self

        # if got to the max depth we wanted, also stop and apply heuristic
        if self.depth == 0:
            self.score = self.state.get_heuristic_score()
            return self

        # ELSE CONTINUE WITH CHECKING NEXT MOVES
        # generate all possible next states
        self.actions = self.state.get_all_possible_actions(self.p_pos, self.is_ai)

        if self.is_ai:
            return self.maximize()
        else:
            return self.minimize()

    def maximize(self):
        n: MiniMax
        for action in self.actions:
            n = self.gen_child(action, self.a, self.b)
            n_with_score = n.run()

            if self.next_best_node is None:
                self.next_best_node = n_with_score

            if n_with_score.score > self.score:
                self.score = n_with_score.score
                self.next_best_node = n_with_score
            self.a = self.score
            if self.a >= self.b:
                return self
        return self

    def minimize(self):
        n: MiniMax
        for action in self.actions:
            n = self.gen_child(action, self.a, self.b)
            n_with_score = n.run()

            if self.next_best_node is None:
                self.next_best_node = n_with_score

            if n_with_score.score < self.score:
                self.score = n_with_score.score
                self.next_best_node = n_with_score
            self.b = self.score
            if self.a >= self.b:
                return self
        return self
