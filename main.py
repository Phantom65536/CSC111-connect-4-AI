"""
Module for TA to run
"""
import doctest
from python_ta.contracts import check_contracts
import python_ta
import connect_four
from players import HumanPlayer, AIPlayer, RandomAgent
import pygame
import gameinterface2
import sys
import math


def get_human_turn() -> tuple[int, int]:
    """
    Let human player choose whether they want to go first or second.
    Returns a tuple of (human player's number, ai player's number)
    """
    hturn = input("Choose whether you would like to go first or second. Please input 1 or 2.")
    if int(hturn) == 1:
        aiturn = 2
    else:
        aiturn = 1
    return (int(hturn), aiturn)


def runner() -> connect_four.ConnectFour:
    """
    Run one game between HumanPlayer and AIPlayer.
    Return the ConnectFour instance after the game is finished.
    """
    size = (500, 500)
    board = gameinterface2.GameInterface(5, 5)
    screen = pygame.display.set_mode(size)
    board.draw_board(screen)
    pygame.display.update()
    game = connect_four.ConnectFour(5, 5)
    turns = get_human_turn()
    human = HumanPlayer(game, turns[0])
    print('AI Model loading')
    if turns[1] == 1:
        ai = AIPlayer(game, 1, '5x5_tree_randagent_P1')
    else:
        ai = AIPlayer(game, 2, '5x5_tree_randagent_P2')
    print('AI Model loaded')

    while game.get_winner() is None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # if AI player's turn
            if (game.is_player_1_turn() and turns[1] == 1) or (not game.is_player_1_turn() and turns[1] == 2):
                ai.make_move()
                board.board = game.get_gameboard()
                board.draw_board(screen)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if human player's turn
                if (game.is_player_1_turn() and turns[0] == 1) or (not game.is_player_1_turn() and turns[0] == 2):
                    x = event.pos[0]
                    col_num = int(math.floor(x / 100))
                    row_num = board.get_next_open_row(col_num)
                    human.make_move(row_num, col_num)
                    board.board = game.get_gameboard()
                    board.draw_board(screen)

    print(f'Winner: {game.get_winner()}')
    return game


if __name__ == '__main__':
    runner()
