from sortedcontainers import SortedDict
from Game_data import Game_data

class History:
    def __init__(self) -> None:
        """History
        """
        self.history = SortedDict({})
        self.epoch_cap = 50

    def add_game(self, game_data: Game_data) -> None:
        """Adds Game_data to history

        Args:
            game_data (Game_data): data of the game

        """
        #create list of game outcomes if it doesn't exist
        if self.history.get(game_data.opponent_id) == None:
            self.history[game_data.opponent_id] = []
        self.history[game_data.opponent_id].append(game_data)
        #check if newly added game_data has newer epoch than previously added game_data
        if len(self.history[game_data.opponent_id]) > 1:
            assert self.history[game_data.opponent_id][-1].epoch > self.history[game_data.opponent_id][-2].epoch
    
    def reduce(self, current_epoch) -> None:
        """Reduces history to epoch_cap

        Args:
            current_epoch (int): the current epoch
        """
        oldest_epoch = max(current_epoch - self.epoch_cap,0)

        for opponent_id in self.history:
            for i in range(len(self.history[opponent_id])):
                if self.history[opponent_id][i].epoch >= oldest_epoch:
                    self.history[opponent_id] = self.history[opponent_id][i:]
                    break

    def game_list(self, opponent_id):
        """Return game list matching opponent_id

        Args:
            opponent_id (int): id of the opponent
        """
        if self.history.get(opponent_id) == None:
            return []
        else:
            return self.history[opponent_id]