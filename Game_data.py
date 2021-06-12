class Game_data:
    def __init__(self, epoch, player_id, opponent_id, player_util, opponent_util, data) -> None:
        """Game data

        Args:
            epoch (int)             : epoch of the game
            player_id (int)         : id of the player
            opponent_id (int)       : id of the opponent
            player_util (float)     : utility of the player
            opponent_util (float)   : utility of the opponent
            data (dict)             : additional data
        """
        self.epoch = epoch
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.player_util = player_util
        self.opponent_util = opponent_util
        self.data = data