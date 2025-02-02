from quests.quest import Quest
from quests.quest_step import QuestStep

#pylint: disable=line-too-long
def grave_concerns():
    q = Quest("Grave Concerns")
    q.set_description("Elder Varik has asked you to aid in finding Gorren, the Soulwarden of Arad and find out what he has been up to.")

    step1 = QuestStep("Find Gorren, the Grave-Touched")
    step1.set_description("Elder Varik directed you to the Cemetery North-East of the Village of Arad.")
    step1.set_log_completion("gorren_leaves_church")

    step2 = QuestStep("Find out how to unseal the Vaelthorne Crypt")
    step2.set_description("Gorren has directed you towards the Vaelthorne Crypt, however it remains sealed. Visit the Crypt to find hints, and ask around town to see if you can find a good starting point.")
    step2.set_log_completion("known_shrine")
    step2.required = [ "gorren_leaves_church" ]

    step3 = QuestStep("Unlock the secrets of the Vaelthorne Shrine")
    step3.set_description("Bartender Doran the Red has told you about the ancient Vaelthorne Shrine that may have the key to your troubles.")
    step3.set_log_completion("runebound_stalker_defeated")
    step3.required = [ "known_shrine" ]

    step4 = QuestStep("Explore the Vaelthorne Crypt for another Obsidian Lantern")
    step4.set_description("With the Vaelthorne Seal in hand you should be able to get into the Vaelthorne Crypt. Search for another Obsidian Lantern to finish Gorren's Ritual.")
    step4.set_log_completion("unhallowed_guardian_defeated")
    step4.required.append("runebound_stalker_defeated")

    step5 = QuestStep("Complete Gorren's Banishment Ritual")
    step5.set_description("Now that you have another Obsidian Lantern, return to the Eternal Church in the Cemetery to complete the Banishment Ritual, purging Arad of the undead.")
    step5.set_log_completion("finish_cemetery_stage_3")
    step5.required.append("unhallowed_guardian_defeated")

    q.steps = [ step1, step2, step3, step4, step5 ]
    q.required_steps = [ step1, step2, step3, step4, step5 ]
    return q

def scales_and_spurs():
    q = Quest("Scales and Spurs")
    q.set_description("Elder Varik notified you of a raided import caravan outside of town.")

    step1 = QuestStep("Investigate the Wreckage")
    step1.set_description("Examine the area of the caravan wreckage South-West of the Village of Arad.")
    step1.set_log_completion("met_rangu")

    q.steps = [ step1 ]
    q.required_steps = [ step1 ]
    return q
