from quests.quest_step import QuestStep
from main.messenger import get_messenger
from main.notification import set_notification

messenger = get_messenger()

class Quest:
    def __init__(self, name: str):
        self.name: str = name
        self.description: str = ""
        self.steps: list[QuestStep] = []

        # Which steps are required to complete in order for this quest to be completed
        self.required_steps: list[QuestStep] = []
        self.complete = False

        # Text to display as a notification when the quest is complete
        self.completion_text = self.name

    def set_description(self, description: str):
        self.description = description

    def debug_print(self):
        print(f"{self.name}\n\t{self.description}\n\t{self.complete}")
        i = 1
        for step in self.steps:
            print(f"{i}: {step.name}\n\t{step.description}\n\t{step.complete}")
            i += 1
        print()

    def check_completion(self):
        for step in self.steps:
            step.check_completion()
        if self.complete:
            return True
        for step in self.required_steps:
            if not step.complete:
                return False
        self.complete = True
        messenger.add(f"Quest Complete! {self.name}")
        set_notification(["Quest Complete!", self.completion_text])
        return True
