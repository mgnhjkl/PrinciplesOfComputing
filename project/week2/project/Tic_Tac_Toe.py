"""
Provided Code for Tic-Tac-Toe
"""

import random

# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}


class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        self._dim = dim
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(dim)]
                           for dummyrow in range(dim)]
        else:
            # Copy board grid
            self._board = [[board[row][col] for col in range(dim)]
                           for row in range(dim)]

    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim

    def square(self, row, col):
        """
        Return the status (EMPTY, PLAYERX, PLAYERO) of the square at
        position (row, col).
        """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).

        Does nothing if board square is not empty.
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """
        If someone has won, return player.
        If game is a draw, return DRAW.
        If game is in progress, return None.
        """
        lines = []

        # rows
        lines.extend(self._board)

        # cols
        cols = [[self._board[rowidx][colidx] for rowidx in range(self._dim)]
                for colidx in range(self._dim)]
        lines.extend(cols)

        # diags
        diag1 = [self._board[idx][idx] for idx in range(self._dim)]
        diag2 = [self._board[idx][self._dim - idx - 1]
                 for idx in range(self._dim)]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None

    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board)


def switch_player(player):
    """
    Convenience function to switch players.

    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX


def play_game(mc_move_function, ntrials, reverse = False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None

    # Run game
    while winner == None:
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = switch_player(curplayer)

        # Display board
        print board
        print

    # Print winner
    if winner == PLAYERX:
        print "X wins!"
    elif winner == PLAYERO:
        print "O wins!"
    elif winner == DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"

def mc_trial(board, player):
    """
    Takes a current board and the next player to move
    """
    curplayer = player
    winner = None
    empty = []
    while winner == None:
        empty = board.get_empty_squares()
        if len(empty) == 0:
            print board.check_win()
        if len(empty) > 1:
            square_rand = empty[random.randint(0, len(empty) - 1)]
        else:
            square_rand = empty[0]
        board.move(square_rand[0], square_rand[1], curplayer)
        winner = board.check_win()
        curplayer = switch_player(curplayer)

def mc_update_scores(scores, board, player):
    """
    Update scores
    """
    if board.check_win() == DRAW:
        return
    else:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row,col) == player:
                    if player == board.check_win():
                        scores[row][col] += 1
                    else:
                        scores[row][col] -= 1


def get_best_move(board, scores):
    """
    Choose the square with the highest score as next move
    """
    squares = []
    empty = board.get_empty_squares()
    return get_max_square(empty, scores)

def get_max_square(squares, scores):
    """
    Return the square with the maximum score
    """
    square_max = [squares[0][0], squares[0][1]]
    score_max = scores[squares[0][0]][squares[0][1]]
    for square in squares:
        if scores[square[0]][square[1]] > score_max:
            square_max = [square[0], square[1]]
            score_max = scores[square[0]][square[1]]
    return square_max

def mc_move(board, player, trials):
    """
    The function should use the Monte Carlo simulation described above to return a move for the machine player in the form of a (row, column) tuple.
    """
    scores = [[0 for dummy_col in range(3)]
                        for dummy_row in range(3)]
    curplayer = random.randint(PLAYERX, PLAYERO)
    for dummy_index in range(trials):
        board_tmp = board.clone()
        mc_trial(board_tmp, curplayer)
        mc_update_scores(scores, board_tmp, curplayer)
    print scores
    square = get_best_move(board, scores)
    return (square[0], square[1])

play_game(mc_move, 500)