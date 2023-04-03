"""
Module for TA to run
"""
import doctest
from python_ta.contracts import check_contracts
import python_ta
import connect_four
from players import HumanPlayer, AIPlayer
import pygame
import gameinterface
import sys
import math


def get_human_turn() -> tuple[int, int]:
    """
    Let human player choose whether they want to go first or second.
    Returns a tuple of (human player's number, AI player's number)
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
    gboard = gameinterface.GameInterface(5, 5)
    game = connect_four.ConnectFour(5, 5)
    gboard.draw_board(game.board)
    turns = get_human_turn()
    human = HumanPlayer(game, turns[0])
    if turns[1] == 1:
        ai = AIPlayer(game, 1, 'AI Models/5x5_tree_randagent_P1')
    else:
        ai = AIPlayer(game, 2, 'AI Models/5x5_tree_randagent_P2')

    while game.get_winner() is None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # if AI player's turn
            if (game.is_player_1_turn() and turns[1] == 1) or (not game.is_player_1_turn() and turns[1] == 2):
                ai.make_move()
                gboard.draw_board(game.board)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if human player's turn
                if (game.is_player_1_turn() and turns[0] == 1) or (not game.is_player_1_turn() and turns[0] == 2):
                    x = event.pos[0]
                    col_num = int(math.floor(x / 100))
                    row_num = gboard.get_next_open_row(game.board, col_num)
                    human.make_move(row_num, col_num)
                    gboard.draw_board(game.board)

    print(f'Winner: {game.get_winner()}')
    return game
