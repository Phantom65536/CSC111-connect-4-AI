import connect_four
import players

if __name__ == "__main__":
    game = connect_four.ConnectFour(5, 8)
    player_1 = players.TrainingAgent(game, 1)
    player_2 = players.TrainingAgent(game, 2)
    while game.get_winner() is None:
        player_1.make_move()
        print(game.board)
        if game.get_winner() is not None:
            break
        player_2.make_move()
        print(game.board)
    print(f'{game.board}\nWinner: {game.get_winner()}')
