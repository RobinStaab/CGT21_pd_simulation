from Game_data import Game_data

class History:
    def __init__(self) -> None:
        """History
        """
        self.data = {}
        self.epoch_cap = 50

    def add_game(self, opponent_id, game_data: Game_data) -> None:
        """Adds game_data dict to history

        Args:
            opponent_id (int): id of opponent
            game_data (Game_data): data of the game

        """
        #create list of game outcomes if it doesn't exist
        if not self.data.has_key(opponent_id):
            self.data[opponent_id] = []
        self.data[opponent_id].append(game_data)
        #check if newly added game_data has newer epoch than previously added game_data
        assert self.data[opponent_id][-1].epoch > self.data[opponent_id][-2].epoch
    
    def reduce(self, current_epoch) -> None:
        """Reduces history to epoch_cap

        Args:
            current_epoch (int): the current epoch
        """
        oldest_epoch = max(current_epoch - self.epoch_cap,0)

        for opponent_id in self.data:
            for i in range(len(self.data[opponent_id])):
                if self.data[opponent_id][i].epoch >= oldest_epoch:
                    self.data[opponent_id] = self.data[opponent_id][i:]
                    break