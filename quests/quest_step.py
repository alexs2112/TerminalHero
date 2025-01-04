from main.player_log import get_player_log
player_log = get_player_log()

class QuestStep:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.complete = False

        # Required other quest steps for this one to show
        self.required = []

        # What needs to be True in the player_log for this to count as complete
        self.log_completion = ""

    def set_description(self, description: str):
        self.description = description

    def set_log_completion(self, player_log_field: str):
        self.log_completion = player_log_field

    def check_completion(self):
        if self.complete:
            return True
        if self.log_completion in player_log:
            if player_log[self.log_completion]:
                self.complete = True
        return self.complete

    def is_enabled(self):
        for q in self.required:
            if not q.complete:
                return False
        return True
