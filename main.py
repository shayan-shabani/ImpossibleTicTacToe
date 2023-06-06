import copy
import numpy as np
import pygame
import sys

from constant_components import *

pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill((220, 220, 220))
pygame.display.set_caption("Tic Tac Toe")


class Board():
    def __init__(self):
        self.squares = np.zeros((rows, columns))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def states(self):
        for col in range(columns): # vertical wins
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[2][col]

        for row in range(rows): # horizontal wins
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][2]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0: # descending diagonal wins
            return self.squares[2][2]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:  # ascending diagonal wins
            return self.squares[0][2]

        return 0  # if there is no win yet

    def update_sqaure(self, row, column, player):
        self.squares[row][column] = player
        self.marked_sqrs += 1

    def empty_square(self, row, column):
        return self.squares[row][column] == 0

    def is_full(self):
        return self.marked_sqrs == 9

    def is_empty(self):
        return self.marked_sqrs == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for i in range(rows):
            for j in range(columns):
                if self.empty_square(i, j):
                    empty_sqrs.append( (i, j) )

        return empty_sqrs


class Minimax:
    def __init__(self, bot=1, player=2):
        self.bot = bot
        self.player = player

    def algorithm(self, board, maximizing):
        case = board.states()  # keeping track of terminal cases

        if case == 1:  # player 1 wins
            return 1, None

        if case == 2:  # player 2 wins
            return -1, None

        elif board.is_full():  # draw
            return 0, None

        if maximizing:
            max_eval = -2
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                board_copy = copy.deepcopy(board)
                board_copy.update_sqaure(row, col, 1)
                eval = self.algorithm(board_copy, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 2
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                board_copy = copy.deepcopy(board)
                board_copy.update_sqaure(row, col, self.player)
                eval = self.algorithm(board_copy, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        eval, move = self.algorithm(main_board, False)
        return move


class TicTacToe():
    def __init__(self):
        self.player = 1
        self.bot = Minimax()
        self.board = Board()
        self.display_lines()
        self.running = True

    def display_lines(self):
        pygame.draw.line(screen, line_color, (sqr_size, 0), (sqr_size, height), line_width)
        pygame.draw.line(screen, line_color, (2*sqr_size, 0), (2*sqr_size, height), line_width)

        pygame.draw.line(screen, line_color, (0, sqr_size), (width, sqr_size), line_width)
        pygame.draw.line(screen, line_color, (0, 2*sqr_size), (width, 2*sqr_size), line_width)

    def next_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def draw_shape(self, row, column):
        if self.player == 1:
            center = (column * sqr_size + sqr_size // 2, row * sqr_size + sqr_size // 2)
            pygame.draw.circle(screen, circ_color, center, radius, circ_width)

        elif self.player == 2:
            start_pos_desc = (column * sqr_size + line_dist, row * sqr_size + line_dist)
            end_pos_desc = (column * sqr_size + sqr_size - line_dist, row * sqr_size + sqr_size - line_dist)
            pygame.draw.line(screen, cross_color, start_pos_desc, end_pos_desc, cross_width)

            start_pos_asc = (column * sqr_size + line_dist, row * sqr_size + sqr_size - line_dist)
            end_pos_asc = (column * sqr_size + sqr_size - line_dist, row * sqr_size + line_dist)
            pygame.draw.line(screen, cross_color, start_pos_asc, end_pos_asc, cross_width)

    def make_move(self, row, col):
        self.board.update_sqaure(row, col, self.player)
        self.draw_shape(row, col)
        self.next_turn()

    def is_over(self):
        return self.board.states() != 0 or self.board.is_full()

def main():
    game = TicTacToe()
    board = game.board
    bot = game.bot

    while True: # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                column = position[0] // sqr_size
                row = position[1] // sqr_size

                if board.empty_square(row, column):
                    board.update_sqaure(row, column, game.player)
                    game.draw_shape(row, column)
                    game.next_turn()

        if game.player == bot.player and game.running:
            pygame.display.update()

            row, column = bot.eval(board)
            game.make_move(row, column)

            if game.is_over():
                game.running = False

        pygame.display.update()

main()