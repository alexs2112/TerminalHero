from quests.quest_step import QuestStep
from main.messenger import get_messenger
from main.notification import add_notification

messenger = get_messenger()

class Quest:
    def __init__(self, name: str, quest_id: str):
        self.name: str = name
        self.id: str = quest_id
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
            print(f"{i}: {step.name}\n\t{step.description}\n\t{step.check_completion()}")
            i += 1
        print()

    def check_completion(self):
        if self.complete:
            return True
        for step in self.required_steps:
            if not step.check_completion():
                return False
        self.complete = True
        messenger.add(f"Quest Complete! {self.name}")
        add_notification(["Quest Complete!", self.completion_text])
        return True
