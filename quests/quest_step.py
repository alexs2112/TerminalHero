from main.player_log import get_player_log
player_log = get_player_log()

class QuestStep:
    def __init__(self, name):
        self.name = name
        self.description = ""

        # What needs to be True in the player_log for this one to show up
        self.required = []

        # What needs to be True in the player_log for this to count as complete
        self.log_completion = ""

    def set_description(self, description: str):
        self.description = description

    def set_log_completion(self, player_log_field: str):
        self.log_completion = player_log_field

    def check_completion(self):
        if self.log_completion in player_log and player_log[self.log_completion]:
            return True
        return False

    def is_enabled(self):
        for q in self.required:
            if not player_log[q]:
                return False
        return True
