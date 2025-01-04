from world.world import World
from world.area import Area
from world.encounter_factory import EncounterFactory
from creature.creature_factory import CreatureFactory

class WorldBuilder:
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.creature_factory = CreatureFactory()
        self.encounter_factory = EncounterFactory()
        self.world: World = None
        self.initialize_world()

    def initialize_world(self):
        self.world = World(self.width, self.height)

    #pylint: disable=line-too-long
    def build_world(self):
        area = Area("Forest", (1,1,12,12),
                    "Dense shrubs and thorny vines choke the undergrowth, making travel slow and difficult. "
                    "The trees here are unremarkable, their bark rough and weathered by years of wind and rain.")
        area.is_filler = True
        self.world.areas[0][0] = area

        area = Area("Forest", (14,1,12,12),
                    "Thin, spindly trees rise from an uneven forest floor covered in dry leaves and small thistles. "
                    "The sunlight filters through the sparse canopy, leaving patches of light scattered throughout.")
        area.is_filler = True
        self.world.areas[1][0] = area

        area = Area("The Corpse Pile", (27,1,12,12),
                    "Just outside of the wooden palisade walls of the village, a pile of corpses grows with bodies of the shrinking population. "
                    "A growing population of giant vermin feast on the bodies within.")
        area.encounters = [
            self.encounter_factory.get_cemetery_encounter_1()
        ]
        area.condition = 'known_cemetery'
        area.entry_log_update = 'visit_cemetery'
        self.world.areas[2][0] = area

        area = Area("Mining Village of Arad", (1,14,12,12),
                    "The Mining Village of Arad is a harsh, desolate settlement, built around the remnants of a fallen Bloodstone meteorite. "
                    "This rare and magical gemstone, prized for its powerful healing properties, is the lifeblood of the village - and its curse. "
                    "Life in Arad is bleak, with the villagers, known as Meldspawn, toiling endlessly in the dangerous mines to meet the Capital's unrelenting demands.")
        area.npcs = [self.creature_factory.new_elder_varik()]
        self.world.areas[0][1] = area

        area = Area("The Bloodstone Mine", (14,14,12,12),
                    "The village is built around the remains of a Bloodstone meteorite that had struck the earth a long time ago. "
                    "It's an unstable and treacherous place, prone to cave-ins and the occasional appearance of strange, magical creatures drawn to the Bloodstone. "
                    "The foreman is employed by the capital and is required to meet the monthly quota of Bloodstone. "
                    "He has a set of armed militiamen for the day to day mining to keep watch over the workers.")
        area.condition = 'known_bloodstone_mine'
        self.world.areas[1][1] = area

        area = Area("Plains", (27,14,12,12),
                    "A flat plain dotted with occasional patches of bare earth and smooth, weathered stones. "
                    "The only movement comes from the swaying grass and the distant flight of a bird.")
        area.is_filler = True
        self.world.areas[2][1] = area

        area = Area("The Starvation Pit", (1,27,12,12),
                    "A grim gathering place where families who can't afford to buy food come to collect leftovers or fight over meager rations. "
                    "The pit is full of scavengers and desperate people.")
        area.condition = 'known_starvation_pit'
        self.world.areas[0][2] = area

        area = Area("The Garrison", (14,27,12,12),
                    "A heavily guarded compound outside of the city stationed by Capital soldiers. "
                    "Only concerned with the mining and Bloodstone shipments, otherwise they do not care about the villagers well-being and don't seek to govern them directly.")
        area.condition = 'known_garrison'
        self.world.areas[1][2] = area

        area = Area("Plains", (27,27,12,12),
                    "A monotonous expanse of grass punctuated by small, jagged rocks protruding from the ground. "
                    "The wind carries a faint whistle, uninterrupted by any sign of trees or shelter.")
        area.is_filler = True
        self.world.areas[2][2] = area
        return self.world
