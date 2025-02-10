from dialog.dialog_node import DialogNode

RESULT_ODDS = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1
}

class DialogRoll(DialogNode):
    def __init__(self, node_id: str, name: str, text: str, value: int, stat: str, success: DialogNode, failure: DialogNode):
        super().__init__(node_id, name, text, [])
        self.type = "Roll"
        self.value = value
        self.stat = stat
        self.success = success
        self.failure = failure

    def roll_successful(self, roll_total, player):
        return roll_total + player.stat(self.stat) >= self.value

    # I feel like we could do this with an actual formula lol
    def percentage(self, player):
        target = self.value - player.stat(self.stat)
        if target > 12:
            return 0
        elif target > 2:
            total = 0
            for i in range(target, 13):
                total += RESULT_ODDS[i]
            return int((total * 100) / 36)
        else:
            return 100
