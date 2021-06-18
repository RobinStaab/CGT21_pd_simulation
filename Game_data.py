class Game_data:
    def __init__(self, epoch, player_id, opponent_id, player_decision, opponent_decision, player_strategy, other_strategy, player_util, opponent_util, data) -> None:
        """Game data

        Args:
            epoch (int)             : epoch of the game
            player_id (int)         : id of the player
            opponent_id (int)       : id of the opponent
            player_decision         : decision of the player
            opponent_decision       : decision of the opponent
            player_strategy         : strategy the player is currently following
            other_strategy          : strategy the other player is currently following
            player_util (float)     : utility of the player
            opponent_util (float)   : utility of the opponent
            data (dict)             : additional data
        """
        self.epoch              = epoch
        self.player_id          = player_id
        self.opponent_id        = opponent_id
        self.player_decision    = player_decision
        self.opponent_decision  = opponent_decision
        self.player_strategy    = player_strategy
        self.other_strategy     = other_strategy
        self.player_util        = player_util
        self.opponent_util      = opponent_util
        self.data               = data