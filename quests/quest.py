from quests.quest_step import QuestStep

class Quest:
    def __init__(self, name: str):
        self.name: str = name
        self.description: str = ""
        self.steps: list[QuestStep] = []

        # Which steps are required to complete in order for this quest to be completed
        self.required_steps: list[QuestStep] = []
        self.complete = False

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
        return True
