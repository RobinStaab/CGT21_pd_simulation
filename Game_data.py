class Game_data:
    def __init__(self, epoch, player_id, opponent_id) -> None:
        """Game data

        Args:
            epoch (int): epoch of the game
        """
        self.epoch = epoch
        self.player_id = player_id
        self.opponent_id = opponent_id