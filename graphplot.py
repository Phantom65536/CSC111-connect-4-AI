"""
GraphPlot class
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class GraphPlot:
    """
    A GraphPlot class that contains methods to plot graphs to analyse the AI’s performance against
    a TrainingAgent instance or a trained AIPlayer instance.
    
    Instance Attributes:
        - results: A list of winners of each game, consisting of either (player) 1 or 2. A 0 indicates a draw.
        - ai_player: The player number indicating the AI player.

    Representation Invariants:
        - all(num in {0, 1, 2} for num in self.results)
        - ai_player in {1, 2}
    """
    results: list[int]
    ai_player: int

    def __init__(self, results: list[int], ai: int) -> None:
        """Initalize a new GraphPlot instance using results.

        Preconditions:
            - len(results) > 0
            - ai in {1, 2}
        """
        self.results = results
        self.ai_player = ai

    def plot_game_stats(self) -> None:
        """
        Plots the following game statistics:
        1. Outcomes: a scatter plot showing the outcome of each game,
        where 1 represents a win for player 1 and 0 represents a win for player 2.
        2. Player 1 cumulative win percentages: a scatter plot showing the cumulative win percentage
        for player 1 over all games played.
        3. Number of wins: a bar plot showing the number of wins for player 1 and player 2.
        """
        outcomes = self.results
        cumulative_win_percentage = [sum(outcomes[0:i]) / i for i in range(1, len(outcomes) + 1)]
        num_of_wins = [self.results.count(1), self.results.count(2), self.results.count(0)]

        fig = make_subplots(rows=2, cols=2)

        fig.add_trace(go.Scatter(y=outcomes, mode='markers',
                                 name='Outcome (1 = Player 1 win, 0 = Player 2 win, 0 = Draw)'),
                      row=1, col=1)

        fig.add_trace(go.Scatter(y=cumulative_win_percentage, mode='lines',
                                 name='Player 1 win percentage (cumulative)'),
                      row=2, col=1)

        fig.append_trace(go.Bar(x=['Player 1', 'Player 2', 'Draw'], y=num_of_wins,
                                text=num_of_wins, textposition='auto',
                                name='Number of wins for player 1 and 2'), row=1, col=2)

        fig.update_yaxes(range=[0.0, 1.0], row=2, col=2)
        fig.update_layout(title='Connect 4 Game Results', xaxis_title='Game')
        fig.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects', 'plotly.subplots'],  # the names (strs) of imported modules
        'allowed-io': ['plot_game_stats'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
