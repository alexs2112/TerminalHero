from quests.quest import Quest

# pylint: disable=invalid-name
_quest_handler = None
def get_quest_handler():
    global _quest_handler
    if not _quest_handler:
        _quest_handler = QuestHandler()
    return _quest_handler

class QuestHandler:
    def __init__(self):
        self.quests: list[Quest] = []
        self.done: list[Quest] = []

    def get(self, i=-1):
        if i > -1:
            return self.quests[i]
        return self.quests

    def get_done(self, i=-1):
        if i > -1:
            return self.done[i]
        return self.done

    def add(self, quest: Quest):
        self.quests.append(quest)

    def add_done(self, quest: Quest):
        self.done.append(quest)

    def mark_complete(self, quest: Quest):
        self.quests.remove(quest)
        self.done.append(quest)
