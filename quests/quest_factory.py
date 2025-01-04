from quests.quest import Quest
from quests.quest_step import QuestStep

#pylint: disable=line-too-long
def investigate_corpse_pile():
    q = Quest("Where are my corpses?")
    q.set_description("Elder Varik has asked you to investigate the nearby cemetery to find out what is happening to the dug-up graves.")
    step1 = QuestStep("Visit the Cemetery")
    step1.set_description("The cemetery is located to the North-East of the Village of Arad.")
    step1.set_log_completion("visit_cemetery")

    step2 = QuestStep("Clear the Corpse Pile of Enemies")
    step2.set_description("You have observed giant vermin feasting on the corpses of Meldkin. Slay them.")
    step2.set_log_completion("clear_cemetery_1")
    step2.required.append(step1)

    step3 = QuestStep("Examine the Crypt")
    step3.set_description("After defeating the patchwork dead, you notice whimpering coming from a nearby open crypt.")
    step3.set_log_completion("met_gorren")
    step3.required.append(step2)

    q.steps = [ step1, step2, step3 ]
    q.required_steps = [ step1, step2, step3 ]
    return q
